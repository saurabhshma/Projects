from scipy import misc
import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn import svm
from numpy import genfromtxt
from sklearn import preprocessing
import time

startTime = time.time()

XTrainColor = np.zeros((1288, 1850))
YTrainColor = []
path = '/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/lfw_easy'
directoryContents = os.listdir(path)
exampleNum = 0
for i in directoryContents:
	temp = i
	if os.path.isdir(path+'/'+temp):
		for j in os.listdir(path+'/'+i):
			XTrainColor[exampleNum, :] = np.around(misc.imread(path+'/'+i+'/'+j, 'L').flatten())
			YTrainColor.append(temp)
			exampleNum = exampleNum + 1

eigenColor = genfromtxt("/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/eigenColor.txt")
projectedX = np.dot(XTrainColor, eigenColor)
projectedXnorm = preprocessing.scale(projectedX)
clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, projectedXnorm, YTrainColor, cv=10)
print("Projected Colored Accuracy: ", scores.mean() * 100)

endTime = time.time()
print("Time Elapsed: ", endTime - startTime)