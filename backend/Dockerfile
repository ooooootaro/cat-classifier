FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file
COPY ./model/yolov11m-cls.pt /app/model/yolov11m-cls.pt

# Copy the application code
COPY ./app /app/app

# Copy the model file
ENV MODEL_PATH=/app/model/yolov11m-cls.pt

# Let Railway handle the port
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]