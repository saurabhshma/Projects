%compute cost function

function J = logRegCostFunction(X, Y, Q)
htemp = X * Q;
H = sigmoid(htemp);
H = H.';
J = 0;
for i = 1:size(htemp, 1)
  if(Y(i) == 1)
    J = J - log(H(i));
  else
    J = J - log(1 - H(i));
  end;
end;
J = J ./ size(Y, 1);
end;