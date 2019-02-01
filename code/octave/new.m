function K= new(X,y,theta)
  i=0;
  m = size(X,1);
  alpha = 0.02;
  while(i <10000) 
    d = (alpha/m) * (X' * (X*theta -y));
    tempChange = zeros(length(theta), 1);
    tempChange = theta - d;
    theta=tempChange;
    K=theta;
    
    i=i+1;
  end;