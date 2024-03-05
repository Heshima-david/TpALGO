# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 07:02:47 2024

@author: LENOVO
"""
# Constants
m = 10  # kg
k = 4000  # N/m
alpha = 20  # Ns/m
x0 = 0.01  # m
v0 = 0  # m/s
F0 = 100  # N
omega = 10  # rad/s

# Time parameters
dt = 0.01
t = np.arange(0, 10, dt)

# Function to solve the differential equation of the system
def solve_differential_eqn(x, v, t, F):
    dxdt = v
    dvdt = (F - k*x - alpha*v) / m
    return dxdt, dvdt

# Function to calculate kinetic energy (Ec), potential energy (Ep), and mechanical energy (Em)
def calculate_energy(x, v):
    Ec = 0.5 * m * v**2
    Ep = 0.5 * k * x**2
    Em = Ec + Ep
    return Ec, Ep, Em

# Initialize arrays to store values
x_values = np.zeros_like(t)
v_values = np.zeros_like(t)
Ec_values = np.zeros_like(t)
Ep_values = np.zeros_like(t)
Em_values = np.zeros_like(t)

# Initial conditions
x_values[0] = x0
v_values[0] = v0

# Solve the differential equation and calculate energy at each time step
for i in range(1, len(t)):
    F = F0 * np.cos(omega * t[i])
    dx, dv = solve_differential_eqn(x_values[i-1], v_values[i-1], t[i], F)
    x_values[i] = x_values[i-1] + dx * dt
    v_values[i] = v_values[i-1] + dv * dt
    
    Ec_values[i], Ep_values[i], Em_values[i] = calculate_energy(x_values[i], v_values[i])

# Plotting the results for case (a)
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, x_values, label='Displacement (m)')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, Ec_values, label='Kinetic Energy')
plt.plot(t, Ep_values, label='Potential Energy')
plt.plot(t, Em_values, label='Mechanical Energy')
plt.xlabel('Time (s)')
plt.ylabel('Energy')
plt.legend()

plt.tight_layout()
plt.show()