X = load('q2x.dat');
Y = load('q2y.dat');
X = [ones(size(X, 1), 1) X];
Q = zeros(size(X, 2), 1);

gradJ = logRegGradient(X, Y, Q);
hessJ = logRegHessian(X, Y, Q);

t = 0; %number of iterations
while(gradJ ~= 0)
  cost = logRegCostFunction(X, Y, Q);
  Q = Q - (pinv(hessJ) * gradJ); %Newton's update
  gradJ = logRegGradient(X, Y, Q);
  hessJ = logRegHessian(X, Y, Q);
  t = t + 1;
end
Q
gradJ
hessJ

plot_x = X(:,2);
plot_x = sortrows(plot_x);
y = (Q(2) .* plot_x + Q(1)) ./ (-Q(3));

pos_index = find(Y == 1);
neg_index = find(Y == 0);

%plot data points and decision boundary
figure();
hold on;
plot(X(pos_index, 2), X(pos_index, 3), '+', 'color', 'b');
plot(X(neg_index, 2), X(neg_index, 3), 'o', 'color', 'r');
plot(plot_x, y, 'LineWidth', 2);
title('Decision Boundary');
legend('Class 1', 'Class 2');
hold off;
