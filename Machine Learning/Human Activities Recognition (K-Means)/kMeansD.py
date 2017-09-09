from numpy import genfromtxt
from sklearn.model_selection import cross_val_score
from sklearn import svm
X = genfromtxt('attr.txt')
Y = genfromtxt('label.txt')
clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, X, Y, cv=10)
for i in range(10):
	print("Cross Val Accuracy: ", scores[i])