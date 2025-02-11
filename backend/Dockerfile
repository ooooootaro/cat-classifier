FROM python:3.9

WORKDIR /app

# Copy requirements first
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory and copy model
RUN mkdir -p /app/model
COPY ../model/yolov11m-cls.pt model/yolov11m-cls.pt

# Copy app code
COPY app app/

ENV PORT=80
ENV MODEL_PATH=/app/model/yolov11m-cls.pt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]