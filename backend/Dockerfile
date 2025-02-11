FROM python:3.9

WORKDIR /app

# Copy requirements first
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and app code
COPY model/ model/
COPY app/ app/

ENV PORT=80
ENV MODEL_PATH=/app/model/yolov11m-cls.pt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]