import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPServer:
    def __init__(self):
        Gst.init(None)
        self.server = GstRtspServer.RTSPServer.new()
        self.factory = GstRtspServer.RTSPMediaFactory.new()
        self.factory.set_launch(
            "( filesrc location=/app/video.mp4 ! decodebin ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency "
            "! rtph264pay name=pay0 pt=96 )"
        )
        self.factory.set_shared(True)
        self.server.get_mount_points().add_factory("/stream", self.factory)
        self.server.attach(None)
        print("RTSP Streaming Server started at rtsp://0.0.0.0:8554/stream")

if __name__ == "__main__":
    loop = GObject.MainLoop()
    server = RTSPServer()
    loop.run()

