X = load('traindata.txt');
Y = load('trainlabels.txt');
testX = load('testdata.txt');
testY = load('testlabels.txt');

Y(find(Y == 2)) = -1;
testY(find(testY == 2)) = -1;

modelGauss = svmtrain(Y, X, '-s 0 -t 2 -c 500 -g 2.5');
[gaussTestLabel, gaussTestAccuracy, gauss_testDec_values] = svmpredict(testY, testX, modelGauss);