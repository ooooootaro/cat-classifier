from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import os
from pathlib import Path
import gc

app = FastAPI()

# Get model path from environment variable
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/yolov11m-cls.pt")
print(f"Using model path: {MODEL_PATH}")

# Don't load model immediately
model = None

def get_model():
    global model
    if model is None:
        try:
            print(f"Loading model from: {MODEL_PATH}")
            print(f"Model file exists: {os.path.exists(MODEL_PATH)}")
            model = YOLO(MODEL_PATH)
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

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cat Classifier API",
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "allowed_origins": ALLOWED_ORIGINS
    }

# Add this new route here
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": {
            "model_path": MODEL_PATH,
            "model_exists": os.path.exists(MODEL_PATH),
            "cwd": os.getcwd(),
            "files_in_model_dir": os.listdir(os.path.dirname(MODEL_PATH)) if os.path.exists(os.path.dirname(MODEL_PATH)) else []
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