function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters
    
    %theta_T_x * theta_x 	    
    theta = theta - ((alpha/m) .* (X' * ((X*theta) .- y)));
    J_history(iter) = computeCost(X, y, theta);
    
    %fprintf('Theta 1 = %f; theta 2 = %f\n', theta(1), theta(2))
    %plot(X, X*theta, '-','color','r');

end

end

