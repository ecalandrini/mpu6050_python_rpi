# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 22:09:54 2024

@author: calan
"""

# sensor.py
from i2c import I2CInterface
from register_map import RegisterMap
import numpy as np

class HMC5883L:
    """
    
    """
    def __init__(self, address, bus_number=1):
        self.address = address
        self.i2c = I2CInterface(bus_number)
        self.sr = 0
        self.mag = np.empty(3)
        self.gyro_fs = 0
        self.accel_fs = 0
        self.DEBUG = False

    def read_measurement(self, register):
        """
        Function to read a 16-bit measurement.
        It reads two register and combine the result.

        Parameters
        ----------
        register : hex
            first register to read.

        Returns
        -------
        int
            combined read result.

        """        
        high_byte = self.i2c.read_byte(self.address, register)
        low_byte = self.i2c.read_byte(self.address, register+1)
        
        value = (high_byte << 8) | low_byte
        
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else: return value

    def read_data(self, register, output="int"):
        """       
        Parameters
        ----------
        register : hex
            Address of the register to read.
        output : str, optional
            type of the function output. The default is "int".

        Returns
        -------
        value : dict
            The function return an int by default or a 8-bit string if output is "str".

        """
        # Example: Read data from a specific register of the sensor
        data = self.i2c.read_byte(self.address, register)
        data_bitstring = self.i2c.int_to_binary_string(data, 8)
        
        value = {
            "int" : data,
            "str" : data_bitstring
            }
        return value[output]
    
    def write_data(self, register, value):
        """
        Function to write in a register.
        Wrapper function of the "write_byte_data".

        Parameters
        ----------
        register : Hex
            Address of the register to be write.
        value : int
            Value to write in the register.

        Returns
        -------
        None.

        """
        # Example: Read data from a specific register of the sensor
        self.i2c.write_byte(self.address, register, value)