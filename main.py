import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Drag coefficient, projectile radius (m), area (m2) and mass (kg).
c = 0.47
r = 0.05
A = np.pi * r**2
m = 0.2
# Air density (kg.m-3), acceleration due to gravity (m.s-2).
rho_air = 1.28
g = 9.81
# For convenience, define this constant.
k = 0.05 * c * rho_air * A

# Initial speed and launch angle (from the horizontal).
v0 = 469
phi0 = np.radians(0)

def deriv(t, u):
    x, xdot, y, ydot = u
    speed = np.hypot(xdot, ydot)  # calculates the magnitude (speed) of a two-dimensional vector
    xdotdot = -k/m * speed * xdot
    ydotdot = -k/m * speed * ydot - g
    return xdot, xdotdot, ydot, ydotdot

# Initial conditions: x0, v0_x, y0, v0_y.
u0 = 0, v0 * np.cos(phi0), 1096., v0 * np.sin(phi0)
# Integrate up to tf unless we hit the target sooner.
t0, tf = 0, 100

def hit_target(t, u):
    # We've hit the target if the y-coordinate is 0.
    return u[2]
# Stop the integration when we hit the target.
hit_target.terminal = True
# We must be moving downwards
hit_target.direction = -1

def max_height(t, u):
    # The maximum height is obtained when the y-velocity is zero.
    return u[3]

soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True,
                 events=(hit_target, max_height))

print(soln)
print('Time to target = {:.2f} s'.format(soln.t_events[0][0]))
print('Time to highest point = {:.2f} s'.format(soln.t_events[1][0]))

# A fine grid of time points from 0 until impact time.
t = np.linspace(0, soln.t_events[0][0], 100)

# Retrieve the solution for the time grid and plot the trajectory.
sol = soln.sol(t)
x, y = sol[0], sol[2]
print('Range to target, xmax = {:.2f} m'.format(x[-1]))
print('Maximum height, ymax = {:.2f} m'.format(max(y)))
plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 12})
plt.plot(x, y)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.show()