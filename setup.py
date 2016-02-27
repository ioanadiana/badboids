
from setuptools import setup, find_packages

setup(
    name = "badboids",
    version = "1.0.0",
	description = "Bad Boids Assignment",
	author = "Ioana Oprea",
	author_email = "ioana.oprea.15@ucl.ac.uk",
	url = "https://github.com/ioanadiana/badboids.git",
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/boids'],
    install_requires = ['argparse','numpy','matplotlib']
)


