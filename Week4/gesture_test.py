import cv2 as cv
import mediapipe as mp
import gestures_module as gs
cap = cv.VideoCapture(0)
detector= gs.handDetector()

while True:
    isTrue, frame= cap.read()
    frame= cv.flip(frame ,1 )
    frame= detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    #pinch gesture
    a= detector.normalised_distance(4,8,frame)
    #if a <0.3:
        #cv.putText(frame, "Pinch",(20, 250),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    handType = detector.findHandType()

    if handType:
        cv.putText(frame, detector.findHandType(),(500, 450),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 255),2)

    if len(lmList) != 0:

        fingers = detector.fingers_up(frame)

        gesture = detector.classify_gesture(fingers)
        


        if a<0.3 and  fingers[2]  and  fingers[3] and fingers [4]:
            cv.putText(frame, "OK",(20, 250),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
        if detector.thumbs_up(frame):
            cv.putText(frame,"THUMBS UP",(20, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv.putText(frame, gesture,(20, 250),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)

    
    

    

    
    
    cv.imshow('frame',frame)




    if cv.waitKey(20) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows()  





