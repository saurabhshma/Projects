import numpy as np
from numpy import genfromtxt
import time
import math

#startTime = time.time()

#trainData = genfromtxt('train.dat', delimiter=',', dtype=int, skip_header=1)
trainData = np.loadtxt('train.dat', delimiter=',', dtype=int, skiprows=1)
tempData = np.hsplit(trainData, [54, 55])
YTrain = np.asarray(tempData[1]).flatten()
initIndex = np.arange(YTrain.size)
XTrain = np.asarray(tempData[0])
XTrain = np.asarray(np.concatenate((XTrain, np.asmatrix(initIndex).transpose()), axis=1))

index = [0]*54
for i in range(0, 54):
	index[i] = 1

#startTime = time.time()

class Node:
	def __init__(self, indices, left=None, right=None):
		self.indices = indices
		self.entropy = -math.inf
		self.majorityClass = -math.inf
		self.bestAttribute = -math.inf
		self.left = left
		self.right = right
		self.median = -math.inf 
	def setEntropy(self, value):
		self.entropy = value
	def setMajorityClass(self, value):
		self.majorityClass = value
	def setBestAttribute(self, value):
		self.bestAttribute = value
	def setMedian(self, value):
		self.median = value

negPosIndexes = [[0 for i in range(54)] for y in range(2)]

def getEntropy(node):
	s = 0
	tempIndices = node
	temp = YTrain[tempIndices]
	tempSizes = [-math.inf] * 7
	for i in range(7):
		tempSizes[i] = np.count_nonzero(temp == (i + 1))
	nodeSize = sum(tempSizes)
	for i in range(7):
		if ((tempSizes[i] == 0) | (nodeSize == 0)):
			continue
		else:
			tempProb = tempSizes[i] / nodeSize
			s = s - (tempProb * np.log2(tempProb))
	return(s)

def findMajorityClass(node):
	tempSizes = [-math.inf] * 7
	tempIndices = node.indices
	temp = YTrain[tempIndices]
	for i in range(7):
		tempSizes[i] = np.count_nonzero(temp == (i + 1))
	return tempSizes.index(max(tempSizes))

def findBestAttribute(node, attributeIndex):
	tempIndices = node.indices
	temp = YTrain[tempIndices]
	tempSizes = [-math.inf] * 7
	for i in range(7):
		tempSizes[i] = np.count_nonzero(temp == (i + 1))
	nodeSize = sum(tempSizes)
	if(tempSizes.count(0) == 6):
		return -1
	else:
		medians = [-math.inf]*10
		negPosNumbers = [[-math.inf for i in range(54)] for y in range(2)]
		condEntropy = [math.inf]*54
		temp1 = XTrain[tempIndices]
		for i in range(54):
			if(attributeIndex[i] != 0):
				temp2 = temp1[:, i]
				if(i < 10):
					medians[i] = np.median(temp2)
					negPosNumbers[0][i] = np.count_nonzero(temp2 <= medians[i])
					negPosNumbers[1][i] = np.count_nonzero(temp2 > medians[i])
					tmp0 = np.argwhere(temp2 <= medians[i]).flatten()
					tmp1 = np.argwhere(temp2 > medians[i]).flatten()
					negPosIndexes[0][i] = temp1[:,54][tmp0]
					negPosIndexes[1][i] = temp1[:,54][tmp1]
				else:
					negPosNumbers[0][i] = np.count_nonzero(temp2 == 0)
					negPosNumbers[1][i] = np.count_nonzero(temp2 == 1)
					tmp0 = np.argwhere(temp2 == 0).flatten()
					tmp1 = np.argwhere(temp2 == 1).flatten()
					negPosIndexes[0][i] = temp1[:,54][tmp0]
					negPosIndexes[1][i] = temp1[:,54][tmp1]
					#negPosIndexes[1][i] = np.intersect1d(tmp1, tempIndices)
				#print("lol: ", negPosNumbers[0][i])
				if(sum(tempSizes) == 0):
					prob0 = math.inf
					prob1 = math.inf
				else:
					prob0 = (negPosNumbers[0][i]/nodeSize)
					prob1 = (negPosNumbers[1][i]/nodeSize)
				#print("prob0", prob0)
				#print("prob1", prob1)
				if(prob0 == 0 or prob1 == 0):
					condEntropy[i] = math.inf 
				else:
					#print("lol")
					ent0 = getEntropy(negPosIndexes[0][i])
					ent1 = getEntropy(negPosIndexes[1][i])
					condEntropy[i] = (prob0 * ent0) + (prob1 * ent1)
		ind = condEntropy.index(min(condEntropy))
		if(ind < 10):
			node.setMedian(medians[ind])
		return (ind)

countNodes = 0
def growTree(node, attributeIndex):
	global countNodes
	countNodes = countNodes + 1
	print(countNodes)
	x = getEntropy(node.indices)
	node.setEntropy(x)
	y = findMajorityClass(node)
	node.setMajorityClass(y)
	z = findBestAttribute(node, attributeIndex)
	if(z >= 0):
		#print("Index: ", z)
		node.setBestAttribute(z)
		if(z >= 10):
			attributeIndex[z] = 0
		leftAttributeIndex = attributeIndex[:]
		rightAttributeIndex = attributeIndex[:]
		leftIndices = negPosIndexes[0][z]
		rightIndices = negPosIndexes[1][z] 
		node.left = Node(leftIndices)
		node.right = Node(rightIndices)
		#print("left indes",leftIndices)
		growTree(node.left, leftAttributeIndex)
		growTree(node.right, rightAttributeIndex)
	else:
		return

node = Node(initIndex)
startTime = time.time()
growTree(node, index)
endTime = time.time()

print("Time elapsed: ", endTime - startTime)
print("Number of Nodes: ", countNodes)

#print(Y)