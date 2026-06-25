import cv2 as cv
import mediapipe as mp  
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
    static_image_mode=self.mode,
    max_num_hands=self.maxHands,
    min_detection_confidence=self.detectionCon,
    min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        
        framergb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(framergb)
        #print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
                
        return img 
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        
        
        if self.results.multi_hand_landmarks:
            myhand =self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)#print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx,cy), 5, (255,0,0),cv.FILLED)
        return lmList
    def findDistance(self, p1, p2, img, draw=True):
        lmList = self.findPosition(img, draw=False)
        if len(lmList) < 2:
            return 0
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        if draw:
            cv.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
            cv.circle(img, (x1,y1), 5, (255,0,255), cv.FILLED)
            cv.circle(img, (x2,y2), 5, (255,0,255), cv.FILLED)
            cv.circle(img, (cx,cy), 5, (0,0,255), cv.FILLED)


        length = math.hypot(x2-x1, y2-y1)
        return length
    def fingers_up(self,img):
        lmList = self.findPosition(img, draw=False)
        if not lmList:
         return None
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


    def classify_gesture(self,fingers):
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
    
    
    
     

        
                
                

 
        



 
def main():
    pTime=0
    cTime=0
    cap= cv.VideoCapture(0)
    detector = handDetector()
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
        if cv.waitKey(20) & 0xFF == ord('d'):
            break

    
    
    cap.release()
    cv.destroyAllWindows()


      


 
if __name__ == "__main__":
    main()