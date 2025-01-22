# Real-Time Video Streaming Server (RTP/RTSP)

This project implements a real-time video streaming server using **RTP (Real-Time Transport Protocol)** and **RTSP (Real-Time Streaming Protocol)** in Python. The server is designed to stream video files to clients over the network, allowing for smooth, synchronized playback with minimal latency.

## Features
- **RTP Packetization**: Video frames are encapsulated into RTP packets with sequence numbers and timestamps for proper synchronization.
- **RTSP Command Handling**: Supports RTSP commands such as:
  - `SETUP`: Establishes the RTP connection.
  - `PLAY`: Starts streaming the video.
  - `PAUSE`: Temporarily halts video playback.
  - `TEARDOWN`: Ends the session.
- **Dockerized Deployment**: Runs in a Docker container for platform independence and easy deployment.
- **Client Compatibility**: Verified with VLC Media Player, FFplay, and Wireshark for accurate playback and network monitoring.

## Requirements
- Python 3.9 or higher
- OpenCV (`cv2`) library
- Docker (for containerized deployment)
- VLC Media Player or any RTSP-compatible client

## How to Run
### Using Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rtp-stream-server.git
   cd rtp-stream-server
2. Build the Docker image:
   ```bash
   docker build -t rtp_server .
3. Run the Docker container:
   ```bash
   docker run -it --rm -p 5544:5544 -p 5005:5005 -v $(pwd)/video.mp4:/home/kali/video.mp4 rtp_server
### Client
Open VLC Media Player or any RTSP-compatible client.
Enter the following URL in the "Open Network Stream" option:

    rtsp://<server-ip>:5544
### How It Works
The server reads the video file and splits it into frames using OpenCV.
Frames are encapsulated into RTP packets with sequence numbers and timestamps.
The RTSP server handles client commands for stream control (PLAY, PAUSE, etc.).
The server streams RTP packets over the network to the client for playback.

### Tools Used
Python: Core development language.
OpenCV: For video frame processing.
Docker: For containerization and deployment.
VLC Media Player: For client-side streaming.
Wireshark: For analyzing RTP/RTSP network traffic.
### Challenges and Solutions
Challenge: Ensuring low latency and synchronized playback.
Solution: Optimized RTP packetization and transmission logic.
Challenge: Cross-platform deployment.
Solution: Dockerized the server for seamless setup and execution.

### Future Enhancements
Add support for live video streaming from webcams.
Implement adaptive bitrate streaming based on client bandwidth.
