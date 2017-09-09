tic;
XTrainGray = importdata('XTrainGray.mat');
%imshow(reshape(XTrainGray(1, :), [112, 92]));
m = size(XTrainGray, 1);
n = size(XTrainGray, 2);
meanX = uint8(sum(XTrainGray, 1) ./ m);
avgFaceGray = reshape(meanX, [112, 92]);
imshow(avgFaceGray);
for i=1:m
    XTrainGray(i, :) = XTrainGray(i, :) - meanX;
end
XTrainGray = double(XTrainGray);
%imshow(reshape(XTrainGray(1, :), [112, 92]));
[~, ~, eigenVectors] = svd(XTrainGray);
for i=1:50
    top50EigenGray(:, i) = eigenVectors(:, i);
end
%save('top50Eigen');
for i=1:5
    temp = top50EigenGray(:, i);
    temp = temp - min(temp);
    temp = temp ./ (max(temp) - min(temp));
    temp = temp*255;
    figure();
    imshow(uint8(reshape(temp, [112, 92])));
end
toc;
projectedX = XTrainGray * top50EigenGray;