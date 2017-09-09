from scipy import misc
import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn import svm
import time

startTime = time.time()

XTrainColor = np.zeros((1288, 1850))
YTrainColor = []
path = '/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/lfw_easy'
directoryContents = os.listdir(path)
directoryContents
exampleNum = 0
for i in directoryContents:
	temp = i
	if os.path.isdir(path+'/'+temp):
		for j in os.listdir(path+'/'+i):
			XTrainColor[exampleNum, :] = np.around(misc.imread(path+'/'+i+'/'+j, 'L').flatten())
			YTrainColor.append(temp)
			exampleNum = exampleNum + 1

clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, XTrainColor, YTrainColor, cv=10)
print("Colored Accuracy: ", scores.mean() * 100)

endTime = time.time()
print("Time Elapsed: ", endTime - startTime)