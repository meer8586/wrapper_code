import os
from setuptools import setup
#import wrapper

with open('requirement.txt') as fp:
    install_requires = fp.read()

setup(install_requires=install_requires)
