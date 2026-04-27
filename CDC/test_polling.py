import psycopg2
import psycopg2.extras
from psycopg2 import sql
from collections import defaultdict, deque
from config import SOURCE_CONN, SINK_CONN


# Data Type Mapping and Normalization

def normalize_type(data_type, udt_name):
    """
    Converts Postgres internal types → valid SQL types
    """
    if data_type == "USER-DEFINED":
        return udt_name  # enum or custom type

    mapping = {
        "character varying": "text",
        "character": "text",
        "timestamp without time zone": "timestamp",
        "timestamp with time zone": "timestamptz",
        "double precision": "double precision",
        "integer": "integer",
        "bigint": "bigint",
        "boolean": "boolean",
        "json": "json",
        "jsonb": "jsonb",
        "ARRAY": "text[]",
        "uuid": "uuid",
    }

    return mapping.get(data_type, "text")


# Enum Replications

def get_enums(conn):
    """
    Extract enum types from source DB
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.typname, e.enumlabel
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE n.nspname = 'public'
            ORDER BY t.typname, e.enumsortorder;
        """)
        rows = cur.fetchall()

    enums = defaultdict(list)
    for typ, label in rows:
        enums[typ].append(label)

    return enums


def create_enums(conn, enums):
    """
    Create enum types in sink DB
    """
    with conn.cursor() as cur:
        for enum_name, values in enums.items():
            try:
                values_sql = ", ".join([f"'{v}'" for v in values])

                cur.execute(f"""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_type WHERE typname = '{enum_name}'
                        ) THEN
                            CREATE TYPE {enum_name} AS ENUM ({values_sql});
                        END IF;
                    END $$;
                """)

            except Exception as e:
                print(f"[enum warn] {enum_name}: {e}")

    conn.commit()


# Schema Discovery

def get_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
              AND table_type='BASE TABLE'
        """)
        return [r[0] for r in cur.fetchall()]


def get_columns(conn, table):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name, data_type, is_nullable, udt_name
            FROM information_schema.columns
            WHERE table_schema='public'
              AND table_name=%s
            ORDER BY ordinal_position
        """, (table,))
        return cur.fetchall()


def get_primary_key(conn, table):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a
              ON a.attrelid = i.indrelid
             AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass
              AND i.indisprimary;
        """, (table,))
        r = cur.fetchall()
        return [row[0] for row in r]


def get_foreign_keys(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name,
                ccu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type='FOREIGN KEY'
              AND tc.table_schema='public';
        """)
        return cur.fetchall()


# Dependency Graph Logic

def build_graph(tables, fks):
    graph = defaultdict(set)
    indegree = {t: 0 for t in tables}

    for src, col, dst, ref in fks:
        if src != dst:
            graph[dst].add(src)
            indegree[src] += 1

    return graph, indegree


def topo_sort(graph, indegree):
    q = deque([n for n in indegree if indegree[n] == 0])
    order = []

    while q:
        n = q.popleft()
        order.append(n)

        for nxt in graph[n]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    if len(order) != len(indegree):
        raise Exception("Cycle detected in schema")

    return order


# Table and Constraint Creation

def create_table(conn, table, cols, pk_cols):
    col_defs = []

    for name, dtype, nullable, udt in cols:
        safe_type = normalize_type(dtype, udt)
        null_str = "" if nullable == "NO" else "NULL"
        col_defs.append(f'"{name}" {safe_type} {null_str}')

    sql_stmt = f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(col_defs)});'

    with conn.cursor() as cur:
        cur.execute(sql_stmt)
        
        if pk_cols:
            # Check if PK exists in sink
            cur.execute("""
                SELECT 1 FROM pg_index i 
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = %s::regclass AND i.indisprimary
            """, (table,))
            
            if not cur.fetchone():
                try:
                    pk_sql = sql.SQL(",").join(map(sql.Identifier, pk_cols))
                    cur.execute(sql.SQL('ALTER TABLE {} ADD PRIMARY KEY ({})').format(
                        sql.Identifier(table),
                        pk_sql
                    ))
                    print(f"[info] Added primary key ({', '.join(pk_cols)}) to {table}")
                except Exception as e:
                    print(f"[pk warn] {table}: {e}")

    conn.commit()


def create_foreign_keys(conn, fks):
    with conn.cursor() as cur:
        for src, col, dst, ref in fks:
            try:
                cur.execute(f"""
                    ALTER TABLE "{src}"
                    ADD CONSTRAINT fk_{src}_{col}
                    FOREIGN KEY ("{col}")
                    REFERENCES "{dst}"("{ref}");
                """)
            except Exception as e:
                print(f"[fk warn] {src}: {e}")

    conn.commit()


# Initial Data Snapshot Logic

def build_upsert(table, cols, pks):
    names = [c[0] for c in cols]

    col_sql = sql.SQL(",").join(map(sql.Identifier, names))
    val_sql = sql.SQL(",").join([sql.Placeholder()] * len(names))
    
    updates_list = [
        sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(c), sql.Identifier(c))
        for c in names if c not in pks
    ]
    
    pk_sql = sql.SQL(",").join(map(sql.Identifier, pks))

    if not updates_list:
        return sql.SQL("""
            INSERT INTO {table} ({cols})
            VALUES ({vals})
            ON CONFLICT ({pk})
            DO NOTHING
        """).format(
            table=sql.Identifier(table),
            cols=col_sql,
            vals=val_sql,
            pk=pk_sql
        )

    updates = sql.SQL(",").join(updates_list)

    return sql.SQL("""
        INSERT INTO {table} ({cols})
        VALUES ({vals})
        ON CONFLICT ({pk})
        DO UPDATE SET {updates}
    """).format(
        table=sql.Identifier(table),
        cols=col_sql,
        vals=val_sql,
        pk=pk_sql,
        updates=updates
    )


def snapshot(conn_src, conn_dst, order):
    for table in order:
        print(f"[data] {table}")

        with conn_src.cursor() as s, conn_dst.cursor() as t:
            s.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
            rows = s.fetchall()

            if not rows:
                continue

            cols = get_columns(conn_src, table)
            pks = get_primary_key(conn_src, table)

            if not pks:
                continue

            upsert = build_upsert(table, cols, pks)

            for row in rows:
                # Ensure JSON columns are properly encoded
                processed_row = []
                for val, col_info in zip(row, cols):
                    dtype = col_info[1] # data_type from information_schema
                    if dtype in ('json', 'jsonb'):
                        if val is not None:
                            # Use extras.Json to ensure proper encoding, 
                            # even if val is a string like "nothing"
                            processed_row.append(psycopg2.extras.Json(val))
                        else:
                            processed_row.append(None)
                    else:
                        processed_row.append(val)
                
                t.execute(upsert, processed_row)

        conn_dst.commit()


# Entry Point Logic

def run():
    src = psycopg2.connect(SOURCE_CONN)
    dst = psycopg2.connect(SINK_CONN)

    # with dst.cursor() as cur:
    #     print("Resetting sink database...")
    #     cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    #     dst.commit()

    src.autocommit = True
    dst.autocommit = True

    # Handle JSON/JSONB automatically
    psycopg2.extras.register_default_json(src)
    psycopg2.extras.register_default_json(dst)
    psycopg2.extras.register_default_jsonb(src)
    psycopg2.extras.register_default_jsonb(dst)

    tables = get_tables(src)
    fks = get_foreign_keys(src)

    print(f"[info] tables: {len(tables)}")
    print(f"[info] fk: {len(fks)}")

    enums = get_enums(src)
    create_enums(dst, enums)

    graph, indegree = build_graph(tables, fks)
    order = topo_sort(graph, indegree)

    print("\n[order]")
    for i, t in enumerate(order):
        print(i + 1, t)

    for table in order:
        cols = get_columns(src, table)
        pks = get_primary_key(src, table)
        create_table(dst, table, cols, pks)

    create_foreign_keys(dst, fks)

    snapshot(src, dst, order)

    print("\nInitial dump finished")


if __name__ == "__main__":
    run()