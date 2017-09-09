import time
import math
startTime = time.time()
'''
YIndex = [0]*7
for i in range(1, 8):
	YIndex[i - 1] = np.argwhere(YTrain == i).flatten()

X0Index = [[0 for x in range(7)] for y in range(54)]
X1Index = [[0 for x in range(7)] for y in range(54)]

for i in range(10, 54):
	xi0 = np.argwhere(XTrain[:, i] == 0).flatten()
	xi1 = np.argwhere(XTrain[:, i] == 1).flatten()
	for j in range(0, 7):
		X0Index[i][j] = np.intersect1d(xi0, YIndex[j])
		X1Index[i][j] = np.intersect1d(xi1, YIndex[j])

for i in range(0, 9):
	xMedian = np.median(XTrain[:, i])
	xi0 = np.argwhere(XTrain[:, i] < xMedian).flatten()
	xi1 = np.argwhere(XTrain[:, i] >= xMedian).flatten()
	for j in range(0, 7):
		X0Index[i][j] = np.intersect1d(xi0, YIndex[j])
		X1Index[i][j] = np.intersect1d(xi1, YIndex[j])
'''
index = [0]*54
for i in range(0, 54):
	if(i < 10):
		index[i] = 1    #continuous
	else:
		index[i] = 2    #discrete




countNodes = 0;
class Tree:
	def __init__(self, targetNode, at_type = 0, median = -math.inf, attribute = -1, majority = -1, left=None, right=None):
		self.targetNode = targetNode
		self.left  = left
		self.right = right
		self.at_type = at_type
		self.median = median
		self.attribute = attribute
		y = [0]*7
		for i in range(0, 7):
			y[i] = self.targetNode[i].size
		self.majority = y.index(max(y))

def getMajority(node):
	return (node.majority)

def getType(node):
	return (node.at_type)

def getMedian(node):
	return (node.median)

def getAttribute(node):
	return (node.attribute)

def getSize(node):
	x = 0
	for i in range(0, 7):
		x = x + node[i].size
	return(x)

def getTargetCount(node):
	count = 0
	for i in range(0, 7):
		if(node[i].size == 0):
			continue
		else:
			count = count + 1
	return (count)

def getMedian(node, attribute):
	x = np.array([], dtype=int)
	for i in range(7):
		x = np.concatenate((x, XTrain[node[i]][:, attribute]))
	return np.median(x)

def getEntropy(node):
	s = 0
	nodeSize = getSize(node)
	for i in range(0, 7):
		if(nodeSize == 0):
			break
		else:
			temp = node[i].size
			tempProb = temp / nodeSize
			if tempProb == 0:
				continue
			else:
				s = s - (tempProb * np.log2(tempProb))
	return(s)

def getCondEntropy(node, attribute):
	temp0Node = [0]*7
	temp1Node = [0]*7
	for i in range(0, 7):
		temp0Node[i] = np.intersect1d(X0Index[attribute][i], node[i])
		temp1Node[i] = np.intersect1d(X1Index[attribute][i], node[i])
	parentSize = getSize(node)
	x0Size = getSize(temp0Node)
	x1Size = getSize(temp1Node)
	x0Prob = x0Size / parentSize
	x1Prob = x1Size / parentSize
	if (x0Size == 0 | x1Size == 0):
		return (-math.inf)
	else:
		return(x0Prob * getEntropy(temp0Node) + x1Prob * getEntropy(temp1Node))

def getMutualInfo(node, ind):
	tempMutualInfo = [-1]*54
	tempEntropy = getEntropy(node.targetNode)
	for i in range(0, 10):
		tempMedian = getMedian(node.targetNode, i)
		for j in range(0, 7):
			X0Index[i][j] = node.targetNode[j][np.argwhere(XTrain[node.targetNode[j]][:, i] <= tempMedian).flatten()]
			X1Index[i][j] = node.targetNode[j][np.argwhere(XTrain[node.targetNode[j]][:, i] > tempMedian).flatten()]
	for i in range(0, 54):
		if(ind[i] == 0):
			tempMutualInfo[i] = -math.inf
			continue
		else:
			tmp = getCondEntropy(node.targetNode, i)
			if(tmp == -math.inf):
				tempMutualInfo[i] = -math.inf
			else:
				tempMutualInfo[i] = tempEntropy - getCondEntropy(node.targetNode, i)
	#print(tempMutualInfo)
	a = max(tempMutualInfo)
	b = tempMutualInfo.index(max(tempMutualInfo))
	node.attribute = b
	if(ind[b] == 1):
		node.at_type = 1
		x = np.array([], dtype=int)
		for i in range(7):
			x = np.concatenate((x, XTrain[node.targetNode[i]][:, b]))
		node.median = np.median(x)
	else:
		node.at_type = 2
	return [a, b]

def getBestAttribute(node, ind):
	[value, i] = getMutualInfo(node, ind)
	print("Index: ", i)
	#print("Attribute: ", attributes[i])
	#print("Value: ", value)
	return (i)

def printNode(node):
	x = [0]*7
	for i in range(7):
		x[i] = node[i].size
	print(x)

countNodes = 0
def growTree(node, ind):
	ind1 = ind[:]
	ind2 = ind[:]
	global countNodes
	countNodes = countNodes + 1
	bestIndex = getBestAttribute(node, ind)
	if(getType(node) == 2):
		ind1[bestIndex] = 0
		ind2[bestIndex] = 0
	if(getTargetCount(node.targetNode) == 1):
		ind1[bestIndex] = 0
		ind2[bestIndex] = 0
		return
	temp0 = [0]*7
	temp1 = [0]*7
	for i in range(0, 7):
		temp0[i] = np.intersect1d(X0Index[bestIndex][i], node.targetNode[i])
		temp1[i] = np.intersect1d(X1Index[bestIndex][i], node.targetNode[i])
	#printNode(temp0)
	#printNode(temp1)
	leftNode = Tree(temp0)
	rightNode = Tree(temp1)
	node.left = leftNode
	node.right = rightNode
	growTree(node.left, ind1)
	growTree(node.right, ind2)

index = [0]*54
for i in range(0, 54):
	if(i < 10):
		index[i] = 1    #continuous
	else:
		index[i] = 2    #discrete

class A:
	def __init__(self, a = 0):
		self.a = a
		
	def x(self):
		temp1 = A(1)
		temp2 = A(2)
		print(temp1.a + temp2.a)
'''
'''
class a:
	def c(self, ind):
		ind[0] = -1

temp = a()
temp.c(index)
'''
'''

class Node:
	def __init__(self, val):
		self.l_child = None
		self.r_child = None
		self.data = val

def binary_insert(root, node):
	if root.data == None:
		root.data = node.data
	else:
		if root.data > node.data:
			if root.l_child == None:
				root.l_child = node
			else:
				binary_insert(root.l_child, node)
		else:
			if root.r_child == None:
				root.r_child = node
			else:
				binary_insert(root.r_child, node)

def in_order_print(root):
	if not root:
		return
	in_order_print(root.l_child)
	print(root.data)
	in_order_print(root.r_child)

def pre_order_print(root):
	if not root:
		return        
	print(root.data)
	pre_order_print(root.l_child)
	pre_order_print(root.r_child)
