import streamlit as st
import cv2
import numpy as np

st.title("Hand Volume Control - Cloud Demo")

st.write("Full hand tracking works locally on Windows (hand_volume.py).")

run = st.checkbox("Start Webcam")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.write("No camera detected")
        break
    frame = cv2.flip(frame, 1)
    cv2.putText(
        frame,
        "Webcam Running",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    FRAME_WINDOW.image(frame, channels="BGR")

cap.release()
