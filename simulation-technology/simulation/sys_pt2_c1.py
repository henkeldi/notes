
import numpy as np

import system


def sys_pt2_c1(x, t):
    """Topology description of simulation model.

    Args:
      x: system state vector at t
      t: current time

    Returns:
      xdot: system state vector derivative at t
      y: subsystem outputs at t
    """
    # u_ext = u_ext(t) # modeled as internal part of the system
    ts = 1.0
    if t < ts:
        u_ext = 0.0
    elif t >= ts:
        u_ext = 1.0
    else:
        u_ext = 0.0

    xdot = np.empty(2)
    u1 = np.empty(2)
    y = np.empty(3)

    # system_3 ---> Start block
    # xdot undefined because input u3 not yet known
    _, y3_start = system.system_3([x[1]], [0.0], t)

    # system_1
    u1 = np.array([u_ext, y3_start])
    _, y[0] = system.system_1([0], u1, t)  # no states

    # system_2
    u2 = np.array([y[0]])
    xdot[0], y[1] = system.system_2([x[0]], u2, t)

    # system_3
    # xdot is now correct because the input is known
    u3 = np.array([y[1]])
    xdot[1], y[2] = system.system_3([x[1]], u3, t)

    return xdot, y
