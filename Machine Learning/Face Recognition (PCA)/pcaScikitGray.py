from scipy import misc
import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn import svm
import time

startTime = time.time()

XTrainGray = np.zeros((400, 10304), dtype=int)
YTrainGray = []
path = '/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/orl_faces'
directoryContents = os.listdir(path)
exampleNum = 0
for i in directoryContents:
	temp = i
	if os.path.isdir(path+'/'+temp):
		for j in os.listdir(path+'/'+i):
			XTrainGray[exampleNum, :] = misc.imread(path+'/'+i+'/'+j).flatten()
			YTrainGray.append(temp)
			exampleNum = exampleNum + 1

clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, XTrainGray, YTrainGray, cv=10)
print("Gray Accuracy: ", scores.mean() * 100)

endTime = time.time()

print("Time Elapsed: ", endTime - startTime)