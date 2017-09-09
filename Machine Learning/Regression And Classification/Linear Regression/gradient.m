function gradJ = gradient(X, Y, Q)
H = X * Q;
gradJ = (X' * (Y - H)) / size(Y, 1);
end