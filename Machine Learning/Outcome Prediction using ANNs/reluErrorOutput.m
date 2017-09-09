function value = reluErrorOutput(out, targetY)
  value = (1 - exp(-out)) .* (targetY - out);
end