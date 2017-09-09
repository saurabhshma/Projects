clear all;
X = load('q4x.dat');
X = X - mean(X);
X = X ./ std(X); 
Y = textread('q4y.dat', '%s', 'delimiter','\n');

pos_index = strmatch('Alaska', Y);
neg_index = strmatch('Canada', Y);

%mean
u0 = [mean(X(pos_index, 1)); mean(X(pos_index, 2))];
u1 = [mean(X(neg_index, 1)); mean(X(neg_index, 2))];

%covariance matrix (sigma1 ~= sigma2)
for(i=1:size(X, 2))
  for(j=1:size(X, 2))
    cov0(i, j) = covariance(X(pos_index, i), X(pos_index, j), u0(i), u0(j));
    cov1(i, j) = covariance(X(neg_index, i), X(neg_index, j), u1(i), u1(j)); 
  end;
end;

%covariance matrix (sigma1 = sigma2 = sigma)
for(i=1:size(X, 2))
  for(j=1:size(X, 2))
    c = 0;
    for(k=1:size(X, 1))
      if(strcmp(Y(k), 'Alaska'))
        c = c + (((X(k, i) - u0(i))) .* (X(k, j) - u0(j)));
      else
        c = c + (((X(k, i) - u1(i))) .* (X(k, j) - u1(j)));
      end;
    end;
   cov(i, j) = c ./ size(X, 1); 
  end;
end;

%decision boundary
%sigma1 = sigma2 = sigma
temp1 = (u0.' * inv(cov) * u0) ./ 2;
temp2 = (u1.' * inv(cov) * u1) ./ 2;
temp3 = inv(cov) * u1;
temp4 = inv(cov) * u0;
temp5 = log((size(pos_index, 1)) ./ (size(neg_index, 1)));
x = sortrows(X(:, 1));
plot_y = ((temp3(1) - temp4(1))/ (temp4(2) - temp3(2))) .* x + temp5 + temp1 - temp2;

%sigma1 ~= sigma2
tempC = log((det(cov0) .* size(pos_index, 1)) ./ (det(cov1) .* size(neg_index, 1))) + (u0.' * inv(cov0) * u0) - (u1.' * inv(cov1) * u1);
A = inv(cov1) - inv(cov0);
B = (inv(cov1) * u1) - (inv(cov0) * u0);
P =  (x .* A(1, 2) + x .* A(2, 1) - 2 * B(2)) ./ A(2, 2);
Q = (((x.^2) .* A(1, 1)) - (2 .* x .* B(1)) - tempC) ./ A(2, 2);
plot_yy = (-P .+ sqrt((P .^ 2) - (4 .* Q))) ./ 2;

%plot Figures
figure();
hold on;
plot(X(pos_index, 1), X(pos_index, 2), '+', 'color', 'b');
plot(X(neg_index, 1), X(neg_index, 2), 'o', 'color', 'r');
plot(x, plot_y, 'm', 'LineWidth', 2);
plot(x, plot_yy, 'g', 'LineWidth', 2);
legend('Alaska', 'Canada');
hold off;
