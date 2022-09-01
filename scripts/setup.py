from setuptools import setup

setup(
    name='pattern_hiring_test',
    version='0.1dev',
    packages=['pattern_steps'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires = ['pandas', 'geopandas', 'requests', 'fire']
)