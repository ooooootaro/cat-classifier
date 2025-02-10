from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from PIL import Image
import io

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React 开发服务器的地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Cat Classifier API"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # 读取上传的图片
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # TODO: 这里添加模型预测逻辑
    # 目前返回模拟数据
    mock_predictions = [
        {"breed": "白猫", "probability": 0.95},
        {"breed": "橘猫", "probability": 0.03},
        {"breed": "黑猫", "probability": 0.02},
    ]
    
    return {"predictions": mock_predictions}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)