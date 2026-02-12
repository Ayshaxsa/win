import streamlit as st
import av
import cv2
import mediapipe as mp
import numpy as np
import math
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

st.title("Hand Gesture Volume Control (Web Demo)")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class HandVolumeProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.7)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)

        h, w, _ = img.shape
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark

                x1 = int(landmarks[8].x * w)
                y1 = int(landmarks[8].y * h)

                x2 = int(landmarks[4].x * w)
                y2 = int(landmarks[4].y * h)

                cv2.circle(img, (x1, y1), 8, (0, 255, 255), -1)
                cv2.circle(img, (x2, y2), 8, (0, 0, 255), -1)

                distance = math.hypot(x2 - x1, y2 - y1)
                volume_percent = int((distance / 200) * 100)
                volume_percent = max(0, min(100, volume_percent))

                cv2.putText(
                    img,
                    f"Volume: {volume_percent}%",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="hand-volume",
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=HandVolumeProcessor,
)
