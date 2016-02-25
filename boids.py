"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np
import yaml

config=yaml.load(open("config.yaml"))

# Define limits 
upper_limits = np.array(config['upper_limits'])
lower_limits = np.array(config['lower_limits'])
upper_limits_velocities = np.array(config['upper_limits_velocities'])
lower_limits_velocities = np.array(config['lower_limits_velocities'])

# Function to generate random flock
def new_formation(no_boids, low_limits, up_limits):
	width=up_limits-low_limits
	return (low_limits[:,np.newaxis] + 
		np.random.rand(2, no_boids)*width[:,np.newaxis])


# Fly towards the middle
def fly_middle(positions,velocities):

	boids_middle=np.mean(positions, 1)
	direction_boids_middle = positions-boids_middle[:, np.newaxis]
	velocities -= direction_boids_middle * config['move_to_middle_strength']


# Fly away from nearby boids
def fly_away(positions,velocities):	

	# Compute distances between each boid and the others in a matrix
	displacements = positions[:,np.newaxis,:] - positions[:,:,np.newaxis]
	squared_displacements = np.power(displacements,2)
	square_distances = np.sum(squared_displacements, 0)
	too_far = square_distances > config['alert_distance']
	separate_if_collide = np.copy(displacements)
	separate_if_collide[0,:,:][too_far] = 0
	separate_if_collide[1,:,:][too_far] = 0
	# Move birds that are about to colide
	velocities += np.sum(separate_if_collide,1)

# Try to match speed with nearby boids
def match_speed(positions, velocities):

    displacements = positions[:,np.newaxis,:] - positions[:,:,np.newaxis]
    squared_displacements = np.power(displacements,2)
    square_distances = np.sum(squared_displacements, 0)	
    velocity_differences = velocities[:,np.newaxis,:] - velocities[:,:,np.newaxis]
    too_far=square_distances > config['boids_flying_distance']
    velocity_differences_if_close = np.copy(velocity_differences)
    velocity_differences_if_close[0,:,:][too_far] = 0
    velocity_differences_if_close[1,:,:][too_far] = 0
	# Match speed for those that are going too far
    velocities -=  np.mean(velocity_differences_if_close, 1) * config['boids_flying_strength']
				

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
positions = new_formation(config['no_boids'], lower_limits, upper_limits)	
velocities = new_formation(config['no_boids'], lower_limits_velocities, upper_limits_velocities)

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
