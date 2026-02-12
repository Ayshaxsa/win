import streamlit as st
import av
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

st.title("Hand Volume Control - Cloud Demo")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)

        cv2.putText(
            img,
            "Webcam Running Successfully!",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="demo",
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=VideoProcessor,
)
