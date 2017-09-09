srcFiles = dir(fullfile('*.pgm'));
XTrainGray = zeros(length(srcFiles), 10304, 'uint8');
YTrainGray = zeros(length(srcFiles), 1, 'uint8');
for i = 1 : length(srcFiles)
    %YTrainGray(i) = str2num(srcFiles(i).name(1));
    XTrainGray(i, :) = reshape(imread(srcFiles(i).name), [1, 10304]);
end