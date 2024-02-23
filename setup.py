# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 23:33:59 2024

@author: EugenioCalandrini
"""

from setuptools import setup, find_packages

setup(
    name='MPU6050',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'smbus2',
    ],
    description='Library for interfacing with MPU6050 over I2C',
    author='Eugenio Calandrini',
    author_email='calandrini.e@gmail.com',
    url='https://github.com/your_username/my_sensor',
    license='MIT',
)
