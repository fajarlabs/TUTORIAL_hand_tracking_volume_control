import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume 
currentVolumeDb = volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange())

################################
wCam, hCam = 1280, 720
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
 
detector = htm.handDetector(detectionCon=0.7, maxHands=1)

last_angle=None
last_length=None

minAngle = 0
maxAngle = 180
angle    = 0
angleBar = 400
angleDeg = 0
minHand  = 50 #50
maxHand  = 300 #300

last_volume = 0
deg_step = 180/50

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        print(lmList)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
 
        length = math.hypot(x2 - x1, y2 - y1)
 
        # Hand range 50 - 300
        angle  = np.interp(length, [minHand, maxHand], [minAngle, maxAngle])
        angleBar = np.interp(length, [minHand, maxHand], [400, 150])
        angleDeg = np.interp(length, [minHand, maxHand], [0, 180])   # degree angle 0 - 180

        maxVol = -62.25
        angleDegStep = maxVol / 180
        valVol = maxVol - (angleDeg * angleDegStep)        
        volume.SetMasterVolumeLevel(valVol, None)
        
        last_angle=angle
        last_length=length
 
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
 
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(angleBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(angleDeg)} deg', (40, 90), cv2.FONT_HERSHEY_COMPLEX,2, (0, 9, 255), 3)
 
    cv2.imshow("Img", img)
    cv2.waitKey(1)