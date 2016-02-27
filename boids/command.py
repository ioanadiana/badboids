from argparse import ArgumentParser
from matplotlib import pyplot as plt
from boids import Flock
from matplotlib import animation
import yaml
import os
import numpy as np

def process():
	parser = ArgumentParser(description = "Boids")
    
	parser.add_argument('--config', dest = 'file')
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	arguments= parser.parse_args()
    
	print(arguments.file)

	boids=Flock('config.yaml')

	figure=plt.figure()
	axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
	handle = lambda frame: animate(boids, scatter) 
	scatter=axes.scatter(boids.positions[0,:],boids.positions[1,:])

	anim = animation.FuncAnimation(figure, handle,
                               frames=50, interval=50)

	plt.show()
   
def animate(boids, scatter):
 
   boids.update_boids()
   scatter.set_offsets(zip(boids.positions[0,:],boids.positions[1,:]))


if __name__ == "__main__":
    process()    
