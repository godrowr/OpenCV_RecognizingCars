# OpenCV_RecognizingCars
Using Machine Vision to recognize license plates, make and model on a car for COMP4102 project. 

### Demonstration

https://www.youtube.com/watch?v=pPQLGuZBYxk

### LPR Instructions

Ensure you have the dependencies installed!

```
pip install opencv-python numpy matplotlib imutils 
git clone https://github.com/godrowr/OpenCV_RecognizingCars
cd OpenCV_RecognizingCars
gedit LPR-Haar-Contour.py
```

Change the path to the file you wish to preform license plate recognition. 

- Contours work with all images in LicenseImages except 12.png. 
```
path = "LicenseImages/1"
algo = ".png"
```

- Haar cascade "russian_plate_number.xml" works for only suzuki_car.jpeg
```
path = "LicenseImages/suzuki_car"
algo = ".jpeg"
```
- Haar cascade "cascade.xml" works only for 12.png. 
```
path = "LicenseImages/12"
algo = ".png"
```
Haar video algorithm runs with the mp4 clip included.

Then uncomment out the line of the method you wish to run.
```
	haar_image_detect(imgGray,plate_cascade)
	#plate, frame  = haar_video_detect(russian_plate_number_cascade)
	#contour_image_detect(imgGray)
```

Then run the LPR code. 

```
python LPR-Haar-Contour.py
```
### OCR Instructions

python segmentation.py or seg.py “your image file name” to segment your image into single character. 

'''
An example would be passing the program 'example.png' or 'example2.png' incase other license plates don't segment correctly  *from the licensePlates folder*
images. The result images would write to the “Output” folder.
'''

To run shape context algorithm for segmented characters:
python shape_context.py to perform shape context recognition once you have segemented characters running the segmentation.py above.

'''
It will reads all character images
and display the prediction
'''

To run shape context algorithm for testing with training data:
python SHAPE.py 

'''
Pass in a index between 0-653 on line 353 and line 378 for the label to print the exact value and predicted value.
'''


### References:
Special thanks to all these people!

Louka Dlagnekov (2005). Video-based Car Surveillance: License Plate, Make, and Model Recognition. University of California. Available at: http://vision.ucsd.edu/belongie-grp/research/carRec/dlagnekov_thesis_2005.pdf 

Russian Car Crash compilation of road accidents, YouTube. Available at: 

https://www.youtube.com/watch?v=nHVY5TTMoyY 

Naotoshi Seo - Tutorial: OpenCV haartraining (Rapid Object Detection with a Cascade of Boosted Classifiers Based on Haar-like Features). Accessed 04, 2021. Available at: http://note.sonots.com/SciSoftware/haartraining.html 

Plates Portal (Ontario), Accessed 03, 2021. Available at:  

http://plates.portal.free.fr/canada/ontario-cdn.html 

License Plate Mania (Canada), Accessed 03, 2021. Available at: 

http://licenseplatemania.com/landenframes/canada_fr.htm 

LICENSE PLATES OF THE WORLD (Ontario) by Michael Kustermann.  Accessed 04,2021. Available at:  

http://www.worldlicenseplates.com/world/CN_ONTA.html 

Olav’s Plates (Ontario), Accessed 03, 2021. Available at: 

Http://www.olavsplates.com/canada.html 

Dutch Numberplate Archives. Accessed 03, 2021. Available at: 

http://dna.nl/ 

Tutorial-haartraining, handaga. Github. Accessed 03, 2021. Available at:  

https://github.com/handaga/tutorial-haartraining 

OpenCV-Haar-Adaboost, Andreluizfc. Github. Accessed 03, 2021. Available at: 

https://github.com/Andreluizfc/OpenCV-Haar-AdaBoost 

OpenCV_3_License_Plate_Recognition_Python, MicrocontrollersAndMore. Github. Accessed 03,2021. Available at: 

https://github.com/MicrocontrollersAndMore/OpenCV_3_License_Plate_Recognition_Python/tree/master/LicPlateImages 


Shape Context Matching For Efficient OCR 

https://people.csail.mit.edu/spillai/data/papers/scocr-project-paper.pdf 

Shape Context descriptor and fast characters recognition 

https://medium.com/machine-learning-world/shape-context-descriptor-and-fast-characters-recognition-c031eac726f9 


Shape context Matching descriptor 

https://en.wikipedia.org/wiki/Shape_context 


Shape Context: A New Descriptor for object matching and object recognition 

https://www.researchgate.net/publication/2353535_Shape_Context_A_new_descriptor_for_shape_matching_and_object_recognition/link/0912f50b3498fd04df000000/download 

