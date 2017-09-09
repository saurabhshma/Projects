%compute hessian matrix
function hessJ = logRegHessian(X, Y, Q)
  htemp = X * Q;
  tempJ = sigmoid(htemp) .* (1 - sigmoid(htemp));
  for(i = 1:size(Q, 1))
    for(j = 1:size(Q, 1))
      temp = 0;
      for(k = 1:size(Y, 1))
        temp = temp + (tempJ(k, 1) * X(k, i)* X(k, j));
      end
      hessJ(i, j) = temp;
    end
  end
  hessJ = (1/size(Y, 1)) .* hessJ; 
end