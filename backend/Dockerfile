FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file
COPY ./model/yolov11m-cls.pt /app/model/yolov11m-cls.pt

# Copy the application code
COPY ./app /app/app

# Set environment variables
ENV MODEL_PATH=/app/model/yolov11m-cls.pt

# Simple command without port handling
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]