%compute gradient
function gradJ = logRegGradient(X, Y, Q)
htemp = X * Q;
H = sigmoid(htemp);
for i=1:size(Q, 1)
    gradJ(i, 1) = sum((H - Y) .* X(:, i)) / size(Y, 1);
end
end