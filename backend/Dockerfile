FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn psutil

# Create model directory
RUN mkdir -p /app/model

# Copy the minimal app
COPY ./minimal_app.py /app/

# For testing purposes, create a dummy model file
RUN dd if=/dev/zero of=/app/model/yolov11m-cls.pt bs=1M count=1

# Add debug information
RUN ls -la /app && ls -la /app/model

# Reduce memory usage
ENV MALLOC_ARENA_MAX=2

# Start the app
CMD bash -c "uvicorn minimal_app:app --host 0.0.0.0 --port=\$PORT --workers=1"