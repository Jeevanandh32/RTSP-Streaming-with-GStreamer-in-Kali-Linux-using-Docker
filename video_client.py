import socket
import struct

RTSP_SERVER_IP = '127.0.0.1'
RTSP_PORT = 5544
RTP_PORT = 5005
BUFFER_SIZE = 2048

def rtsp_client():
    # RTSP connection
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.connect((RTSP_SERVER_IP, RTSP_PORT))
    print("Connected to RTSP server.")

    # Send RTSP SETUP command
    rtsp_socket.send(b"SETUP RTP/UDP 5005\r\n")

    # RTP socket for receiving video
    rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp_socket.bind(('', RTP_PORT))

    try:
        # Send RTSP PLAY command
        rtsp_socket.send(b"PLAY\r\n")
        
        while True:
            # Receive RTP packet
            rtp_packet, _ = rtp_socket.recvfrom(BUFFER_SIZE)
            
            # Parse RTP header
            header = rtp_packet[:12]
            payload = rtp_packet[12:]
            
            # Extract sequence number and timestamp
            _, _, sequence_number, timestamp, _ = struct.unpack('!BBHII', header)
            print(f"Received RTP packet: Seq={sequence_number}, Timestamp={timestamp}")
            
            # Process payload (e.g., display video)
            with open("frame.jpg", "wb") as f:
                f.write(payload)
    except KeyboardInterrupt:
        print("Client interrupted.")
    finally:
        # Send RTSP PAUSE command
        rtsp_socket.send(b"PAUSE\r\n")
        rtp_socket.close()
        rtsp_socket.close()

if __name__ == "__main__":
    rtsp_client()
