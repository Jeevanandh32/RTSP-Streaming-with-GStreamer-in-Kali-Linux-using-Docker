# RTSP Streaming with GStreamer in Docker (Kali Linux)

This guide explains how to set up an RTSP streaming server using Docker with GStreamer on Kali Linux. The containerized solution ensures consistency and avoids dependency issues.

**1. Install Docker (If Not Installed)**
Before setting up the RTSP server, install Docker on Kali Linux:
    bash
    sudo apt update
    sudo apt install -y docker.io
Enable and start the Docker service:
     bash
     sudo systemctl enable docker
     sudo systemctl start docker
Verify Docker installation:
     bash
     docker --version

**2. Understanding the Docker Setup**
The repository contains:

Dockerfile – Defines how the container is built.
rtsp_server.py – A Python script that sets up the RTSP server.
video.mp4 – A sample video file for streaming.
How the Dockerfile Works
Uses Kali Linux as the base image.
Installs GStreamer RTSP plugins and Python.
Copies the RTSP server script into the container.
Exposes port 8554 for streaming.
Runs the Python RTSP server script on startup.
How rtsp_server.py Works
Uses GStreamer and Python to create an RTSP server.
Streams a pre-recorded video file (video.mp4).
Binds to port 8554, allowing clients to connect.

**3. Building and Running the Docker Container**
Navigate to the repository folder:

cd rtsp_gstreamer

Build the Docker Image

docker build -t rtsp-gstreamer .

Run the RTSP Server

docker run -it --rm -p 8554:8554 rtsp-gstreamer

If successful, you should see:

arduino
RTSP Streaming Server started at rtsp://0.0.0.0:8554/stream

**4. Playing the RTSP Stream**

Instead of VLC, use GStreamer to receive the RTSP stream.
gst-launch-1.0 -v rtspsrc location=rtsp://127.0.0.1:8554/stream ! decodebin ! videoconvert ! autovideosink

This command:

Connects to the RTSP server at 127.0.0.1:8554.
Decodes the video and renders it on screen.

**5. Running the Server in Detached Mode**
To keep the RTSP server running in the background, use:

docker run -d -p 8554:8554 rtsp-gstreamer

List running containers:

docker ps

To stop the container:

docker stop <container_id>

**6. Debugging and Troubleshooting**

1. Check if the RTSP Server is Running

ps aux | grep python
If the process is not found, restart the container.

2. Verify Port 8554 is Open

ss -tulnp | grep 8554
If the port is not listed, the server is not running correctly.

3. Restart the RTSP Server in Debug Mode

GST_DEBUG=3 python3 rtsp_server.py
This provides detailed logs.

4. Restart Docker Container

docker restart <container_id>

**7. Cleaning Up Docker**
1. To stop all running containers:

docker stop $(docker ps -aq)

2. To remove the image:

docker rmi rtsp-gstreamer

3. Create the RTSP Server Script
Run:
nano rtsp_server.py

4. Add a Video File
Place a sample video file (video.mp4) in the directory:

cp /path/to/your/video.mp4 rtsp_gstreamer/video.mp4
If you don't have a video, download a sample file:

wget -O rtsp_gstreamer/video.mp4 https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4

Navigate to your project directory:

cd rtsp_gstreamer

5. Build the Docker Image

docker build -t rtsp-gstreamer .

6. Run the RTSP Server

docker run -it --rm -p 8554:8554 rtsp-gstreamer

Expected output:

RTSP Streaming Server started at rtsp://0.0.0.0:8554/stream

7. Test the RTSP Stream
Once the container is running, open a new terminal and test the RTSP stream using GStreamer:
gst-launch-1.0 -v rtspsrc location=rtsp://127.0.0.1:8554/stream ! decodebin ! videoconvert ! autovideosink
This will receive and display the video stream from the Docker container.

8a. Run RTSP Server in Background (Detached Mode)
If you want the RTSP server to run in the background, start the container in detached mode:

docker run -d -p 8554:8554 rtsp-gstreamer

To list running containers, use:

docker ps

To stop the container, use:

docker stop <container_id>

### Challenges and Solutions
Challenge: Ensuring low latency and synchronized playback.
Solution: Optimized RTP packetization and transmission logic.
Challenge: Cross-platform deployment.
Solution: Dockerized the server for seamless setup and execution.

### Future Enhancements
Add support for live video streaming from webcams.
Implement adaptive bitrate streaming based on client bandwidth.

Troubleshooting
If the RTSP stream does not work, follow these steps:

1. Verify RTSP Server is Running
Check if the server process is active:

ps aux | grep python

If rtsp_server.py is not running, restart it:

python3 rtsp_server.py

2. Check If Port 8554 is Open
Run:

ss -tulnp | grep 8554
or

netstat -tulnp | grep 8554
If port 8554 is not listed, the RTSP server is not running properly.
If it's listed, retry the GStreamer client command.

3. Restart RTSP Server in Debug Mode
Run:

GST_DEBUG=3 python3 rtsp_server.py
This will show detailed logs of any errors.

4. Temporarily Disable Firewall (If Necessary)
If your firewall is blocking port 8554, disable it temporarily:

sudo ufw disable
Then retry streaming.

5. Ensure You Are Using the Correct Stream URL
When running GStreamer client, always use:

gst-launch-1.0 -v rtspsrc location=rtsp://127.0.0.1:8554/stream ! decodebin ! videoconvert ! autovideosink
If your server is on another machine, replace 127.0.0.1 with the server’s IP.

Final Checklist
✅ RTSP server is running (ps aux | grep python)
✅ Port 8554 is open (ss -tulnp | grep 8554)
✅ Try playing with GStreamer (gst-launch-1.0 ...)
✅ Run RTSP server in debug mode (GST_DEBUG=3 python3 rtsp_server.py)
✅ Temporarily disable firewall (sudo ufw disable)
✅ Use the correct RTSP URL (rtsp://127.0.0.1:8554/stream)
