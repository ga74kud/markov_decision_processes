import numpy as np
sigma_x=3
sigma_y=3
rho=0
mu_x=3
mu_y=3
x=4
y=4

factor_A=1/(2*np.pi*sigma_x*sigma_y*np.sqrt(1-rho**2))
exp_factor_A=-1/(2*(1-rho**2))
exp_factor_B=((x-mu_x)/sigma_x)**2-2*rho*((x-mu_x)/(sigma_x))*((y-mu_y)/(sigma_y))+((y-mu_y)/sigma_y)**2

factor_B=np.exp(exp_factor_A*exp_factor_B)

f=factor_A*factor_B
print(f)

