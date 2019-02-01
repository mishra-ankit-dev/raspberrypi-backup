function U = min(X, y, theta)
  i=0;
  m = size(X,1);
  alpha = 0.01;
  while(i <100000) 
    pridictions = theta' * X;
    difference = pridictions - y;
    d = (1/m) * alpha* ((difference) * X');
    size(d);
    theta = theta- d';
    U = theta;
    sqrErrors = difference.^2;
    J= 1/(2*m) *   sum(sqrErrors);
    i = i+1;
  end;