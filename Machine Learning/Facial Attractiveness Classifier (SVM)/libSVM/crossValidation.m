C = [1, 10, 100, 1000, 10000, 100000, 1000000];
X = load('traindata.txt');
Y = load('trainlabels.txt');
testX = load('testdata.txt');
testY = load('testlabels.txt');

Y(find(Y == 2)) = -1;
testY(find(testY == 2)) = -1;
for i = 1:length(C)
  trainAcc(i) = svmtrain(Y, X, sprintf("-s 0 -t 2 -c %d -g 2.5 -v 10", C(i)));
  modelGauss = svmtrain(Y, X, sprintf("-s 0 -t 2 -c %d -g 2.5", C(i)));
  [gaussTestLabel, gaussTestAccuracy, gauss_testDec_values] = svmpredict(testY, testX, modelGauss);
  testAcc(i) = gaussTestAccuracy(1);
end

figure();
hold on;
scatter(log10(C), trainAcc, 'b', '+', 'LineWidth', 4);
scatter(log10(C), testAcc, 'r', '+', 'LineWidth',4);
title('Cross Validation Test and Train Accuracy');
xlabel('C');
ylabel('Accuracy');
legend('Train Accuracy', 'Test Accuracy');
hold off;