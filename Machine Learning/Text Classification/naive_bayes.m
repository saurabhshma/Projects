tic
data1 = textread('r8-train-all-terms.txt', '%s', 'Delimiter', '\t');
data2 = textread('r8-test-all-terms.txt', '%s', 'Delimiter', '\t');
dataSize1 = length(data1);
dataSize2 = length(data2); 
yIndex = [1:2:dataSize1 - 1];
yIndex2 = [1:2:dataSize2 - 1];
xIndex1 = [2:2:dataSize1];
xIndex2 = [2:2:dataSize2];
X1 = data1(xIndex1);
X2 = data2(xIndex2);
Y = data1(yIndex);
Y2 = data2(yIndex2);
X = [X1; X2];
trainLength = dataSize1 / 2;
testLength = dataSize2 / 2;

%Create dictionary of words using the training samples
[dict, X] = createDictionary(X, length(X));
dictSize = length(dict);
targetY = unique(Y); %Different class of reuters

%Calculate total number of reuters of each class, respective indices, phi, and number of words in each class
for i=1:length(targetY)
  auxY{i} = find(strcmp(Y(:), targetY{i}));
  numOfY(i) = length(auxY{i});
  phi(i) = log(numOfY(i) / trainLength);
  numOfWords(i) = length([X{auxY{i}}]);
end

tempDict = zeros(1, dictSize);
%conditional probability matrix
for i = 1:length(targetY)
  tempA = [(X(auxY{i}){:})];
  [a, ~, c] = unique(tempA);
  [~, ~, temp3] = intersect(a, dict);
  tempDict(temp3) = hist(c, length(a));
  tempDict = log((tempDict + 1) ./ (numOfWords(i) + dictSize));
  condProb{i} = tempDict;
  tempDict(:) = 0;
end

targetIndex = zeros(1, trainLength);
%occurence
for i = 1:trainLength
  tempA = X{i};
  [a, ~, c] = unique(tempA);
  [~, ~, index] = intersect(a, dict);
  counts = hist(c, length(a));
  for j=1:length(targetY)
    probab(j) = sum((condProb{j}(index)) .* counts) + phi(j);
  end
  [~, imax] = max(probab);
  targetIndex(i) = imax;
end

%train Data accuracy
trainAccuracy = sum(strcmp(targetY(targetIndex), Y)) / trainLength

testTargetIndex = zeros(1, testLength);
%occurence
for i = 1:testLength
  tempA = X{i + trainLength};
  [a, ~, c] = unique(tempA);
  [~, ~, index] = intersect(a, dict);
  counts = hist(c, length(a));
  for j=1:length(targetY)
    probab(j) = sum((condProb{j}(index)) .* counts) + phi(j);
  end
  [~, imax] = max(probab);
  testTargetIndex(i) = imax;
end

%test Data accuracy
testAccuracy = sum(strcmp(targetY(testTargetIndex), Y2)) / testLength

%random Data accuracy
randomTestIndex = randi([1,8], 1, testLength);
randomAccuracy = sum(strcmp(targetY(randomTestIndex), Y2)) / testLength

%majority data accuracy
majorityTestIndex(:, 1:testLength) = find(numOfY == max(numOfY));
majorityAccuracy = sum(strcmp(targetY(majorityTestIndex), Y2)) / testLength

%confusion matrix
toc
for i = 1:length(targetY)
  for j = 1:length(targetY)
  confMat(i, j) = length(intersect(find(strcmp(targetY(j), targetY(testTargetIndex))), find(strcmp(targetY(i), Y2))));
  end
end