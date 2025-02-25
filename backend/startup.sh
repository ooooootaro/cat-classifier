#!/bin/bash
# startup.sh - Direct startup script that handles PORT variable correctly

# Print environment variables for debugging
echo "Environment variables:"
echo "PORT: $PORT"
echo "MODEL_PATH: $MODEL_PATH"

# Start the application with explicit port
if [ -z "$PORT" ]; then
  echo "PORT is not set, using default 8000"
  exec uvicorn minimal_app:app --host 0.0.0.0 --port 8000 --workers 1
else
  echo "Starting app on port $PORT"
  exec uvicorn minimal_app:app --host 0.0.0.0 --port "$PORT" --workers 1
fi