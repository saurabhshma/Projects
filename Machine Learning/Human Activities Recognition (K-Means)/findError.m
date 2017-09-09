function error = findError(X, XLabels, Means)
  error = 0;
  for j=1:size(Means, 1)
    temp = X((XLabels == j), :);
    for(i=1:size(temp, 1))
        temp(i, :) = temp(i, :) - Means(j, :);
    end
    error = error + sum(sum(temp.^2, 2));    
  end
end