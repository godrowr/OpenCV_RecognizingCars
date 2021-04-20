from PIL import Image
import numpy
import cv2
import glob

basewidth = 100
imagenum = 56
folder = "negatives/"


def resizeImage(imageName):
	img = Image.open(imageName)
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	img.save(imageName)


for i in glob.glob(folder+'/*.jpg'):
	resizeImage(i)



