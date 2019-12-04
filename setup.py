from setuptools import setup

setup(
       name='sharenewstools',
       version='0.1',
       description='Toolkit for analyzing news sharing on social media',
       author='Damian Trilling',
       author_email='d.c.trilling@uva.nl',
       packages=['sharenewstools'],  
       install_requires=['requests', 'pandas'],  # TODO: check
       scripts=['bin/urls2crowdtangle']
    )
