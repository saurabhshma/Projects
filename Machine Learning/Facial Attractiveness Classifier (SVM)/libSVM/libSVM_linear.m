X = load('traindata.txt');
Y = load('trainlabels.txt');
testX = load('testdata.txt');
testY = load('testlabels.txt');

Y(find(Y == 2)) = -1;
testY(find(testY == 2)) = -1;

model = svmtrain(Y, X, '-s 0  -t 0 -c 500');
[testLabel, testAccuracy, testDec_values] = svmpredict(testY, testX, model);