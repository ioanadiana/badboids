"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np

# Constants
no_boids = 50;
move_to_middle_strength = 0.01;
alert_distance = 100;
formation_flying_distance = 10000;
formation_flying_strength = 0.125;

# Define limits 
upper_limits = np.array([50.0,600.0])
lower_limits = np.array([-450.0,300.0])
upper_limits_velocities = np.array([10.0,20.0])
lower_limits_velocities = np.array([0,-20.0])

# Function to generate random flock
def new_formation(no_boids, lower_limits, upper_limits):
	width=upper_limits-lower_limits
	return (lower_limits[:,np.newaxis] + 
		np.random.rand(2, no_boids)*width[:,np.newaxis])


# Fly towards the middle
def fly_middle(positions,velocities):

	boids_middle=np.mean(positions, 1)
	direction_boids_middle = positions-boids_middle[:, np.newaxis]
	velocities -= direction_boids_middle * move_to_middle_strength


# Fly away from nearby boids
def fly_away(positions,velocities):	

	# Fly away from nearby boids
	for i in range(no_boids):
		for j in range(no_boids):
			separation = positions[:,j] - positions[:,i]
			squared_displacement = separation * separation
			distance = np.sum(squared_displacement, 0)
			if distance < alert_distance:
				velocities[:,i]-=separation



# Try to match speed with nearby boids
def match_speed(positions, velocities):

	
	# Try to match speed with nearby boids
	for i in range(no_boids):
		for j in range(no_boids):
			separation = positions[:,j] - positions[:,i]
			squared_displacement = separation * separation
			distance = np.sum(squared_displacement, 0)
			if distance < formation_flying_distance:
				velocities[:,i]+=(velocities[:,j]-velocities[:,i])*formation_flying_strength/no_boids
				


# Update position
def update_position(positions, velocities):
	positions+=velocities

def update_boids(positions, velocities):

	# Fly towards the middle
  	fly_middle(positions,velocities)

 	# Fly away from nearby boids
  	fly_away(positions,velocities)

 	# Try to match speed with nearby boids
  	match_speed(positions,velocities)

	# Move according to velocities
	update_position(positions,velocities)

# Initialise flock
positions = new_formation(no_boids, lower_limits, upper_limits)	
velocities = new_formation(no_boids, lower_limits_velocities, upper_limits_velocities)

figure=plt.figure()
axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
scatter=axes.scatter(positions[0,:],positions[1,:])

def animate(frame):
   # np.column_stack((positions,velocities))
   update_boids(positions, velocities)
   scatter.set_offsets(zip(positions[0,:],positions[1,:]))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)



if __name__ == "__main__":
    plt.show()
