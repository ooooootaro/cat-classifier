from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import uvicorn
import os
from pathlib import Path

app = FastAPI()

# Get the absolute path to the model file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "model", "yolov11m-cls.pt")

# Load the YOLO model at startup
try:
    model = YOLO(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your Vercel URL here for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cat Classifier API",
        "model_path": str(MODEL_PATH),
        "model_exists": os.path.exists(MODEL_PATH)
    }

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Read and convert image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Run inference with YOLO model
        results = model(image)
        
        # Get the top prediction
        predicted_breed = results[0].names[results[0].probs.top1]
        confidence = float(results[0].probs.top1conf)
        
        # Return prediction
        return {
            "breed": predicted_breed,
            "confidence": confidence
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")  # Add server-side logging
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)