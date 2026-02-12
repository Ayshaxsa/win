import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ================= AUDIO SETUP =================

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = cast(interface, POINTER(IAudioEndpointVolume))

minVol, maxVol, _ = volume_interface.GetVolumeRange()

def set_volume(vol_percent):
    vol_percent = max(0, min(100, vol_percent))
    newVol = minVol + (vol_percent / 100) * (maxVol - minVol)
    volume_interface.SetMasterVolumeLevel(newVol, None)

# ================= HAND DETECTION =================

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, c = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            x1 = int(landmarks[8].x * w)
            y1 = int(landmarks[8].y * h)

            x2 = int(landmarks[4].x * w)
            y2 = int(landmarks[4].y * h)

            cv2.circle(img, (x1, y1), 10, (0, 255, 255), -1)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), -1)

            distance = math.hypot(x2 - x1, y2 - y1)

            volume_percent = int((distance / 200) * 100)
            volume_percent = max(0, min(100, volume_percent))

            set_volume(volume_percent)

            cv2.putText(img, f'Volume: {volume_percent}%',
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 3)

    cv2.imshow("Hand Volume Control - Windows", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
