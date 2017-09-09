from scipy import misc
import numpy as np
import os
import time

startTime = time.time()
XTrainGray = np.zeros((400, 10304), dtype=int)
path = '/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/orl_faces'
directoryContents = os.listdir(path)
exampleNum = 0
for i in directoryContents:
	temp = i
	if os.path.isdir(path+'/'+temp):
		for j in os.listdir(path+'/'+i):
			XTrainGray[exampleNum, :] = misc.imread(path+'/'+i+'/'+j).flatten()
			exampleNum = exampleNum + 1

m = XTrainGray.shape[0]
n = XTrainGray.shape[1]
meanX = np.mean(XTrainGray, axis=0)
avgFaceGray = meanX.reshape(112, 92)
misc.imsave('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/grayImages/avgImage.png', avgFaceGray)
XTrainGray = XTrainGray - meanX;
_, _, eigenVectors = np.linalg.svd(XTrainGray)

top50EigenGray = eigenVectors[0:50, :]
np.savetxt('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/eigenGray.txt', top50EigenGray.T)
for i in range(5):
	temp = top50EigenGray[i, :]
	temp = temp - min(temp)
	temp = temp / (max(temp) - min(temp))
	temp = temp * 255
	misc.imsave('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/grayImages/'+str(i)+'.png', temp.reshape(112, 92))

projectedX = np.dot(XTrainGray, top50EigenGray.T)
np.savetxt('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/projectedGray.txt', projectedX)
endTime = time.time()
print("Time Elapsed: ", endTime - startTime)