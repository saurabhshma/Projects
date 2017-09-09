tic
X = csvread('traindata.txt');
Y = csvread('trainlabels.txt');
testX = csvread('testdata.txt');
testY = csvread('testlabels.txt');
Y(find(Y == 2)) = -1;
m = length(Y);
for(i = 1:m)
    YX(i, :) = Y(i) * X(i, :);
end
Q = YX * YX';
b = ones(m, 1);

%find the support vectors
cvx_begin
    variable a(m)
    maximize((b' * a) - 0.5 * (a' * Q * a))
    subject to 
        0 <= a <= 500
        Y' * a == 0
cvx_end

supportVectorsLinear = find(a >= 1);

%find weight vectors w, intercept term b ,and testAccuracy
w = a' * YX;
indices = find(a <= 499 & a >= 1);
temp = w * X';
tempMax = max(temp(intersect(find(Y == -1), indices)));
tempMin = min(temp(intersect(find(Y == 1), indices)));
b = -(0.5) * (tempMax + tempMin); 

testAccLabels = (w * testX') + b;
testAccLabels(find(testAccLabels >= 0)) = 1;
testAccLabels(find(testAccLabels < 0)) = 2;

%trainAccuracy
%trainAccLabels = (w * X') + b;
%trainAccLabels(find(trainAccLabels >= 0)) = 1;
%trainAccLabels(find(trainAccLabels < 0)) = -1;

%trainAccuracy = sum(trainAccLabels' == Y) / length(Y)
testAccuracy = (sum(testAccLabels' == testY) / length(testY)) * 100

%Gaussian Kernel
gaussKern=zeros(m,m);
for i=1:m
  for j=1:m
    gaussKern(i, j) = exp(-2.5 * norm((X(i, :) - X(j, :)))^2);
  end
end

bGauss = ones(m, 1);
QGauss = diag(Y) * gaussKern * diag(Y);

%find the support vectors
cvx_begin
    variable aGauss(m)
    maximize((bGauss' * aGauss) - 0.5 * (aGauss' * QGauss * aGauss))
    subject to 
        0 <= aGauss <= 500
        Y' * aGauss == 0
cvx_end

supportVectorsGauss = find(aGauss >= 1);

%Testing data kernel
for i=1:m
  for j=1:length(testY)
    predTest(i, j) = exp(-2.5 * norm((X(i, :) - testX(j, :)))^2);
  end
end

WTX = aGauss' * diag(Y) * predTest;
tempGauss = aGauss' * diag(Y) * gaussKern;
gaussIndices = find(aGauss <= 499 & aGauss >= 1);
tempMax = max(tempGauss(intersect(find(Y == -1), gaussIndices)));
tempMin = min(tempGauss(intersect(find(Y == 1), gaussIndices)));
bGauss = -(0.5) * (tempMax + tempMin);

testAccLabels = WTX + bGauss;
testAccLabels(find(testAccLabels >= 0)) = 1;
testAccLabels(find(testAccLabels < 0)) = 2;
%Gaussian Test Accuracy
gaussTestAccuracy = (sum(testAccLabels' == testY) / length(testY)) * 100

%WTXTrain = aGauss' * diag(Y) * gaussKern;
%trainAccLabels = WTXTrain + bGauss;
%trainAccLabels(find(trainAccLabels >= 0)) = 1;
%trainAccLabels(find(trainAccLabels < 0)) = -1;
%Gaussian Train Accuracy
%gaussTrainAccuracy = sum(trainAccLabels' == Y) / length(Y)

toc 
