import cv2 as cv
img = cv.imread(r'D:\coding\opencv\ak.jpg')
cv.imshow('Ak', img)
def rescaleFrame(frame, scale=0.25):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
resized_image = rescaleFrame(img)
cv.imshow('Resized Ak', resized_image)

CAP = cv.VideoCapture('photos/srrec.mp4')
while True:
    isTrue, frame = CAP.read()
    frame_resized = rescaleFrame(frame)
    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break
CAP.release()
cv.destroyAllWindows()


