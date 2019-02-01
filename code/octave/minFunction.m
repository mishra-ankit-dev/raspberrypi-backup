function J = minFunction(X, y, theta)
m = size(X,1)
pridictions = theta' * X ;
delta = (1/m) * [(pridictions - y) * X];
alpha = 0.005;
temp = theta - alpha * delta;
theta = temp;
J = theta;