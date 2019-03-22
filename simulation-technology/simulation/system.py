
import numpy as np


def system_1(x, u, t):
    k = 29.0 / 24.0

    # state equation (derivative)
    xdot = np.array([0.0])  # no states, dummy output

    # output equation
    y = np.array([k * (u[0]-u[1])])

    return xdot, y


def system_2(x, u, t):
    # state equation (derivative)
    xdot = np.array([-5.0 * x[0] + u[0]])

    # output equation
    y = np.array([3.0 * x[0]])

    return xdot, y


def system_3(x, u, t):
    # state equation (derivative)
    xdot = np.array([-2.0*x[0] + u[0]])

    # output equation
    y = np.array([4.0*x[0]])

    return xdot, y
