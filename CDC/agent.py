import time
import psycopg2
from psycopg2.extras import DictCursor

from config import SOURCE_CONN, REPLICATION_SLOT, PUBLICATION
from decoder import PgOutputDecoder
from checkpoint import save_lsn, load_lsn
import sink_postgres
import sink_file
import test_polling
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["initial_dump", "cdc"],
        required=False
    )
    return parser.parse_args()

def run():
    decoder = PgOutputDecoder()
    last_lsn = load_lsn()

    print(f"Starting SQL Polling")
    print(f"Resuming from local LSN: {last_lsn or 'latest'}")

    # Standard database connection (no replication protocol required)
    conn = psycopg2.connect(SOURCE_CONN)
    conn.autocommit = True

    print(f"Connected. Polling for logical changes...")

    while True:
        with conn.cursor() as cur:
            # PEEK the latest binary changes (does not consume the slot yet)
            # This allows us to apply to sinks safely before acknowledging
            peek_sql = f"""
                SELECT lsn::text, xid, data 
                FROM pg_logical_slot_peek_binary_changes(
                    '{REPLICATION_SLOT}', NULL, 100, 
                    'proto_version', '1', 
                    'publication_names', '{PUBLICATION}'
                );
            """
            cur.execute(peek_sql)
            rows = cur.fetchall()
            if not rows:
                time.sleep(1.0) # sleep if no changes
                continue

            max_lsn = None

            for row in rows:
                lsn, xid, raw_data = row
                
                # raw_data is a memoryview, convert to bytes
                payload = raw_data.tobytes()

                # Decode using our pgoutput decoder
                print(f"Raw message received (len: {len(payload)}) at {lsn}")
                event = decoder.decode(payload, str(lsn))

                if event is not None:
                    print(f"Processing {event.op.upper()} on {event.schema}.{event.table}")
                    # Apply to Postgres Sink
                    try:
                        sink_postgres.apply(event)
                    except Exception as e:
                        print(f"Postgres Sink error: {e}")
                    
                    # Apply to File Sink
                    try:
                        sink_file.apply(event)
                    except Exception as e:
                        print(f"File Sink error: {e}")

                max_lsn = lsn

            else:
                # If the for loop did NOT break (meaning everything was applied successfully)
                # We can officially advance the replication slot on the server to `max_lsn`
                if max_lsn:
                    consume_sql = f"SELECT pg_replication_slot_advance('{REPLICATION_SLOT}', '{max_lsn}');"
                    cur.execute(consume_sql)
                    save_lsn(max_lsn)

        # Sleep a small amount before next poll
        time.sleep(0.5)

if __name__ == '__main__':
    MODE="cdc"
    args = parse_args()
    MODE = args.mode

    print(f"Running in mode: {MODE}")
    if MODE=="cdc":
        while True:
            try:
                run()
            except KeyboardInterrupt:
                print("Stopped by user")
                break
            except Exception as e:
                print(f"Connection lost or error: {e}. Reconnecting in 5s...")
                time.sleep(5)
    else:
        test_polling.run()
        
