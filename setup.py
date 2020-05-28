import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='LIB-Feynman',
      version='0.0.1',
      packages=['Feynman'],
      license='MIT License',
      description='My personal library',
      long_description=README,
      url='https://github.com/kangheeyong/LIB-Feynman.git',
      author='khy',
      author_email='cagojeiger@naver.com')
