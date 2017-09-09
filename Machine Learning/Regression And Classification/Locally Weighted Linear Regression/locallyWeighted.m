X = csvread('q3x.dat');
Y = csvread('q3y.dat');
X = [ones(size(X, 1), 1) X];

%Normal Equation
Q = pinv(X.' * X) * X.' * Y;
tempY = X * Q;
figure();
hold on;
scatter(X(:, 2), Y, 'b', '.');
plot(X(:, 2), tempY, 'r', 'LineWidth', 2);
title('Hypothesis Function');
xlabel('X');
ylabel('Y');
hold off;

%locally weighted linear regression
T = 10; %Bandwidth Parameter
W = zeros(size(X, 1), size(X, 1));
for k=1:size(X, 1)
    for i=1:size(X, 1)
        W(i, i) = (1 / exp(((X(k, 2) - X(i, 2)) ^ 2)/ (2 * T^2))); 
    end
    Xtrans = X.';
    tempQ = pinv(Xtrans * W * X) * Xtrans * W * Y;
    plotTheta(1, k) = tempQ(1);
    plotTheta(2, k) = tempQ(2);
end
for i = 1:size(X, 1)
    tempY(i) = X(i, 1) * plotTheta(1, i) + X(i, 2) * plotTheta(2, i);
end;

plotTemp = [X(:, 2) tempY];
plotTemp = sortrows(plotTemp);

figure();
hold on;
scatter(X(:, 2), Y, 'b', '.');
plot(plotTemp(:, 1), plotTemp(:, 2), 'r', 'LineWidth', 2);
title('Hypothesis Function');
xlabel('X');
ylabel('Y');
hold off;