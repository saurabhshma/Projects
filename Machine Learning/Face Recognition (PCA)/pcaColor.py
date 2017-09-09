from scipy import misc
import numpy as np
import os
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
			exampleNum = exampleNum + 1

m = XTrainColor.shape[0]
n = XTrainColor.shape[1]
meanX = np.mean(XTrainColor, axis=0)
avgFaceColor = meanX.reshape(50, 37)
misc.imsave('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/colorImages/avgImage.png', avgFaceColor)
XTrainColor = XTrainColor - meanX;
_, _, eigenVectors = np.linalg.svd(XTrainColor)

top50EigenColor = eigenVectors[0:50, :]
np.savetxt('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/eigenColor.txt', top50EigenColor.T)
for i in range(5):
	temp = top50EigenColor[i, :]
	temp = temp - min(temp)
	temp = temp / (max(temp) - min(temp))
	temp = temp * 255
	misc.imsave('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/colorImages/'+str(i)+'.png', temp.reshape(50, 37))

projectedX = np.dot(XTrainColor, top50EigenColor.T)
np.savetxt('/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/projectedColor.txt', projectedX)
endTime = time.time()
print("Time Elapsed: ", endTime - startTime)