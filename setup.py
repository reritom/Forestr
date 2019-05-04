from setuptools import setup
import os

def get_requirements():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt'), 'r') as f:
        lines = f.readlines()
        return lines

setup(
   name='Forestr',
   version='1.0',
   description='Forestry Surveying Tool',
   author='reritom',
   install_requires=get_requirements()
)
