%compute covariance matrix
function c = covariance(x1, x2, mean1, mean2)
    c =(((x1 - mean1)).' * (x2 - mean2)) / size(x1, 1);
end;