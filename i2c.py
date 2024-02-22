# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 21:58:57 2024

@author: calan
"""

# =============================================================================
# I2C BUS COMMUNICATION UTILITIES
# =============================================================================
import smbus2

class I2CInterface:
    def __init__(self, bus_number):
        self.bus = smbus2.SMBus(bus_number)

    def read_byte(self, address, register):
        return self.bus.read_byte_data(address, register)

    def write_byte(self, address, register, value):
        self.bus.write_byte_data(address, register, value)
        
    def int_to_binary_string(number, length):
        binary_string = format(number, f'0{length}b')
        return binary_string
    
    def binary_string_to_int(binary_string):
        number = int(binary_string, 2)
        return number

