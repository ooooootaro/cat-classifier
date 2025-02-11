import React, { useState } from 'react';
import { Camera, Upload, RefreshCw } from 'lucide-react';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedImage(file);
        setPreview(URL.createObjectURL(file));
        setPrediction(null);
        setError(null);
      } else {
        setError('请选择图片文件');
      }
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;
    
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('识别请求失败');
      }

      const data = await response.json();
      
      // Handle potential error response
      if (data.error) {
        throw new Error(data.error);
      }

      setPrediction({
        breed: data.breed,
        confidence: data.confidence // YOLO model returns confidence as decimal
      });
    } catch (error) {
      console.error('Error:', error);
      setError('识别过程中出现错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto p-6 space-y-6">
        <h1 className="text-3xl font-bold text-center mb-8">猫咪品种识别</h1>
        
        <div className="space-y-4">
          <div className="flex justify-center">
            <label className="flex flex-col items-center p-6 bg-white border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
              <Camera className="w-12 h-12 text-gray-400" />
              <span className="mt-2 text-sm text-gray-500">点击上传猫咪图片</span>
              <input
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleImageChange}
              />
            </label>
          </div>

          {error && (
            <div className="p-4 text-red-700 bg-red-100 rounded-lg">
              {error}
            </div>
          )}

          {preview && (
            <div className="flex justify-center">
              <img
                src={preview}
                alt="Preview"
                className="max-w-full h-64 object-contain rounded-lg shadow-lg"
              />
            </div>
          )}

          <div className="flex justify-center">
            <button
              onClick={handleSubmit}
              disabled={!selectedImage || loading}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <RefreshCw className="w-5 h-5 animate-spin" />
              ) : (
                <Upload className="w-5 h-5" />
              )}
              {loading ? '识别中...' : '开始识别'}
            </button>
          </div>

          {prediction && (
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold mb-4">识别结果</h2>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="font-medium">{prediction.breed}</span>
                <div className="flex items-center">
                  <div className="w-32 h-2 bg-gray-200 rounded-full mr-3">
                    <div 
                      className="h-full bg-blue-600 rounded-full"
                      style={{ width: `${prediction.confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-gray-600 w-16 text-right">
                    {(prediction.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;