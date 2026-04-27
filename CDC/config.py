import os
from dotenv import load_dotenv

load_dotenv()

# Source (Supabase)
SOURCE_CONN = (
    f"host={os.getenv('SOURCE_HOST')} "
    f"port={os.getenv('SOURCE_PORT')} "
    f"dbname={os.getenv('SOURCE_DBNAME')} "
    f"user={os.getenv('SOURCE_USER')} "
    f"password={os.getenv('SOURCE_PASSWORD')}"
)

REPLICATION_SLOT = os.getenv("REPLICATION_SLOT")
PUBLICATION      = os.getenv("PUBLICATION")

# Sink (Local Postgres)
SINK_CONN = (
    f"host={os.getenv('SINK_HOST')} "
    f"port={os.getenv('SINK_PORT')} "
    f"dbname={os.getenv('SINK_DBNAME')} "
    f"user={os.getenv('SINK_USER')} "
    f"password={os.getenv('SINK_PASSWORD')}"
)

JSONL_PATH = os.getenv("JSONL_PATH", "./changes.jsonl")