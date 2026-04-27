import psycopg
from config import SINK_CONN
from decoder import ChangeEvent

def get_connection():
    return psycopg.connect(SINK_CONN)

def apply(event: ChangeEvent):
    """
    Applies a change event to local PostgreSQL.
    All operations are idempotent — safe to replay if the agent crashes.
    """
    if event.op == 'insert':
        print("inserting to local")
        _upsert(event)
    elif event.op == 'update':
        print("updating to local")
        _upsert(event)     
    elif event.op == 'delete':
        print("deleting from local")
        _delete(event)

def _execute(sql: str, values: list, event: ChangeEvent = None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, values)
                conn.commit()
            except psycopg.errors.UndefinedTable:
                conn.rollback()
                if event:
                    print(f"[sink_postgres] Table {event.schema}.{event.table} not found. Creating it...")
                    _create_table(event)
                    _execute(sql, values)
                else:
                    raise
            except psycopg.errors.InvalidSchemaName:
                conn.rollback()
                if event:
                    print(f"[sink_postgres] Schema {event.schema} not found. Creating it...")
                    cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{event.schema}";')
                    conn.commit()
                    _execute(sql, values, event)
                else:
                    raise
            except Exception as e:
                conn.rollback()
                print(f"[sink_postgres] Error: {e}")
                raise

def _create_table(event: ChangeEvent):
    """
    Creates a simple table structure based on the incoming event data.
    All columns are treated as TEXT initially for maximum compatibility.
    """
    schema = event.schema
    table  = event.table
    cols   = event.data.keys() if event.data else event.old_data.keys()
    
    # Use id as the primary key if it exists, otherwise no PK for now
    cols_def = []
    for c in cols:
        if c.lower() == 'id':
            cols_def.append(f'"{c}" TEXT PRIMARY KEY')
        else:
            cols_def.append(f'"{c}" TEXT')
    
    sql = f'CREATE TABLE IF NOT EXISTS "{schema}"."{table}" ({", ".join(cols_def)});'
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}";')
            cur.execute(sql)
            conn.commit()
    print(f"[sink_postgres] Created table {schema}.{table}")

def _upsert(event: ChangeEvent):
    if not event.data:
        return

    columns = list(event.data.keys())
    values  = list(event.data.values())

    col_str     = ', '.join(f'"{c}"' for c in columns)
    placeholder = ', '.join(['%s'] * len(columns))
    
   
    conflict_target = '"id"' if 'id' in event.data else col_str
    update_str  = ', '.join(f'"{c}" = EXCLUDED."{c}"' for c in columns)

    sql = f"""
        INSERT INTO "{event.schema}"."{event.table}" ({col_str})
        VALUES ({placeholder})
        ON CONFLICT ({conflict_target}) DO UPDATE SET {update_str}
    """
    _execute(sql, values, event)

def _delete(event: ChangeEvent):
    source = event.old_data if event.old_data else event.data
    if not source:
        return

    conditions = ' AND '.join(f'"{k}" = %s' for k in source.keys())
    values     = list(source.values())

    sql = f'DELETE FROM "{event.schema}"."{event.table}" WHERE {conditions}'
    _execute(sql, values, event)