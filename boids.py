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


# Deliberately terrible code for teaching purposes

boids_x=[random.uniform(-450,50.0) for x in range(no_boids)]
boids_y=[random.uniform(300.0,600.0) for x in range(no_boids)]
boid_x_velocities=[random.uniform(0,10.0) for x in range(no_boids)]
boid_y_velocities=[random.uniform(-20.0,20.0) for x in range(no_boids)]
boids=(boids_x,boids_y,boid_x_velocities,boid_y_velocities)

# Function to generate random flock
def new_formation(no_boids, lower_limits, upper_limits):
	width=upper_limits-lower_limits
	return (lower_limits[:,np.newaxis] + 
		np.random.rand(2, no_boids)*width[:,np.newaxis])

def fly_middle(positions,velocities):

	# Fly towards the middle
	for i in range(no_boids):
		for j in range(no_boids):
			velocities[0,i]+=(positions[0,j]-positions[0,i])*move_to_middle_strength/no_boids
			velocities[1,i]+=(positions[1,j]-positions[1,i])*move_to_middle_strength/no_boids

	return velocities

def fly_away(positions,velocities):

	# Fly away from nearby boids
	for i in range(no_boids):
		for j in range(no_boids):
			if (positions[0,j]-positions[0,i])**2 + (positions[1,j]-positions[1,i])**2 < alert_distance:
				velocities[0,i]+=positions[0,i]-positions[0,j]
				velocities[1,i]+=positions[1,i]-positions[1,j]

	return velocities

def match_speed(positions, velocities):

	# Try to match speed with nearby boids
	for i in range(no_boids):
		for j in range(no_boids):
			if (positions[0,j]-positions[0,i])**2 + (positions[1,j]-positions[1,i])**2 < formation_flying_distance:
				velocities[0,i]+=(velocities[0,j]-velocities[0,i])*formation_flying_strength/no_boids
				velocities[1,i]+=(velocities[1,j]-velocities[1,i])*formation_flying_strength/no_boids

	return velocities

def update_position(positions, velocities):

	for i in range(no_boids):
		positions[0,i]+=velocities[0,i]
		positions[1,i]+=velocities[1,i]

	return positions

def update_boids(positions, velocities):

	# Fly towards the middle
  	velocities = fly_middle(positions,velocities)

 	# Fly away from nearby boids
  	velocities = fly_away(positions,velocities)

 	# Try to match speed with nearby boids
  	velocities = match_speed(positions,velocities)

	# Move according to velocities
	positions = update_position(positions,velocities)

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
