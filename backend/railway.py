# railway.py
# Place this file at the root level of your backend directory

import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    sys.path.append("./app")  # Add app directory to path
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, workers=1)