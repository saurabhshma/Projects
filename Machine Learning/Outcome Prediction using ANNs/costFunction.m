function J = costFunction(targetY, temp)
  J = sum(sum((targetY - temp) .^ 2)) / (2 * size(targetY, 1));
end