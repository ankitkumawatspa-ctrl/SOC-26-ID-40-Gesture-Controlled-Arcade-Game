import cv2 as cv
import mediapipe as mp  
import time

import handtraackingmodule as htm

pTime=0
cTime=0
cap= cv.VideoCapture(0)
detector = htm.handDetector()
while True:
    isTrue, frame = cap.read()
    img = detector.findHands(frame)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])
    

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv.imshow('Video', img)

    ref= detector.findDistance(0,9,img, draw = False)
    


    if cv.waitKey(20) & 0xFF == ord('d'):
        break
cap.realease()
cv.destroyAllWindows()
 