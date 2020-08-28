"""Damped spring-mass system."""

# Spring-mass system parameters
anchor_pos = 1.5  # anchor position above ground [m]
displacement = 0.4  # mass initial displacement towards ground [m]
mass = 0.3  # mass (m) [kg]
spring_const = 4.5  # spring constant (k) [N/m]
damping_coef = 0.6  # damping coefficient (c) [N*s/m]
gravity = 9.81  # gravitational acceleration (g) [m/s**2]

# Simulation parameters
sim_duration = 10.0  # simulation duration [s]
sim_dt = 0.1  # simulation time step [s]
