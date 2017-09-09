XTrain = importdata('attr.txt');
YTrain = importdata('label.txt');
m = size(XTrain, 1);
n = 10;
k = 6;
J = zeros(n, 1);
randInit = zeros(n, k);
tic;
for numIter=1:10
    XTrainLabels = zeros(m, 1);
    randInit(numIter, :) = randi(m, k, 1);
    means = XTrain(randInit(numIter, :), :);
    for(t=1:60)
      for i=1:m
          XTrainLabels(i) = findLabel(XTrain(i, :), means);
      end
      for j=1:k
        temp = find(XTrainLabels == j);
        means(j, :) = sum(XTrain(temp, :), 1) ./ length(temp);
      end
      jNew = findError(XTrain, XTrainLabels, means)
    end
    t
    J(numIter, 1) = jNew;
end
toc;
tic;
[~, index] = min(J);
plotJ = zeros(60, 1);
plotAcc = zeros(60, 1);
means = XTrain(randInit(index, :), :);
XTrainLabels = zeros(m, 1);
for t=1:60
  accLabels = 0;
  for i=1:m
      XTrainLabels(i) = findLabel(XTrain(i, :), means);
  end
  for j=1:k
    temp = find(XTrainLabels == j);
    accLabels = accLabels + sum(mode(YTrain(temp)) == YTrain(temp));
    means(j, :) = sum(XTrain(temp, :), 1) ./ length(temp);
  end
  accLabels = accLabels / m;
  jNew = findError(XTrain, XTrainLabels, means);
  plotJ(t) = jNew;
  plotAcc(t) = accLabels;
end
toc;
t = [1:1:60];
figure();
plot(t, plotJ, 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Cost');
title('Cost vs Number of iterations');

figure();
plot(t, plotAcc, 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Accuracy');
title('Accuracy vs Number of iterations');


