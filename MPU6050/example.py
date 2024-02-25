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

t = sensor.temp_get()
gy = sensor.gyro_get()
a = sensor.accel_get()

for i in range(200):
    print(i)
    sensor.temp_get()
    sensor.gyro_get()
    sensor.accel_get()
    if i >= 100:
        t += sensor.temp_get()
        gy += sensor.gyro_get()
        a += sensor.accel_get()
        
print("values", t, gy, a)
print("mean", t/100, gy/100, a/100)