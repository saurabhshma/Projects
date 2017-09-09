srcFiles = dir(fullfile('*.jpg'));
m = length(srcFiles);
XTrainColor = zeros(length(srcFiles), 1850, 'uint8');
for i = 1 : m
    XTrainColor(i, :) = reshape(rgb2gray(imread(srcFiles(i).name)), [1, 1850]);
end