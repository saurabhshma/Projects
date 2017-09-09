clear all;
trainData = importdata('train.data');
testData = importdata('test.data');
XTrain = trainData(:, 1:126);
YTrain = trainData(:, 127);
XTest = testData(:, 1:126);
YTest = testData(:, 127);
learningRate = 0.05;
%learningRate = 0.1;
epsilon = 0.00001;

mTrain = size(YTrain, 1);  %number of training examples
mTest = size(YTest, 1);  %number of test examples
n = 126;  %size of each training example
numHidden = 100;  %number of hidden layers

XTrain = [ones(mTrain, 1), XTrain];
XTest = [ones(mTest, 1), XTest];

tempTarget = [1, 0, 0; 0, 1, 0; 0, 0, 1];
targetY = zeros(mTrain, 3);
for i=1:mTrain
  if(YTrain(i) == 1)
    targetY(i, :) = tempTarget(1, :);
  elseif(YTrain(i) == 2)
    targetY(i, :) = tempTarget(2, :);
  else
    targetY(i, :) = tempTarget(3, :);
  end
end
numHidden = 100
tic;
  
costPrev = realmax;
inputWeights = ((rand(numHidden, n + 1) .* 2) - 1) ./ 1000;
hiddenWeights = ((rand(3, numHidden + 1) .* 2) - 1) ./ 1000;
outHidden = zeros(numHidden, 1); %output from hidden layer 
temp = relu([ones(mTrain, 1), relu(XTrain * inputWeights')] * hiddenWeights');
cost = costFunction(targetY, temp);
t = 0;
while((costPrev - cost) > epsilon)
  t = t + 1;
  for i = 1:mTrain
    outHidden = relu(inputWeights * XTrain(i, :)');
    outFinal = relu(hiddenWeights * [1;outHidden]);  %output from output layer
    outError = reluErrorOutput(outFinal', targetY(i, :));
    hiddenError = reluErrorHidden(outError, hiddenWeights, [1;outHidden]);
    deltaHidden = ([1;outHidden] * outError) .* learningRate;
    hiddenWeights = hiddenWeights + deltaHidden';
    deltaInput = (hiddenError(2:numHidden+1, 1) * XTrain(i, :)) .* learningRate;
    inputWeights = inputWeights + deltaInput;
  end
  temp = relu([ones(mTrain, 1), relu(XTrain * inputWeights')] * hiddenWeights');
  costPrev = cost;
  cost = costFunction(targetY, temp);
end
trainAccTargetY = zeros(mTrain, 1);
testAccTargetY = zeros(mTest, 1);

 for i = 1:mTrain
   [~, index] = max(sigmoid([1, sigmoid(XTrain(i, :) * inputWeights')] * hiddenWeights'));
   trainAccTargetY(i) = index;
 end

for i = 1:mTest
  [~, index] = max(sigmoid([1, sigmoid(XTest(i, :) * inputWeights')] * hiddenWeights'));
  testAccTargetY(i) = index;
end

trainAccuracy = (sum(trainAccTargetY == YTrain))/ mTrain
testAccuracy = (sum(testAccTargetY == YTest)) / mTest
toc;