# OpenCV_RecognizingCars
Using Machine Vision to recognize license plates, make and model on a car for COMP4102 project. 

## Instructions

Ensure you have the dependencies installed!
'''
pip install opencv-python, numpy, matplotlib, imutils, 
git clone https://github.com/godrowr/OpenCV_RecognizingCars
cd OpenCV_RecognizingCars
gedit LPR-Haar-Contour.py
'''

Change the path to the file you wish to preform license plate recognition. 

- Contours work with everythin except 12.png. 
'''
path = "LicenseImages/1"
algo = ".png"
'''

- Haar cascade "russian_plate_number.xml" works for only suzuki_car.jpeg
'''
path = "LicenseImages/suzuki_car"
algo = ".jpeg"
'''
- Haar cascade "cascade.xml" works only for 12.png. 
'''
path = "LicenseImages/12"
algo = ".png"
'''

Then uncomment out the line of the method you wish to run.
'''
	haar_image_detect(imgGray,plate_cascade)
	#plate, frame  = haar_video_detect(russian_plate_number_cascade)
	#contour_image_detect(imgGray)
'''

Then run the LPR code. 

'''
python LPR-Haar-Contour.py
'''


References:
(Please see final report included) 
-  MicrocontrollersAndMore / OpenCV_3_License_Plate_Recognition_Python 
-  Andreluizfc / OpenCV-Haar-AdaBoost 
-  GeekyPRAVEE / OpenCV-Projects 
-   AjayAndData / Licence-plate-detection-and-recognition---using-openCV-only 
