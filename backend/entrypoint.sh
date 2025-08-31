#!/bin/sh
set -e

if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database to be ready... ($DATABASE_URL)"
  python - <<'PY'
import os, time, sys
from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL")
timeout = int(os.environ.get("DB_WAIT_TIMEOUT", "60"))
interval = float(os.environ.get("DB_WAIT_INTERVAL", "2"))

if not url:
    sys.exit(0)

start = time.time()
last_err = None
while True:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready.")
        break
    except Exception as e:
        last_err = e
        if time.time() - start > timeout:
            print(f"Database not ready after {timeout}s: {last_err}", file=sys.stderr)
            sys.exit(1)
        time.sleep(interval)
PY
fi

RUN_DB_INIT=${RUN_DB_INIT:-"true"}
if [ "$RUN_DB_INIT" = "true" ]; then
  echo "Running db_init and ingest..."
  python -m app.db_init
  python -m app.ingest
else
  echo "Skipping db_init and ingest (RUN_DB_INIT=$RUN_DB_INIT)"
fi

echo "Launching Gunicorn..."
exec gunicorn -c gunicorn.conf.py app.main:app


