function s = sigmoid(z)
  s = 1.0 ./ (1.0 + exp(-1 * z));
end