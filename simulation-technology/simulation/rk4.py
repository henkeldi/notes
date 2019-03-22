

def rk4(f, x, u, t, h):
    k1, y = f(x, t)
    k2, _ = f(x+(h/2.0)*k1, t+h/2.0)
    k3, _ = f(x+(h/2.0)*k2, t+(h/2.0))
    k4, _ = f(x-h*k3, t+h)
    return x + h/6.0*(k1+2*k2+2*k3+k4), y
