# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:57:55 2024

@author: EugenioCalandrini
"""

from MPU6050.mpu6050 import MPU6050
from MPU6050.register_map import RegisterMap
import numpy as np
import time

sensor = MPU6050(0x68)
sensor.wakeup()
sensor.who_am_i()
sensor.sample_rate_get()
sensor.config_get()
sensor.gyro_config_get()
sensor.accel_config_get()

sensor.pass_through_mode_get()
sensor.pass_through_mode_set(True)
sensor.pass_through_mode_get()


t = []
gy = []
a = []

for i in range(200):
    #print(i)
    sensor.temp_get()
    sensor.gyro_get()
    sensor.accel_get()
    if i >= 100:
        t.append(sensor.temp)
        gy.append(sensor.gyro)
        a.append(sensor.accel)
    time.sleep(.1)
        
print("values temp gy_x gy_y gy_z a_x a_y a_z norm")
t_mean = np.array(t).mean(axis=0)
gy_mean = np.array(gy).mean(axis=0)
a_mean = np.array(a).mean(axis=0)
print("mean", t_mean, gy_mean, a_mean, np.sqrt(a_mean.dot(a_mean)))