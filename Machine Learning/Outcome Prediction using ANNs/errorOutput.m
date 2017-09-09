function value = errorOutput(out, targetY)
  value = (1 - out) .* (out) .* (targetY - out);
end