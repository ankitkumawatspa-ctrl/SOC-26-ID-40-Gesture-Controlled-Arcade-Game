import cv2 as cv
import mediapipe as mp  
import time
cap= cv.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=4, min_detection_confidence=0.5)
mpDraw= mp.solutions.drawing_utils

pTime=0
cTime=0

def fingers_up(lmList):
    fingers = []

    # Thumb (for right hand with mirrored webcam)
    if lmList[4][1] > lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index, Middle, Ring, Pinky
    tipIds = [8, 12, 16, 20]

    for tip in tipIds:
        if lmList[tip][2] < lmList[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def classify_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    elif fingers == [1, 1, 1, 1, 1]:
        return "OPEN PALM"

    elif fingers == [0, 1, 0, 0, 0]:
        return "POINTING"

    elif fingers == [0, 1, 1, 0, 0]:
        return "PEACE"

    elif fingers == [1, 0, 0, 0, 0]:
        return "THUMBS UP"

    else:
        return "UNKNOWN"


while True:
    isTrue, frame = cap.read()
 

    
    framergb= cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = hands.process(framergb)
    
    #print(results.multi_hand_landmarks)
    lmList=[]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            
            for id, lm in enumerate(handLms.landmark):
                

                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
        
                #print(id, cx, cy)
                lmList.append([id , cx,cy])
                

            mpDraw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=4))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    ##gestures printing
    

    if len(lmList) != 0:

        fingers = fingers_up(lmList)

        gesture = classify_gesture(fingers)

        cv.putText(frame, gesture,(20, 250),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)

        print(fingers, gesture)
    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv.imshow('Video', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows()
 
