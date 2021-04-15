import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import imutils
import time


def main():

    #TODO Works with: 
    #"LicenseImages/ontario_car.jpeg"
    #"LicenseImages/2.png"
    #"LicenseImages/3.png"
    #"LicenseImages/10.png"

    #TODO DOesn't work with: 
    #"LicenseImages/mountain_car.jpeg" #Need to clear out clutter, remove background
    #"LicenseImages/ny_car.jpeg"
    #"LicenseImages/ontario_car2.jpeg" #Need to clear out clutter
    #"LicenseImages/1.png"
    #"LicenseImages/4.png" Need to fix find contors to find more boxes
    #"LicenseImages/5.png"
    #"LicenseImages/6.png
    #"LicenseImages/8.png"
    #"LicenseImages/7.png" Only gets one character
    #"LicenseImages/9.png"
    #"LicenseImages/12.png"
    #"LicenseImages/delorean_car.jpeg"
    imgOriginalScene  = cv2.imread("LicenseImages/delorean_car.jpeg")

    listOfPossiblePlates = [] 

    height, width, numChannels = imgOriginalScene.shape

    imgHSV = cv2.cvtColor(imgOriginalScene, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgGrayscale  = cv2.split(imgHSV)
    
    cv2.namedWindow("imgOriginalScene", cv2.WINDOW_NORMAL)    
    cv2.imshow("imgOriginalScene", imgGrayscale)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgMaxContrastGrayscale  = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, (5, 5), 0)

    imgThreshScene = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,19, 9)

    cv2.namedWindow("imgOriginalScene", cv2.WINDOW_NORMAL)
    cv2.namedWindow("imgThreshScene", cv2.WINDOW_NORMAL)
    cv2.imshow("imgOriginalScene", imgOriginalScene)
    cv2.imshow("imgThreshScene", imgThreshScene)

    # TODO Edge Detection
    # TODO REMOVE CLUTTER FROM PICTURE
    bfilter = cv2.bilateralFilter(imgThreshScene, 25,25,25) #11 17 17
    imgEdged = cv2.Canny(bfilter, 30, 200)
    cv2.namedWindow("imgEdged", cv2.WINDOW_NORMAL)    
    cv2.imshow("imgEdged", imgEdged)
    
    

    # TODO IMPROVE CONTOURS
    keypoints = cv2.findContours(imgEdged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            listOfPossiblePlates.append(location)

    print(listOfPossiblePlates)
    
    mask = np.zeros(imgGrayscale.shape, np.uint8)
    i = 0
    for possiblePlate in listOfPossiblePlates:
        imgPlate = cv2.drawContours(mask, [possiblePlate], 0, 255, -1)
        imgPlate = cv2.bitwise_and(imgOriginalScene ,imgOriginalScene, mask=mask)
        cv2.namedWindow(str(i), cv2.WINDOW_NORMAL)    
        cv2.imshow(str(i), imgPlate)
        i = i + 1
    
    # TODO OCR.
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for i in range (1,5):
        cv2.waitKey(1)


main()

