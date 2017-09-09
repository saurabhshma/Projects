clear all;
alpha = 2.1; %learning rate
t = 0; %number of iterations
X = csvread('q1x.dat');
Y = csvread('q1y.dat');
X = (X - mean(X)) / std(X);  %normalise the data
Q = zeros(size(X, 2) + 1, 1);
plotTheta = Q;

X = [ones(size(X, 1), 1) X];
epsilon = 0.0001;
costPrev = realmax;
cost = costFunction(X, Y, Q); %cost function value
plotCost = cost;
while((costPrev - cost) > epsilon)
    Q = Q + alpha * gradient(X, Y, Q);
    plotTheta = [plotTheta Q];
    costPrev = cost
    cost = costFunction(X, Y, Q)
    plotCost = [plotCost, cost];
    t = t + 1;
end
t
cost
Q
plotTheta
plotCost

theta1 = plotTheta(1, :);
theta2 = plotTheta(2, :);

tempY = X * Q;

%Plot hypothesis function
figure();
hold on;
scatter(X(:, 2), Y, 'b', '.');
plot(X(:, 2), tempY, 'r', 'LineWidth', 2);
title('Hypothesis Function');
xlabel('X');
ylabel('Y');
hold off;

%Function to plot Contour and Mesh
[A, B] = meshgrid(-3:0.2:8, -3:0.2:8);
for i=1:size(A, 1)
    for j=1:size(A, 2)
        Z(i,j) = costFunction(X, Y, [A(i, j); B(i, j)]);
    end;
end;

%Plot mesh grid
figure();
view([-37.5 -30]);
hold on;
mesh([-3:0.2:8], [-3:0.2:8], Z);
title('Cost Function vs Theta mesh');
for i=1:size(theta1, 2)
    plot3(theta1(i), theta2(i), plotCost(i), 'ro', 'color', 'r', 'MarkerSize', 7);
    pause(0.2);
end
hold off;

figure();
hold on;
contour([-3:0.2:8], [-3:0.2:8], Z);
title('Cost Function vs Theta contour');
for i=1:size(theta1, 2)
    plot3(theta1(i), theta2(i), plotCost(i), 'ro', 'color', 'r');
    pause(0.5);
end
hold off;



