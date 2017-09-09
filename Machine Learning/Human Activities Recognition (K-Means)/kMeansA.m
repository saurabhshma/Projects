XTrain = importdata('attr.txt');
YTrain = importdata('label.txt');
m = size(XTrain, 1);
jOld = realmax;
jNew = realmin;
XTrainLabels = zeros(m, 1);
k = 6;
means = XTrain(randi(m, k, 1), :);
t = 0; 
epsilon = 0.001;
tic;
while((jOld - jNew) > epsilon)
  if(t ~= 0)
    jOld = jNew;
  end
  for i=1:m
      XTrainLabels(i) = findLabel(XTrain(i, :), means);
  end
  for j=1:k
    temp = find(XTrainLabels == j);
    means(j, :) = sum(XTrain(temp, :), 1) ./ length(temp);
  end
  jNew = findError(XTrain, XTrainLabels, means)
  t = t + 1
  jOld - jNew
end
toc;