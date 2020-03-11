from setuptools import setup, find_packages 

# dependencies 
with open('requirements.txt') as f:
    requirements = f.read() 

requirements = requirements.split('\n')
requirements = [r.strip() for r in requirements]

# description/readme 
with open('README.md') as f:
    description = f.read()

setup(
    name='jpmigrator',
    version='0.1 alpha',
    author='Joshua Poirier',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT License',
    long_description=description
)