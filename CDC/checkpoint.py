import os
import json

CHECKPOINT_FILE = "./checkpoint.json"

def save_lsn(lsn: str):
    """Save the last successfully processed LSN to disk."""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({"lsn": lsn}, f)

def load_lsn() -> str | None:
    """Load the last LSN on startup. None means start from now."""
    if not os.path.exists(CHECKPOINT_FILE):
        return None
    with open(CHECKPOINT_FILE, 'r') as f:
        data = json.load(f)
        return data.get("lsn")