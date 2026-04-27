import json
from datetime import datetime, timezone
from config import JSONL_PATH
from decoder import ChangeEvent

def apply(event: ChangeEvent):
    """
    Appends a change event to a JSONL file.
    Each line is a complete, self-contained JSON record.
    JSONL is perfect for audit logs — easy to tail, grep, and stream.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "op":        event.op,
        "schema":    event.schema,
        "table":     event.table,
        "lsn":       event.lsn,
        "data":      event.data,
        "old_data":  event.old_data,
    }

    with open(JSONL_PATH, 'a') as f:
        f.write(json.dumps(record) + '\n')