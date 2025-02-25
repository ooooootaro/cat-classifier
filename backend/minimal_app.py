# minimal_app.py
import os
import sys
import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware setup
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/debug")
async def debug():
    # Get system information
    memory_info = psutil.virtual_memory()
    process = psutil.Process()
    process_memory = process.memory_info()
    
    # Check for model file
    model_path = os.getenv("MODEL_PATH", "/app/model/yolov11m-cls.pt")
    model_exists = os.path.exists(model_path)
    
    # List directories
    directories = {}
    for path in ["/", "/app", "/app/model"]:
        try:
            if os.path.exists(path):
                directories[path] = os.listdir(path)
            else:
                directories[path] = "Directory does not exist"
        except Exception as e:
            directories[path] = f"Error: {str(e)}"
    
    # Get environment variables
    env_vars = {
        "PORT": os.getenv("PORT", "Not set"),
        "MODEL_PATH": os.getenv("MODEL_PATH", "Not set"),
        "MALLOC_ARENA_MAX": os.getenv("MALLOC_ARENA_MAX", "Not set"),
        "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "Not set"),
        "PYTHONPATH": os.getenv("PYTHONPATH", "Not set")
    }
    
    return {
        "system": {
            "total_memory_mb": memory_info.total / (1024 * 1024),
            "available_memory_mb": memory_info.available / (1024 * 1024),
            "used_memory_percent": memory_info.percent,
        },
        "process": {
            "memory_rss_mb": process_memory.rss / (1024 * 1024),
            "memory_vms_mb": process_memory.vms / (1024 * 1024),
        },
        "model": {
            "path": model_path,
            "exists": model_exists,
            "size_mb": os.path.getsize(model_path) / (1024 * 1024) if model_exists else "N/A"
        },
        "directories": directories,
        "environment": env_vars
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("minimal_app:app", host="0.0.0.0", port=port, workers=1)