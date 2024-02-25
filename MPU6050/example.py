# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:57:55 2024

@author: EugenioCalandrini
"""

from mpu6050 import MPU6050
from register_map import RegisterMap
import numpy as np

sensor = MPU6050(0x68)
sensor.wakeup()
sensor.who_am_i()
sensor.sample_rate_get()
sensor.config_get()
sensor.gyro_config_get()
sensor.accel_config_get()

sensor.read_data(RegisterMap.USER_CTRL, output="str")

# t = []
# gy = []
# a = []

# for i in range(200):
#     print(i)
#     sensor.temp_get()
#     sensor.gyro_get()
#     sensor.accel_get()
#     if i >= 100:
#         t.append(sensor.temp)
#         gy.append(sensor.gyro)
#         a.append(sensor.accel)
        
# print("values", len(t), len(gy), len(a))
# print("mean", np.array(t).mean(axis=0), np.array(gy).mean(axis=0), np.array(a).mean(axis=0))