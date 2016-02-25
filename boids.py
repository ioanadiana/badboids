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

def update_boids(boids):
	xs,ys,xvs,yvs=boids
	# Fly towards the middle
	for i in range(len(xs)):
		for j in range(len(xs)):
			xvs[i]=xvs[i]+(xs[j]-xs[i])*move_to_middle_strength/len(xs)
	for i in range(len(xs)):
		for j in range(len(xs)):
			yvs[i]=yvs[i]+(ys[j]-ys[i])*move_to_middle_strength/len(xs)
	# Fly away from nearby boids
	for i in range(len(xs)):
		for j in range(len(xs)):
			if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < alert_distance:
				xvs[i]=xvs[i]+(xs[i]-xs[j])
				yvs[i]=yvs[i]+(ys[i]-ys[j])
	# Try to match speed with nearby boids
	for i in range(len(xs)):
		for j in range(len(xs)):
			if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < formation_flying_distance:
				xvs[i]=xvs[i]+(xvs[j]-xvs[i])*formation_flying_strength/len(xs)
				yvs[i]=yvs[i]+(yvs[j]-yvs[i])*formation_flying_strength/len(xs)
	# Move according to velocities
	for i in range(len(xs)):
		xs[i]=xs[i]+xvs[i]
		ys[i]=ys[i]+yvs[i]


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
