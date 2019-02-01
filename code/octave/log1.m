function [J, grad] = costFunction(theta, X, y)
hx = sigmoid(X * theta);
m = length(X);

J = (-y' * log(hx) - (1 - y')*log(1 - hx)) / m;
grad = X' * (hx - y) / m;

end