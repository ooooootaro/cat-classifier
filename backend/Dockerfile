FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory which now includes the model
COPY ./app /app/app

# Set environment variables
ENV MODEL_PATH=/app/app/model/yolov11m-cls.pt
ENV PORT=8000

# Use shell form instead of exec form to properly expand environment variables
CMD uvicorn app.main:app --host=0.0.0.0 --port=$PORT