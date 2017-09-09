
tempDict = zeros(1, dictSize);
%conditional probability matrix
for i = 1:size(targetY, 1)
  temp = auxY{i};
  for j = 1:size(temp, 1)
    tempDict = tempDict + ismember(dict, X{temp(j)});
  end
  condProb{i} = tempDict;
  tempDict(:) = 0;
end