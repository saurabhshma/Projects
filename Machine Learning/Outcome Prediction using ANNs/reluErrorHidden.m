function value = reluErrorHidden(outError, hiddenWeights, outHidden)
  value = (1 - exp(-outHidden)) .* (hiddenWeights' * outError');
end