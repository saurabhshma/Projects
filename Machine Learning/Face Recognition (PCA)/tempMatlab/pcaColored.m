tic;
XTrainColor = importdata('XTrainColor.mat');
%imshow(reshape(XTrainGray(1, :), [112, 92]));
m = size(XTrainColor, 1);
n = size(XTrainColor, 2);
meanX = uint8(sum(XTrainColor, 1) ./ m);
avgFaceGray = reshape(meanX, [50, 37]);
imshow(avgFaceGray);
for i=1:m
    XTrainColor(i, :) = XTrainColor(i, :) - meanX;
end
XTrainColor = double(XTrainColor);
%imshow(reshape(XTrainGray(1, :), [112, 92]));
[~, ~, eigenVectors] = svd(XTrainColor);
for i=1:50
    top50EigenColor(:, i) = eigenVectors(:, i);
end
%save('top50Eigen');
for i=1:5
    temp = top50EigenColor(:, i);
    temp = temp - min(temp);
    temp = temp ./ (max(temp) - min(temp));
    temp = temp*255;
    figure();
    imshow(uint8(reshape(temp, [50, 37])));
end
toc;
projectedX = XTrainColor * top50EigenColor;
%%reconstructed
%projectedImages = projectedX * top50Eigen';
%do scaling