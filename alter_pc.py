import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found in env")
    sys.exit(1)

DATABASE_URL = DATABASE_URL.replace("::", ":", 1) if "::" in DATABASE_URL else DATABASE_URL

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE production_charts ADD COLUMN IF NOT EXISTS machines JSONB DEFAULT '[]'::jsonb;"))
        conn.commit()
        print("Successfully added machines column to production_charts.")
    except Exception as e:
        print(f"Error: {e}")
