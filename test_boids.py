from nose.tools import assert_almost_equal
import os
import yaml
import numpy as np
import flock as f

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]   

    positions = np.append([np.asarray(boid_data[0])],[np.asarray(boid_data[1])],axis=0)
    velocities = np.append([np.asarray(boid_data[2])],[np.asarray(boid_data[3])],axis=0)

    boids = f.Flock('config.yaml')
    boids.set_positions(positions)
    boids.set_velocities(velocities)
    boids.update_boids()

    for after,before in zip(regression_data["after"],np.append(boids.positions,boids.velocities,axis=0)):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.1)
	
