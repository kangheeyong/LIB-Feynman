import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='Feynman',
      version='0.1.0',
      license='MIT License',
      description='My personal library',
      long_description=README,
      url='https://github.com/kangheeyong/LIB-Feynman.git',
      packages=find_packages(),
      exclude=['scripts', 'tests'],
      author='khy',
      author_email='cagojeiger@naver.com')
