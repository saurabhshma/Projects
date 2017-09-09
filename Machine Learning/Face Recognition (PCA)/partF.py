from scipy import misc
import numpy as np
import os
import time
from numpy import genfromtxt

XTrainColor = np.zeros((1288, 1850), dtype=int)
YTrainColor = []
path = '/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/lfw_easy'
directoryContents = os.listdir(path)
exampleNum = 0
for i in directoryContents:
	temp = i
	if os.path.isdir(path+'/'+temp):
		for j in os.listdir(path+'/'+i):
			XTrainColor[exampleNum, :] = misc.imread(path+'/'+i+'/'+j, 'L').flatten()
			exampleNum = exampleNum + 1

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

meanXColor = np.mean(XTrainColor, axis=0)
meanXGray = np.mean(XTrainGray, axis=0)

projectedXColor = genfromtxt("/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/projectedColor.txt")
projectedXGray = genfromtxt("/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/projectedGray.txt")

eigenColor = genfromtxt("/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/eigenColor.txt")
eigenGray = genfromtxt("/home/saurabh/Desktop/IIT D/Semester 2/ML/Assignments/Ass4/q2/eigenGray.txt")

print("Enter face id")
x = input()
dataType, index = x[:1], int(x[1:])
if dataType == 'g':
	temp = XTrainGray[index, :]
	temp1 = np.dot(projectedXGray[index, :], eigenGray.T) + meanXGray
	print("Original Image")
	misc.imshow(temp.reshape(112, 92))
	print("Reconstructed Image")
	misc.imshow(temp1.reshape(112, 92))
else:
	temp = XTrainColor[index, :]
	temp1 = np.dot(projectedXColor[index, :], eigenColor.T) + meanXColor
	print("Original Image")
	misc.imshow(temp.reshape(50, 37))
	print("Reconstructed Image")
	misc.imshow(temp1.reshape(50, 37))