FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory to match MODEL_PATH
RUN mkdir -p /app/model

# Copy the app directory
COPY ./app .

# Add debug information
RUN ls -la /app && ls -la /app/model

# Use environment variables from Railway
ENV MODEL_PATH=/app/model/yolov11m-cls.pt
# PORT is already set by Railway

# Use minimal resources
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "1"]