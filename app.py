import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math

st.title("Hand Gesture Volume Control (Demo Version)")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

while run:
    ret, frame = camera.read()
    if not ret:
        st.write("Camera not detected")
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            x1 = int(landmarks[8].x * w)
            y1 = int(landmarks[8].y * h)

            x2 = int(landmarks[4].x * w)
            y2 = int(landmarks[4].y * h)

            distance = math.hypot(x2 - x1, y2 - y1)

            volume_percent = int((distance / 200) * 100)
            volume_percent = max(0, min(100, volume_percent))

            st.write(f"Volume Level: {volume_percent}%")

    FRAME_WINDOW.image(frame, channels="BGR")

camera.release()
