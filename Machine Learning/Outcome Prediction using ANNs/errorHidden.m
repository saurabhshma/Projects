function value = errorHidden(outError, hiddenWeights, outHidden)
  value = (outHidden .* (1 - outHidden)) .* (hiddenWeights' * outError');
end