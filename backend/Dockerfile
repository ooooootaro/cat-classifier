FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory which now includes the model
COPY ./app /app/app

# Set environment variables - update path to reflect new structure
ENV MODEL_PATH=/app/app/model/yolov11m-cls.pt

# Command with proper module path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]