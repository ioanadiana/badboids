from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np
import yaml
import sys

class Flock(object):
	def __init__(self, configuration):
		self.config=yaml.load(open("config.yaml"))			
		self.positions = self.new_formation(np.array(self.config['no_boids']), np.array(self.config['lower_limits']), np.array(self.config['upper_limits']))
		self.velocities = self.new_formation(np.array(self.config['no_boids']), np.array(self.config['lower_limits_velocities']), np.array(self.config['upper_limits_velocities']))


	def new_formation(self, no_boids, low_limits, up_limits):
		width=up_limits-low_limits
		return (low_limits[:,np.newaxis] + np.random.rand(2, no_boids)*width[:,np.newaxis])

	
	# Fly towards the middle
	def fly_middle(self):

		boids_middle=np.mean(self.positions, 1)
		direction_boids_middle = self.positions-boids_middle[:, np.newaxis]
		self.velocities -= direction_boids_middle * self.config['move_to_middle_strength']
	
	# Fly away from nearby boids
	def fly_away(self):	

		# Compute distances between each boid and the others in a matrix
		displacements = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
		squared_displacements = np.power(displacements,2)
		square_distances = np.sum(squared_displacements, 0)
		too_far = square_distances > self.config['alert_distance']
		separate_if_collide = np.copy(displacements)
		separate_if_collide[0,:,:][too_far] = 0
		separate_if_collide[1,:,:][too_far] = 0
		# Move birds that are about to colide
		self.velocities += np.sum(separate_if_collide,1)
	
	# Try to match speed with nearby boids
	def match_speed(self):

		displacements = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
		squared_displacements = np.power(displacements,2)
		square_distances = np.sum(squared_displacements, 0)	
		velocity_differences = self.velocities[:,np.newaxis,:] - self.velocities[:,:,np.newaxis]
		too_far=square_distances > self.config['boids_flying_distance']
		velocity_differences_if_close = np.copy(velocity_differences)
		velocity_differences_if_close[0,:,:][too_far] = 0
		velocity_differences_if_close[1,:,:][too_far] = 0
		# Match speed for those that are going too far
		self.velocities -=  np.mean(velocity_differences_if_close, 1) * self.config['boids_flying_strength']

	# Move according to velocities
	def update_position(self):
		self.positions+=self.velocities

	# Update position of boids
	def update_boids(self):
		
		# Fly towards the middle					
		self.fly_middle()		
	 	# Fly away from nearby boids
		self.fly_away()
		# Try to match speed with nearby boids
	  	self.match_speed()		
		# Move according to velocities	
		self.update_position()		
		#sys.exit(0)

	# Set position
	def set_positions(self, new_position):
		self.positions = new_position

	# Set velocity
	def set_velocities(self, new_velocity):
		self.velocities = new_velocity


if __name__ == "__main__":
    plt.show()


