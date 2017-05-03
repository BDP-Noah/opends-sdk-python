#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()


setup(
    name='opends',
    version='0.0.1',
    description='Official OpenDS REST API Client',
    long_description=readme,
    author='bdp',
    author_email='huangwenda@haizhi.com',
    url='http://www.bdp.cn/',
    packages=['opends'],
    install_requires=map(lambda x: x.replace('==', '>='), open("requirements.txt").readlines()))
