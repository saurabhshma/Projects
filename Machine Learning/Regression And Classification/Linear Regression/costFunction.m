function J = costFunction(X, Y, Q)
H = X * Q;
J = sum((Y - H) .^ 2) / (2 * size(Y, 1));
end