function index = findLabel(X, Means)
    temp = repmat(X, 6, 1) - Means;
    [~, index] = min(sum(temp.^2, 2));
end