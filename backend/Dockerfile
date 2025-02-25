FROM python:3.9-slim

WORKDIR /app

# Print working directory for debugging
RUN pwd && ls -la

# Copy requirements first for better caching
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory
RUN mkdir -p /app/model

# Copy the model file separately and explicitly 
COPY ./app/model/yolov11m-cls.pt /app/model/
RUN ls -la /app/model

# Copy the rest of the app
COPY ./app /app/
COPY ./railway.py /app/

# Add debug information
RUN ls -la /app && ls -la /app/model

# Use environment variables
ENV MODEL_PATH=/app/model/yolov11m-cls.pt
ENV MALLOC_ARENA_MAX=2

# Reduce worker count and concurrency for memory constraints
CMD ["python", "railway.py"]