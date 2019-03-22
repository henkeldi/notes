import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from rk4 import rk4
from sys_pt2_c1 import sys_pt2_c1

mpl.rcParams['font.size'] = 14

# system parameter
model = sys_pt2_c1
u = [0.0]  # input modelled in the topology file

# simulation parameter
t = 0.0
tf = 5.0
h = 1e-2
ts = 1.0

# initial values
x = np.array([0.0, 0.0])  # x ... system state vector

# simulation
t_values = np.arange(t, tf+h, h)
N = len(t_values)
x_values = np.zeros((N, x.shape[0]))
y_values = np.zeros((N, 3))
y_exact = np.zeros((N))

for i, t in enumerate(t_values):
    (x, y) = rk4(model, x, u, t, h)
    x_values[i, :] = x
    y_values[i, :] = y
    y_exact[i] = 0.0 if t <= ts else (29.0 / 49.0) *\
        (1.0-math.exp(-3.5*(t-ts))*(np.cos(3.5*(t-ts)) + np.sin(3.5*(t-ts))))

plt.plot(t_values, y_values[:, 2])
plt.plot(t_values, y_exact)
plt.xlabel(r'$\frac{t}{s}$')
plt.ylabel('$y$')

plt.legend(['simulation', 'ground truth'])
plt.grid()
plt.tight_layout()
plt.savefig('step_response.svg')
# plt.show()
