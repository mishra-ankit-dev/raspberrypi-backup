function U = minOfCostFunction(X, y, theta)
  %A=X(2,:);
  i=0;
  m = size(X,1);
  alpha = 0.1;
  while(i <1000) 
    pridictions = theta' * X;
    difference = pridictions - y;
    d = (1/m) * ((difference) * X');
    size(d);
    temp = theta- alpha * d';
    theta = temp;
    U = theta;
    sqrErrors = difference.^2;
    J= 1/(2*m) *   sum(sqrErrors);
    i = i+1;
  end;