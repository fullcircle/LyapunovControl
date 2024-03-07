import simpy
import numpy as np

CONTAINER_CAPACITY = 100

# Define the dynamical system
def dynamical_system(env, state, A):
    while True:
        # System dynamics: x' = Ax
        delta_level = A * state.level * env.now
        state.put(abs(delta_level+.1))  # Update using the absolute value
        yield env.timeout(1)

# Define the Lyapunov function
def lyapunov_function(x):
    # Example Lyapunov function: V(x) = |x|
    return (x*x)

# Check the stability using the Lyapunov function
def check_stability(env, state):
    while True:
        # Calculate the Lyapunov function value
        current_level = state.level
        V = lyapunov_function(current_level)
        # Check if the Lyapunov condition is met: V >= 0
        if V >= 0:
            print(f"System is stable at time {env.now}")
        else:
            print(f"System is unstable at time {env.now}")
        yield env.timeout(1)

# Initialize the simpy environment
env = simpy.Environment()

# Initial level of the system (scalar)
initial_level = 10.0

# System matrix (should be stable for the Lyapunov function to work)
A = -1.0

# Create a shared state object
state = simpy.Container(env, CONTAINER_CAPACITY, init=initial_level)

# Start the process
env.process(dynamical_system(env, state, A))
env.process(check_stability(env, state))

# Run the simulation for a specified time
simulation_time = 10  # Adjust as needed
env.run(until=simulation_time)
