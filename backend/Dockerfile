FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY ./minimal_requirements.txt /app/
RUN pip install --no-cache-dir -r minimal_requirements.txt

# Create model directory
RUN mkdir -p /app/model

# Copy the minimal app
COPY ./minimal_app.py /app/

# Copy startup script
COPY ./startup.sh /app/
RUN chmod +x /app/startup.sh

# For testing purposes, create a dummy model file
RUN dd if=/dev/zero of=/app/model/yolov11m-cls.pt bs=1M count=1

# Add debug information
RUN ls -la /app && ls -la /app/model

# Reduce memory usage
ENV MALLOC_ARENA_MAX=2

# Start the app using the bash script
CMD ["/app/startup.sh"]