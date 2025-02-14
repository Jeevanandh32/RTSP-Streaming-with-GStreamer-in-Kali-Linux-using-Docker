# Base Image: Use Kali Linux with Python and GStreamer
FROM kalilinux/kali-rolling

# Set Environment Variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Dependencies
RUN apt update && apt install -y \
    python3 python3-gi python3-gi-cairo \
    gstreamer1.0-rtsp gstreamer1.0-tools \
    gstreamer1.0-python3-plugin-loader \
    libgstrtspserver-1.0-0 gir1.2-gst-rtsp-server-1.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy RTSP Server Script into Container
COPY rtsp_server.py /app/rtsp_server.py

# Set Work Directory
WORKDIR /app

# Expose RTSP Port
EXPOSE 8554

# Run RTSP Server
CMD ["python3", "rtsp_server.py"]
