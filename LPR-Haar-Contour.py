import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import imutils
import time

plate_cascade = cv2.CascadeClassifier("cascade.xml")

russian_plate_number_cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

licence_plate_rus_cascade = cv2.CascadeClassifier("haarcascade_licence_plate_rus_16stages.xml")

path = "LicenseImages/1"
algo = ".png"
videopath = 'testdriverussia.mp4'
imgOriginal  = cv2.imread(path + algo) #suzuki_car.jpeg  10.png

img = imgOriginal.copy()

def clean_license(plate_number, img, method):
	print(plate_number)
	for (x, y, w, h) in plate_number:
		(x1, y1) = (np.min(x), np.min(y))
		(x2, y2) = (np.max(x), np.max(y))
		colour = img[x1:x2+1, y2:y2+1] #Color inference??? 
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

#def haar_track_plate(start_plate_number, end_plate_number, start_frame, end_frame):
	

def haar_video_detect(cascade):
	cap = cv2.VideoCapture(videopath)
	count = 0
	start_plate_number = []
	end_plate_number = []
	while(cap.isOpened()):
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		plate_number = cascade.detectMultiScale(gray, 1.3, 5)
		print(plate_number)
		for (x, y, w, h) in plate_number:
			cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
			count = count + 1
		if count == 1:
			start_frame = frame
			start_plate_number = plate_number	
		cv2.imshow('frame',frame)
		end_frame = frame
		end_plate_number = plate_number
		if cv2.waitKey(1) & 0xFF == ord('q'):
			
			return start_plate_number, start_frame

def haar_image_detect(imgGray, cascade):
	plate_number = cascade.detectMultiScale(imgGray, 1.3, 5)

	for (x, y, w, h) in plate_number:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = imgGray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		clean_license(plate_number, img, "haar")
		#cv2.imwrite(path + "_plate" + algo, plate)
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


	
	
def contour_image_detect(imgGray):
	plate_number = [] 

	bfilter = cv2.bilateralFilter(imgGray, 25,25,25) #11 17 17
	imgEdged = cv2.Canny(bfilter, 30, 200)	
	cv2.imshow("imgEdged", imgEdged)

	keypoints = cv2.findContours(imgEdged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	contours = imutils.grab_contours(keypoints)
	possible_plate_contours = sorted(contours, key=cv2.contourArea,reverse=True)

	location = None
	for contour in possible_plate_contours:
		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 5, True)
		if len(approx) == 4:
			location = approx
			plate_number.append(location)
			break
			
	mask = np.zeros(imgGray.shape, np.uint8)	
	
		
	plate = convert_to_xywh(plate_number[0])
	plate_number = [] 
	plate_number.append(plate)
	clean_license(plate_number, img, "contour")
	cv2.imshow('img', img)
	
def main():
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	haar_image_detect(imgGray,plate_cascade)
	#start, end = video_detect(russian_plate_number_cascade)
	#print("----")
	#print(start)
	#print(end)
	#contour_image_detect(imgGray)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
main()
