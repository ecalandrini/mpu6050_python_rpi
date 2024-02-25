# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:57:55 2024

@author: EugenioCalandrini
"""

from mpu6050 import MPU6050

sensor = MPU6050(0x68)
sensor.wakeup()
sensor.who_am_i()
sensor.sample_rate_get()
sensor.config_get()
sensor.gyro_config_get()
sensor.accel_config_get()

sensor.temp_get()
sensor.gyro_get()
sensor.accel_get()