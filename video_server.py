import cv2
import socket
import struct
import time

# Constants
RTP_PORT = 5005
RTSP_PORT = 5544
BUFFER_SIZE = 2048
PAYLOAD_TYPE = 26  # Example: MJPEG
FPS = 30  # Frames per second

# RTP Header Construction
def create_rtp_header(sequence_number, timestamp, ssrc=12345):
    header = struct.pack('!BBHII', 0x80, PAYLOAD_TYPE, sequence_number, timestamp, ssrc)
    return header

def video_server(video_file):
    # Open video file
    video_file_path = "video.mp4"
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return
    
    # RTP socket
    rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp_client_address = None

    # RTSP socket
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind(('', RTSP_PORT))
    rtsp_socket.listen(1)
    print(f"RTSP Server listening on port {RTSP_PORT}...")

    conn, addr = rtsp_socket.accept()
    print(f"RTSP Client connected from {addr}")

    sequence_number = 0
    ssrc = 12345
    streaming = False

    try:
        while True:
            # Handle RTSP commands
            rtsp_request = conn.recv(BUFFER_SIZE).decode()
            if "PLAY" in rtsp_request:
                streaming = True
                print("Received RTSP PLAY command.")
                conn.send(b"RTSP/1.0 200 OK\r\n")
            elif "PAUSE" in rtsp_request:
                streaming = False
                print("Received RTSP PAUSE command.")
                conn.send(b"RTSP/1.0 200 OK\r\n")
            elif "SETUP" in rtsp_request:
                # Extract client RTP port
                rtp_client_address = addr[0]
                print(f"Setup RTP for client at {rtp_client_address}:{RTP_PORT}")
                conn.send(b"RTSP/1.0 200 OK\r\n")
            elif "TEARDOWN" in rtsp_request:
                print("Received RTSP TEARDOWN command.")
                conn.send(b"RTSP/1.0 200 OK\r\n")
                break

            # Stream video frames
            if streaming and rtp_client_address:
                ret, frame = cap.read()
                if not ret:
                    print("End of video stream.")
                    break
                
                # Encode frame as JPEG
                _, encoded_frame = cv2.imencode('.jpg', frame)
                frame_data = encoded_frame.tobytes()
                
                # Add RTP header
                timestamp = int(time.time() * 1000)
                rtp_packet = create_rtp_header(sequence_number, timestamp, ssrc) + frame_data
                
                # Send RTP packet to client
                rtp_socket.sendto(rtp_packet, (rtp_client_address, RTP_PORT))
                
                # Increment sequence number
                sequence_number += 1
                
                # Control streaming rate
                time.sleep(1 / FPS)
    finally:
        cap.release()
        rtp_socket.close()
        rtsp_socket.close()

if __name__ == "__main__":
    video_file_path = "sample_video.mp4"  # Replace with your video file path
    video_server(video_file_path)
