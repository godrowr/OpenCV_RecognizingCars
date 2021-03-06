import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import imutils
import time

# 12.png sort of
plate_cascade = cv2.CascadeClassifier("cascade.xml")

russian_plate_number_cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

path = "LicenseImages/12"
algo = ".png"
videopath = 'testdriverussia.mp4'
imgOriginal  = cv2.imread(path + algo) #suzuki_car.jpeg  10.png

img = imgOriginal.copy()


# This method cleans the license plate and obtains the colour information. 
def clean_license(plate_number, img, method):
	print(plate_number)
	for (x, y, w, h) in plate_number:
		(x1, y1) = (np.min(x), np.min(y))
		(x2, y2) = (np.max(x), np.max(y))
		colour = img[x1:x2+1, y2:y2+1]
		cv2.imshow('colour', colour)
		if method == "haar":
			a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
			plate = img[y+a:y+h-a, x+b:x+w-b, :] #+a -a +b -b
		else:
			plate = img[y:y+h, x:x+w, :]
		k = np.ones((1,1),np.int8)
		plate = cv2.dilate(plate,k,iterations=1)
		plate = cv2.erode(plate,k, iterations=1)
		plate = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
		cv2.imshow('plate', plate)
		cv2.imwrite(path + "_plate" + algo, plate)


#This method starts the video and 	
def haar_video_detect(cascade):
	cap = cv2.VideoCapture(videopath)
	count = 0
	x_start = 0
	y_start = 0
	detected = 0
	while(cap.isOpened()):
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		plate_number = cascade.detectMultiScale(gray, 1.3, 5)
		print(plate_number)
		for (x, y, w, h) in plate_number:
			cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
			if count == 1:
				detected = 1
				x_start = x
				y_start = y
			count = count + 1
		cv2.imshow('frame',frame)
		
		if detected == 1 and not any(map(len, plate_number)) or cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.rectangle(frame, (x_start, y_start), (x_start+w, y_start+h), (255,0,0), 2)
			cv2.line(frame, (x_start, y_start), (x, y), (0, 0, 255), 2)
			cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
			cv2.imshow('frame',frame)
			cv2.imwrite("testdriverussia_plate" + algo, frame)
			#clean_license(plate_number, frame, "video")
			return plate_number,frame
	

def haar_image_detect(imgGray, cascade):
	plate_number = cascade.detectMultiScale(imgGray, 1.3, 5)

	for (x, y, w, h) in plate_number:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = imgGray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		clean_license(plate_number, img, "haar")
		cv2.imshow('img', img)


def convert_to_xywh(plate_number):
	min_x = 0
	min_y = 0
	max_x = 0
	max_y = 0
	count = 0
	for tupl in plate_number:
		for point in tupl:
			x = point[0]
			y = point[1]
			if count ==0:
				min_x = x
				min_y = y
				max_x = x
				max_y = y
			else:
				if x < min_x:
					min_x = x
				elif x > max_x:
					max_x = x
				if y < min_y:
					min_y = y
				elif y > max_y:
					max_y = y
			count = count + 1	
	w = max_x - min_x 
	h = max_y - min_y 
	return [min_x, min_y, w, h]

# Not implemented fully!
def hough_image_detect(imgGray):
	bfilter = cv2.bilateralFilter(imgGray, 25,25,25) #11 17 17
	imgEdged = cv2.Canny(bfilter, 30, 200)	
	lines = cv2.HoughLines(imgEdged,1,np.pi/180,200)
	for line in lines:
	    rho,theta = line[0]
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))
	    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
	
	lines = cv2.HoughLinesP(imgEdged,1,np.pi/180,100,minLineLength=20,maxLineGap=20)
	for line in lines:
    		x1,y1,x2,y2 = line[0]
    		if x2 - x1 > 50 and y2 - y1 < 1:
    			cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	    
	cv2.imshow("imgEdged-hough", img)
	cv2.imwrite(path + "_imgEdged-hough" + algo, img)	
	
	
	
def contour_image_detect(imgGray):
	plate_number = [] 

	bfilter = cv2.bilateralFilter(imgGray, 25,25,25) #11 17 17
	imgEdged = cv2.Canny(bfilter, 30, 200)	

	cv2.imshow("imgEdged", imgEdged)
	cv2.imwrite(path + "_imgEdged" + algo, imgEdged)
	
	keypoints = cv2.findContours(imgEdged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	contours = imutils.grab_contours(keypoints)
	possible_plate_contours = sorted(contours, key=cv2.contourArea,reverse=True)

	location = None
	for contour in possible_plate_contours:
		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 5, True)[:10]
		if len(approx) == 4:
			location = approx
			plate_number.append(location)
			break
			
	mask = np.zeros(imgGray.shape, np.uint8)
	new_plate_number = []	
	for p in plate_number:
		plate = convert_to_xywh(p)
		print(plate)
		if plate[2] > 20 and plate[3] > 20:
			new_plate_number = []
			new_plate_number.append(plate)
			cv2.imshow('img', img)
			clean_license(new_plate_number, img, "contour")
	#print(new_plate_number)
	#clean_license(new_plate_number, img, "contour")
	
	#clean_license(plate_number, img, "contour")
	#cv2.imshow('img', img)
	
def main():
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	haar_image_detect(imgGray,plate_cascade)
	#plate, frame  = haar_video_detect(russian_plate_number_cascade)
	#contour_image_detect(imgGray)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
main()
