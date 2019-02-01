function J = log(X,y,theta)
  i=0;
  m=size(X,2);
  alpha= 0.01;
  while(i<100)
    prediction = 1/(ones(1,6)+e.**(theta'*X));
    d = (alpha/m) *(X' * (prediction- y));
    temp = zeros(length(theta),1);
    temp = theta-d;
    theta = temp;
    J=theta;
  end;