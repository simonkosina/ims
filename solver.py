# %%
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# %%
# S(lambda - beta*S*I - alpha*S - mu*S, (double) S0),
# E(beta*S*I - GAMMA*E + sigma*beta*V*I - mu*E, (double) E0),
# I(GAMMA*E - DELTA*I - mu*I, (double) I0),
# Q(delta*I - (1 - kappa)*THETA*Q - kappa*RHO*Q - mu*Q, (double) Q0),
# R((1 - kappa)*theta*Q - mu*R, (double) R0),
# D(kappa*rho*Q, (double) D0),
# V(alpha*S - sigma*beta*V*I - mu*V, (double) V0) {}

S0 = 34_217_993
E0 = 3
I0 = 3
Q0 = 1
R0 = 0
D0 = 0
V0 = 0

LAMBDA = 0
BETA = 0.000000073 
ALPHA = 0.000035 
MU = 0.00003
GAMMA = (1.0/5.5)  
SIGMA = 0.05 
DELTA = (1.0/3.8)  
KAPPA = 0.014
THETA = (1.0/10)
RHO = (1.0/15)

# d[0] = S
# d[1] = E
# d[2] = I
# d[3] = Q
# d[4] = R
# d[5] = D
# d[6] = V

def rhs(t, d):
    return [
        LAMBDA - BETA*d[0]*d[2] - ALPHA*d[0] - MU*d[0],
        BETA*d[0]*d[2] - GAMMA*d[1] + SIGMA*BETA*d[6]*d[2] - MU*d[1],
        GAMMA*d[1] - DELTA*d[2] - MU*d[2],
        DELTA*d[2] - (1 - KAPPA)*THETA*d[3] - KAPPA*RHO*d[3] - MU*d[3],
        (1 - KAPPA)*THETA*d[3] - MU*d[4],
        KAPPA*RHO*d[3],
        ALPHA*d[0] - SIGMA*BETA*d[6]*d[2] - MU*d[6],
    ]

# %%

res = solve_ivp(rhs, (0, 180), [S0, E0, I0, Q0, R0, D0, V0])

# %%
plt.plot(res.t, res.y.T)


# %%
