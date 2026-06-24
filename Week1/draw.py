import cv2 as cv
import numpy as np
blank = np.zeros((500, 500,3), dtype='uint8')

blank[:] = 0,255,0

blank[200:300, 100:400] = 0,0,255


#cv.rectangle(blank, (0,0), (250,250), (255,0,0), thickness= -1) 
cv.rectangle(blank, (0,0), (blank.shape[1]//2, blank.shape[0]//2), (255,0,0), thickness= -1)

cv.circle(blank , (250,250), 100, (0,0,0), thickness= 10)

cv.line(blank, (0,0) ,(blank.shape[1]//2, blank.shape[0]//2), (255,255,255), thickness= 5)

cv.putText(blank, 'hello ankit ji ,how u doing', (50,255),cv.FONT_HERSHEY_TRIPLEX, 0.75, (255,255,255), thickness= 2)
cv.imshow('Blank', blank)  
cv.waitKey(0)

 