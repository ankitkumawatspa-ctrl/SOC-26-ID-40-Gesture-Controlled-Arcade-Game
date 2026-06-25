import math
import numpy as np

import cv2 as cv
import mediapipe as mp
import time

import gestures_module as htm
from pycaw.pycaw import AudioUtilities
cap= cv.VideoCapture(0 )
detector = htm.handDetector(detectionCon=0.75)
ptime=0

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
print(f"Audio output: {device.FriendlyName}")
#print(f"- Muted: {bool(volume.GetMute())}")
#print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
#print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
volrange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-5.0, None)
minVol= volrange[0]
maxVol= volrange[1]
volBAR=400
while True:
    isTrue, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame= detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    if lmList != []:
        #print(lmList[4], lmList[8])
        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cv.circle(frame,(x1,y1), 7, (255 ,0,0), cv.FILLED)
        cv.circle(frame,(x2,y2), 7, (255,0,0), cv.FILLED)
        cv.line(frame, (x1,y1), (x2,y2), (255,0,255), 3)
        cx,cy= (x1+x2)//2, (y1+y2)//2
        cv.circle(frame,(cx,cy), 7, (0,0,255), cv.FILLED)
        len= math.hypot(x2-x1, y2-y1)
        #print(len)
        # hand range = 50 - 300
        # volume range = -65 - 0
        vol= np.interp(len, [50,300], [minVol, maxVol])
        volBAR= np.interp(len, [50,300], [400,150])
        volume.SetMasterVolumeLevel(vol, None)
        if len<50:
            cv.circle(frame,(cx,cy), 7, (0,255,0), cv.FILLED)
    cv.rectangle(frame, (50,150), (85,400), (0,0,0), 3)
    cv.rectangle(frame, (50,int(volBAR)), (85,400), (0,255,0), cv.FILLED)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv.imshow('Volume_gesture_control', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break   
cap.release()
cv.destroyAllWindows()  