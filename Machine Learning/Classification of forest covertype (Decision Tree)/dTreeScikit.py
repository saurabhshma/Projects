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

from  sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion='entropy', min_samples_split=2, min_samples_leaf=1, max_depth=None)
classifier = classifier.fit(XTrain, YTrain)
print("Training Accuracy: ", sum(classifier.predict(XTrain) == YTrain) * 100/ YTrain.size)
print("Test Accuracy: ", sum(classifier.predict(XTest) == YTest) * 100/ YTest.size)
print("Validation Accuracy: ", sum(classifier.predict(XValid) == YValid) * 100/ YValid.size)
print("Number of Nodes: ", classifier.tree_.node_count)


##################Random Forest####################
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(criterion='entropy', n_estimators=90, max_features=auto , bootstrap=False)
classifier = classifier.fit(XTrain, YTrain)
print("Training Accuracy: ", sum(classifier.predict(XTrain) == YTrain) * 100/ YTrain.size)
print("Test Accuracy: ", sum(classifier.predict(XTest) == YTest) * 100/ YTest.size)
print("Validation Accuracy: ", sum(classifier.predict(XValid) == YValid) * 100/ YValid.size)
print("Number of Nodes: ", classifier.tree_.node_count)
