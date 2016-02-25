"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random

# Constants
no_boids = 50;
move_to_middle_strength = 0.01;
alert_distance = 100;
formation_flying_distance = 10000;
formation_flying_strength = 0.125;


# Deliberately terrible code for teaching purposes

boids_x=[random.uniform(-450,50.0) for x in range(no_boids)]
boids_y=[random.uniform(300.0,600.0) for x in range(no_boids)]
boid_x_velocities=[random.uniform(0,10.0) for x in range(no_boids)]
boid_y_velocities=[random.uniform(-20.0,20.0) for x in range(no_boids)]
boids=(boids_x,boids_y,boid_x_velocities,boid_y_velocities)

def fly_middle(position_x,position_y,velocity_x,velocity_y):
	# Fly towards the middle
	for i in range(len(position_x)):
		for j in range(len(position_x)):
			velocity_x[i]=velocity_x[i]+(position_x[j]-position_x[i])*move_to_middle_strength/len(position_x)
	for i in range(len(position_x)):
		for j in range(len(position_x)):
			velocity_y[i]=velocity_y[i]+(position_y[j]-position_y[i])*move_to_middle_strength/len(position_x)

	return (velocity_x, velocity_y)

def fly_away(position_x,position_y,velocity_x,velocity_y):
	# Fly away from nearby boids
	for i in range(len(position_x)):
		for j in range(len(position_x)):
			if (position_x[j]-position_x[i])**2 + (position_y[j]-position_y[i])**2 < alert_distance:
				velocity_x[i]=velocity_x[i]+(position_x[i]-position_x[j])
				velocity_y[i]=velocity_y[i]+(position_y[i]-position_y[j])

	return (velocity_x, velocity_y)

def match_speed(position_x,position_y,velocity_x,velocity_y):
	# Try to match speed with nearby boids
	for i in range(len(position_x)):
		for j in range(len(position_x)):
			if (position_x[j]-position_x[i])**2 + (position_y[j]-position_y[i])**2 < formation_flying_distance:
				velocity_x[i]=velocity_x[i]+(velocity_x[j]-velocity_x[i])*formation_flying_strength/len(position_x)
				velocity_y[i]=velocity_y[i]+(velocity_y[j]-velocity_y[i])*formation_flying_strength/len(position_x)

	return (velocity_x, velocity_y)

def update_boids(boids):
	position_x,position_y,velocity_x,velocity_y=boids
	
	# Fly towards the middle
  	velocity_x, velocity_y = fly_middle(position_x,position_y,velocity_x,velocity_y)
 	# Fly away from nearby boids
  	velocity_x, velocity_y = fly_away(position_x,position_y,velocity_x,velocity_y)
 	# Try to match speed with nearby boids
  	velocity_x, velocity_y = match_speed(position_x,position_y,velocity_x,velocity_y)

	# Move according to velocities
	for i in range(len(position_x)):
		position_x[i]=position_x[i]+velocity_x[i]
		position_y[i]=position_y[i]+velocity_y[i]


figure=plt.figure()
axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
scatter=axes.scatter(boids[0],boids[1])

def animate(frame):
   update_boids(boids)
   scatter.set_offsets(zip(boids[0],boids[1]))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
