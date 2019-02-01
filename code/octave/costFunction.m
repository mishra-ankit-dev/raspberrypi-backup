function J = costFunction(X, y, theta)
  m = size(X,1)
  pridictions = theta'*X;
  sqrErrors = (pridictions-y).^2;
  size(sqrErrors)
  J = 1/(2*m) * sum(sqrErrors);
  size(J)
  end;