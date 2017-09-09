import numpy as np
from numpy import genfromtxt
import time
import math
import copy
import pandas
import matplotlib.pyplot as plt

startCompleteTime = time.time()
startTime = time.time()
trainData = pandas.read_csv('train.dat', delimiter=',', dtype=int, skiprows=1, header=None)
testData = pandas.read_csv('test.dat', delimiter=',', dtype=int, skiprows=1, header=None)
validData = pandas.read_csv('valid.dat', delimiter=',', dtype=int, skiprows=1, header=None)
endTime = time.time()
print("Data Read time: ", endTime - startTime)
trainData = np.asarray(trainData)
testData = np.asarray(testData)
validData = np.asarray(validData)
XTrain = trainData[:, 0:54]
YTrain = trainData[:, 54]
XTest = testData[:, 0:54]
YTest = testData[:, 54]
XValid = validData[:, 0:54]
YValid = validData[:, 54]

initIndex = np.arange(YTrain.size)
testIndex = np.arange(YTest.size)
validIndex = np.arange(YValid.size)

XTrain = np.asarray(np.concatenate((XTrain, np.asmatrix(initIndex).transpose()), axis=1))
XTest = np.asarray(np.concatenate((XTest, np.asmatrix(testIndex).transpose()), axis=1))
XValid = np.asarray(np.concatenate((XValid, np.asmatrix(validIndex).transpose()), axis=1))

index = [0]*54
for i in range(0, 54):
	index[i] = 1

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
				if(sum(tempSizes) == 0):
					prob0 = math.inf
					prob1 = math.inf
				else:
					prob0 = (negPosNumbers[0][i]/nodeSize)
					prob1 = (negPosNumbers[1][i]/nodeSize)
				if(prob0 == 0 or prob1 == 0):
					condEntropy[i] = math.inf 
				else:
					ent0 = getEntropy(negPosIndexes[0][i])
					ent1 = getEntropy(negPosIndexes[1][i])
					condEntropy[i] = (prob0 * ent0) + (prob1 * ent1)
		ind = condEntropy.index(min(condEntropy))
		if(ind < 10):
			node.setMedian(medians[ind])
		return (ind)

def getClass(root, data):
	if root.left == None and root.right == None:
		return root.majorityClass
	else:
		if root.bestAttribute < 10:
			if data[root.bestAttribute] <= root.median:
				root = root.left
			else:
				root = root.right
		else:
			if data[root.bestAttribute] == 0:
				root = root.left
			else:
				root = root.right
		return getClass(root, data)

def findAccuracy(node, dataSet, size):
	testIndices = np.zeros(size, dtype=int)
	for i in range(size):
		testIndices[i] = getClass(node, dataSet[i]) + 1
	return testIndices


def growTree(node, attributeIndex):
	global countNodes
	countNodes = countNodes + 1
	print("Number of nodes: ", countNodes)
	x = getEntropy(node.indices)
	node.setEntropy(x)
	y = findMajorityClass(node)
	node.setMajorityClass(y)
	z = findBestAttribute(node, attributeIndex)
	if(z >= 0):
		node.setBestAttribute(z)
		if(z >= 10):
			attributeIndex[z] = 0
		leftAttributeIndex = attributeIndex[:]
		rightAttributeIndex = attributeIndex[:]
		leftIndices = negPosIndexes[0][z]
		rightIndices = negPosIndexes[1][z] 
		node.left = Node(leftIndices)
		node.right = Node(rightIndices)
		growTree(node.left, leftAttributeIndex)
		growTree(node.right, rightAttributeIndex)
	else:
		return


def findEachNodeAccuracyTrain(root):
	global nodeNumber
	global trainAuxAccuracyMatrix
	global trainAuxLabelMatrix
	nodeNumber = nodeNumber + 1
	if root.left == None and root.right == None:
		trainAuxLabelMatrix[root.indices] = root.majorityClass + 1
		trainAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(trainAuxLabelMatrix == YTrain) / YTrain.size) * 100
		#print("Accuracy: ", nodeNumber, trainAuxAccuracyMatrix[nodeNumber])
		return
	else:
		trainAuxLabelMatrix[root.indices] = root.majorityClass + 1
		trainAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(trainAuxLabelMatrix == YTrain) / YTrain.size) * 100
		#print("Accuracy: ", nodeNumber, trainAuxAccuracyMatrix[nodeNumber])
		temp1 = root.left
		temp2 = root.right
		findEachNodeAccuracyTrain(temp1)
		findEachNodeAccuracyTrain(temp2)

def findEachNodeAccuracyTest(root, indices):
	global nodeNumber
	global testAuxAccuracyMatrix
	global testAuxLabelMatrix
	nodeNumber = nodeNumber + 1
	if root.left == None and root.right == None:
		testAuxLabelMatrix[indices] = root.majorityClass + 1
		testAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(testAuxLabelMatrix == YTest) / YTest.size) * 100
		#print("Accuracy: ", nodeNumber, testAuxAccuracyMatrix[nodeNumber])
		return
	else:
		testAuxLabelMatrix[indices] = root.majorityClass + 1
		testAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(testAuxLabelMatrix == YTest) / YTest.size) * 100
		#print("Accuracy: ", nodeNumber, testAuxAccuracyMatrix[nodeNumber])
		temp = XTest[indices][:, root.bestAttribute]
		if(root.bestAttribute < 10):
			leftTempIndices = XTest[indices][np.argwhere(temp <= root.median).flatten()][:, 54]
			rightTempIndices = XTest[indices][np.argwhere(temp > root.median).flatten()][:, 54]
		else:
			leftTempIndices = XTest[indices][np.argwhere(temp == 0).flatten()][:, 54]
			rightTempIndices = XTest[indices][np.argwhere(temp == 1).flatten()][:, 54]
		temp1 = root.left
		temp2 = root.right
		findEachNodeAccuracyTest(temp1, leftTempIndices)
		findEachNodeAccuracyTest(temp2, rightTempIndices)

def findEachNodeAccuracyValid(root, indices):
	global nodeNumber
	global validAuxAccuracyMatrix
	global validAuxLabelMatrix
	nodeNumber = nodeNumber + 1
	if root.left == None and root.right == None:
		validAuxLabelMatrix[indices] = root.majorityClass + 1
		validAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(validAuxLabelMatrix == YValid) / YValid.size) * 100
		#print("Accuracy: ", nodeNumber, validAuxAccuracyMatrix[nodeNumber])
		return
	else:
		validAuxLabelMatrix[indices] = root.majorityClass + 1
		validAuxAccuracyMatrix[nodeNumber] = (np.count_nonzero(validAuxLabelMatrix == YValid) / YValid.size) * 100
		#print("Accuracy: ", nodeNumber, validAuxAccuracyMatrix[nodeNumber])
		temp = XValid[indices][:, root.bestAttribute]
		if(root.bestAttribute < 10):
			leftTempIndices = XValid[indices][np.argwhere(temp <= root.median).flatten()][:, 54]
			rightTempIndices = XValid[indices][np.argwhere(temp > root.median).flatten()][:, 54]
		else:
			leftTempIndices = XValid[indices][np.argwhere(temp == 0).flatten()][:, 54]
			rightTempIndices = XValid[indices][np.argwhere(temp == 1).flatten()][:, 54]
		temp1 = root.left
		temp2 = root.right
		findEachNodeAccuracyValid(temp1, leftTempIndices)
		findEachNodeAccuracyValid(temp2, rightTempIndices)

def pruneTree(root, validInd, testInd, trainInd):
	global pruneTreeNumNodes
	global validPruneCorrect
	global testPruneCorrect
	global trainPruneCorrect
	if(root.left == None and root.right == None):
		tempValid = np.count_nonzero(YValid[validInd] == (root.majorityClass + 1))
		tempTest = np.count_nonzero(YTest[testInd] == (root.majorityClass + 1))
		tempTrain = np.count_nonzero(YTrain[trainInd] == (root.majorityClass + 1))
		return (tempValid, tempTest, tempTrain, 1)
	else:
		tempValidBestAttr = XValid[validInd][:, root.bestAttribute]
		tempTestBestAttr = XTest[testInd][:, root.bestAttribute]
		tempTrainBestAttr = XTrain[trainInd][:, root.bestAttribute]
		tempLeft = root.left
		tempRight = root.right
		if(root.bestAttribute < 10):
			leftTempIndicesValid = XValid[validInd][np.argwhere(tempValidBestAttr <= root.median).flatten()][:, 54]
			rightTempIndicesValid = XValid[validInd][np.argwhere(tempValidBestAttr > root.median).flatten()][:, 54]
			leftTempIndicesTest = XTest[testInd][np.argwhere(tempTestBestAttr <= root.median).flatten()][:, 54]
			rightTempIndicesTest = XTest[testInd][np.argwhere(tempTestBestAttr > root.median).flatten()][:, 54]
			leftTempIndicesTrain = XTrain[trainInd][np.argwhere(tempTrainBestAttr <= root.median).flatten()][:, 54]
			rightTempIndicesTrain = XTrain[trainInd][np.argwhere(tempTrainBestAttr > root.median).flatten()][:, 54]
		else:
			leftTempIndicesValid = XValid[validInd][np.argwhere(tempValidBestAttr == 0).flatten()][:, 54]
			rightTempIndicesValid = XValid[validInd][np.argwhere(tempValidBestAttr == 1).flatten()][:, 54]
			leftTempIndicesTest = XTest[testInd][np.argwhere(tempTestBestAttr == 0).flatten()][:, 54]
			rightTempIndicesTest = XTest[testInd][np.argwhere(tempTestBestAttr == 1).flatten()][:, 54]
			leftTempIndicesTrain = XTrain[trainInd][np.argwhere(tempTrainBestAttr == 0).flatten()][:, 54]
			rightTempIndicesTrain = XTrain[trainInd][np.argwhere(tempTrainBestAttr == 1).flatten()][:, 54]
		parentCountValid = np.count_nonzero(YValid[validInd] == (root.majorityClass + 1))
		parentCountTest = np.count_nonzero(YTest[testInd] == (root.majorityClass + 1))
		parentCountTrain = np.count_nonzero(YTrain[trainInd] == (root.majorityClass + 1))
		leftChildCountValid, leftChildCountTest, leftChildCountTrain, leftSubtreeChild = pruneTree(tempLeft, leftTempIndicesValid, leftTempIndicesTest, leftTempIndicesTrain)
		rightChildCountValid, rightChildCountTest, rightChildCountTrain, rightSubtreeChild = pruneTree(tempRight, rightTempIndicesValid, rightTempIndicesTest, rightTempIndicesTrain)
		if((leftChildCountValid + rightChildCountValid) < parentCountValid):
			root.left = None
			root.right = None
			pruneTreeNumNodes.append(pruneTreeNumNodes[len(pruneTreeNumNodes) - 1] - (leftSubtreeChild + rightSubtreeChild))
			validPruneCorrect.append(validPruneCorrect[len(validPruneCorrect) - 1] + (parentCountValid - (leftChildCountValid + rightChildCountValid)))
			testPruneCorrect.append(testPruneCorrect[len(testPruneCorrect) - 1] + (parentCountTest - (leftChildCountTest + rightChildCountTest)))
			trainPruneCorrect.append(trainPruneCorrect[len(trainPruneCorrect) - 1] + (parentCountTrain - (leftChildCountTrain + rightChildCountTrain)))
			return (parentCountValid, parentCountTest, parentCountTrain, 1)
		else:
			return (leftChildCountValid + rightChildCountValid), (leftChildCountTest + rightChildCountTest), (leftChildCountTrain + rightChildCountTrain), (leftSubtreeChild + rightSubtreeChild + 1)


countNodes = 0
node = Node(initIndex)
startTime = time.time()
growTree(node, index)
endTime = time.time()
print("Grow Tree Time: ", endTime - startTime)

startTime = time.time()
trainTestLabels = findAccuracy(node, XTrain, YTrain.size)
trainAccuracy = (np.count_nonzero(trainTestLabels == YTrain) / YTrain.size) * 100
testTestLabels = findAccuracy(node, XTest, YTest.size)
testAccuracy = (np.count_nonzero(testTestLabels == YTest) / YTest.size) * 100
validTestLabels = findAccuracy(node, XValid, YValid.size)
validAccuracy = (np.count_nonzero(validTestLabels == YValid) / YValid.size) * 100

print("Number of Nodes: ", countNodes)
print("Train Accuracy: ", trainAccuracy)
print("Test Accuracy: ", testAccuracy)
print("Valid Accuracy: ", validAccuracy)
endTime = time.time()
print("Find Accuracy Time : ", endTime - startTime)

tempTrainCounts = np.count_nonzero(trainTestLabels == YTrain)
tempTestCounts = np.count_nonzero(testTestLabels == YTest)
tempValidCounts = np.count_nonzero(validTestLabels == YValid)

pruneTreeNumNodes = [countNodes]
validPruneCorrect = [0]
testPruneCorrect = [0]
trainPruneCorrect = [0]

tempNode = copy.deepcopy(node)

startTime = time.time()
validCorrect, testCorrect, trainCorrect, junk = pruneTree(tempNode, validIndex, testIndex, initIndex)
endTime = time.time()
print("Prune Tree Time: ", endTime - startTime)

trainPruneCorrect = [((tempTrainCounts + x) * 100/ YTrain.size) for x in trainPruneCorrect]
testPruneCorrect = [((tempTestCounts + x) * 100/ YTest.size) for x in testPruneCorrect]
validPruneCorrect = [((tempValidCounts + x) * 100/ YValid.size) for x in validPruneCorrect]

trainAuxAccuracyMatrix = np.zeros(countNodes, dtype=float)
testAuxAccuracyMatrix = np.zeros(countNodes, dtype=float)
validAuxAccuracyMatrix = np.zeros(countNodes, dtype=float)
trainAuxLabelMatrix = np.zeros(YTrain.size, dtype=int)
testAuxLabelMatrix = np.zeros(YTest.size, dtype=int)
validAuxLabelMatrix = np.zeros(YValid.size, dtype=int)
startTime = time.time()
nodeNumber = -1
findEachNodeAccuracyTrain(node)
nodeNumber = -1
findEachNodeAccuracyTest(node, testIndex)
nodeNumber = -1
findEachNodeAccuracyValid(node, validIndex)
endTime = time.time()
print("Find Each Node Accuracy Time: ", endTime - startTime)
print("Pruned Tree Valid Accuracy: ", validCorrect * 100/ YValid.size)
print("Pruned Tree Test Accuracy: ", testCorrect * 100 / YTest.size)
print("Pruned Tree Train Accuracy: ", trainCorrect * 100 / YTrain.size)

endCompleteTime = time.time()
print("Total Time elapsed: ", endCompleteTime - startCompleteTime)
 
#Plotting graphs
#Accuracy graphs
xAxis = np.arange(trainAuxAccuracyMatrix.size)
plt.plot(xAxis, trainAuxAccuracyMatrix, 'b', label='Train Data Accuracy')
plt.plot(xAxis, testAuxAccuracyMatrix, 'r', label='Test Data Accuracy')
plt.plot(xAxis, validAuxAccuracyMatrix, 'g', label='Valid Data Accuracy')
plt.legend(loc = 'lower right')
plt.xlabel('Number of nodes')
plt.ylabel('Accuracies')
plt.show()

#Prune graph
plt.plot(pruneTreeNumNodes, validPruneCorrect, 'b', label='Prune validation Accuracy')
plt.plot(pruneTreeNumNodes, testPruneCorrect, 'r', label='Prune test Accuracy')
plt.plot(pruneTreeNumNodes, trainPruneCorrect, 'g', label='Prune train Accuracy')
plt.legend(loc = 'lower right')
plt.xlabel('Number of nodes')
plt.ylabel('Accuracies')
plt.axis((77000, 92000,80,105))
plt.show()