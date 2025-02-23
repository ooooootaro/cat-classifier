FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory
RUN mkdir -p /app/model

# Copy the entire app directory, including the model
COPY ./app /app/

# Debug information
RUN ls -la /app && ls -la /app/model

# Use environment variables from Railway
ENV MODEL_PATH=/app/model/yolov11m-cls.pt

# Reduce memory usage
ENV MALLOC_ARENA_MAX=2

# Use minimal resources
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "1", "--limit-concurrency", "1"]