import cv2 as cv




CAP = cv.VideoCapture('srrec.mp4')
def ChangeRes(width, height):
    CAP.set(3, width)
    CAP.set(4, height)
ChangeRes(1280, 720)

while True:
    isTrue, frame = CAP.read()
    cv.imshow('Video', frame)
    

    if cv.waitKey(20) & 0xFF == ord('d'):
        break
CAP.release()
cv.destroyAllWindows()
