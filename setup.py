from setuptools import setup
import os
import sys

install_requires_fname = 'requirements.txt'

if os.path.exists(install_requires_fname):
    with open(install_requires_fname, 'r') as infile:
        install_requires = infile.read().split()

setup(name='pytracker',
      version='0.1',
      description='simple bittorrent index',
      author='Jeff',
      author_email='ampernand+pytracker@gmail.com',
      packages=['pytracker'],
      license="Public Domain",
      install_requires_fname=install_requires
)
