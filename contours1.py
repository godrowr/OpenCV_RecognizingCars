import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from matplotlib import pyplot as plt

img = cv2.imread("Images/philly_car.jpeg",cv2.IMREAD_COLOR)
#img = imutils.resize(img, width=500 )
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
edged = cv2.Canny(gray, 170, 200) # 30  Perform Edge detection
cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:20] # CHANGE THIS NUMBER
cv2.drawContours(img, cnts, -1, (0,255,0), 3)

plt.imshow(img,'gray')
plt.show()


