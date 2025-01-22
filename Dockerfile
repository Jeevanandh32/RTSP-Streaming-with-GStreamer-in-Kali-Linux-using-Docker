# Base image
FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python script to container
COPY video_server.py /app/

# Install OpenCV and required Python libraries
RUN pip install opencv-python-headless

# Expose RTP and RTSP ports
EXPOSE 5005 5544

# Run the Python server
CMD ["python", "video_server.py"]
