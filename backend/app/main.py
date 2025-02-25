from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import os
from pathlib import Path
import gc

app = FastAPI()

# Better path handling
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "model" / "yolov11m-cls.pt"))

print(f"Current working directory: {os.getcwd()}")
print(f"Base directory: {BASE_DIR}")
print(f"Model path: {MODEL_PATH}")
print(f"Model exists: {os.path.exists(MODEL_PATH)}")

# Load model only when needed
model = None

def get_model():
    global model
    if model is None:
        try:
            # Try both paths
            if os.path.exists(MODEL_PATH):
                model = YOLO(MODEL_PATH)
            else:
                # Try relative path as fallback
                fallback_path = str(BASE_DIR / "model" / "yolov11m-cls.pt")
                print(f"Trying fallback path: {fallback_path}")
                model = YOLO(fallback_path)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return model

# CORS settings - Get from environment variable
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
print(f"Allowed origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this to your main.py file

@app.get("/debug-model-path")
async def debug_model_path():
    model_path = os.getenv("MODEL_PATH", "Not set")
    return {
        "model_path": model_path,
        "model_exists": os.path.exists(model_path) if model_path != "Not set" else False,
        "directory_contents": {
            "/": os.listdir("/") if os.path.exists("/") else "Not accessible",
            "/app": os.listdir("/app") if os.path.exists("/app") else "Not accessible",
            "/app/model": os.listdir("/app/model") if os.path.exists("/app/model") else "Not accessible",
        }
    }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cat Classifier API",
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "allowed_origins": ALLOWED_ORIGINS
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "debug_info": {
            "cwd": os.getcwd(),
            "base_dir": str(BASE_DIR),
            "model_path": MODEL_PATH,
            "model_exists": os.path.exists(MODEL_PATH),
            "directory_contents": os.listdir(str(BASE_DIR)),
            "model_dir_contents": os.listdir(str(BASE_DIR / "model")) if os.path.exists(str(BASE_DIR / "model")) else []
        }
    }


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Load model only when needed
        model = get_model()
        
        # Read and convert image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Run inference
        results = model(image)
        
        # Get prediction
        predicted_breed = results[0].names[results[0].probs.top1]
        confidence = float(results[0].probs.top1conf)
        
        # Clean up memory
        del results
        gc.collect()
        
        return {
            "breed": predicted_breed,
            "confidence": confidence
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)