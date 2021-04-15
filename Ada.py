import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import cv2
import numpy as np
import glob

ALPHA_DICT = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'E',
              13: 'H', 14: 'I', 15: 'K', 16: 'L', 17: 'M', 18: 'N', 19: 'O', 20: 'P', 21: 'T', 22: 'U', 23: 'X', 24: 'Y',
              25: 'Z', 26: 'Background'}

folders = glob.glob("/home/godrowr/PycharmProjects/OpenCV_RecognizingCars/train_data") #TODO CHange absolute paths to relative
images = []
labels = []
index = 0
for folder in folders:
    for f in folder:
        index = index + 1
print(index)
index = 0
for folder in folders:
    for f in glob.glob(folder+'/*.png'): #folder+'/*.png'
        image = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
        tempimage = cv2.resize(image, (28, 28))
        images.append(tempimage.reshape(-1))
        labels.append(index)
    index = index + 1 
images = np.array(images)
labels = np.array(labels)
print("Images for training {}".format(images.size))
#Split arrays/matrices into random train and test subsets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, train_size=0.8,random_state=1)

forest = AdaBoostClassifier(n_estimators = 50)
#Build a boosted classifier from the training set (train_images, train_labels).
forest = forest.fit(train_images,train_labels)
forest_output = forest.predict(test_images)
print("accuracy score:{}".format(accuracy_score(test_labels, forest_output)))
test_image = test_images[0]
exact_label = test_labels[0]
print(test_labels[0])
print("exact value : {}".format(ALPHA_DICT[exact_label]))
predict_value = forest.predict([test_image])
print("predicted value : {}".format(ALPHA_DICT[predict_value[0]]))
print("numbers more than 10 represent alphbet following in dataset folders")