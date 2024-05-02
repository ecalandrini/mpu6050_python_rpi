# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 22:09:54 2024

@author: calan
"""

# sensor.py
from i2c import I2CInterface
from register_map import RegisterMap
import numpy as np
import ctypes

class HMC5883L:
    """
    
    """
    def __init__(self, address, bus_number=1):
        self.address = address
        self.i2c = I2CInterface(bus_number)
        self.sr = 0
        self.mag = np.empty(3)
        self.gain = 0
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
        
        reading = (high_byte << 8) | low_byte

        return ctypes.c_int32(reading).value

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

    def modify_register(self, register, value, position):
        """
        Function to modify a bit or a group of contiguous bits in a register.

        Parameters
        ----------
        register : hex
            Address of the register to modify.
        value : str
            new bit string to write in the register.
        position : int
            position of the firts bit to modify.

        Returns
        -------
        None.

        """
        data = self.read_data(register)
        bit_string = self.i2c.int_to_binary_string(data, 8)
        new_string = self.i2c.modify_bit_string(bit_string, value, position)
        new_data = self.i2c.binary_string_to_int(new_string)
        if self.DEBUG:
            print("Modifying register:", register, ":", bit_string, "->", new_string)
        self.write_data(register, new_data)

    def avg_get(self):

        value = self.read_data(RegisterMap.CRA, output="str")[1:3]
        samples_avgd = list(RegisterMap.sample_average.keys())[list(RegisterMap.sample_average.values()).index(value)]
        print("No of samples averaged per measurement output:", samples_avgd)
    
    def avg_set(self, samples):
        
        self.modify_register(RegisterMap.CRA, RegisterMap.sample_average[samples], 1)
    
    def output_rate_get(self):

        value = self.read_data(RegisterMap.CRA, output="str")[3:7]
        output_rate = list(RegisterMap.output_rate.keys())[list(RegisterMap.output_rate.values()).index(value)]
        print("Output rate(Hz):", output_rate)

    def output_rate_set(self, rate):

        self.modify_register(RegisterMap.CRA, RegisterMap.output_rate[rate], 3)
    
    def meas_mode_get(self):

        value = self.read_data(RegisterMap.CRA, output="str")[6:]
        meas_mode = list(RegisterMap.measurement_mode.keys())[list(RegisterMap.measurement_mode.values()).index(value)]
        print("Measurement mode", meas_mode)

    def meas_mode_set(self, int_val):

        meas_mode = list(RegisterMap.measurement_mode.keys())[int_val]
        mode_str = list(RegisterMap.measurement_mode.values())[int_val]
        self.modify_register(RegisterMap.CRA, RegisterMap.measurement_mode[mode_str], 6)
        print("Setting the measurement mode to", meas_mode)

    def gain_get(self):

        value = self.read_data(RegisterMap.CRB, output="str")[0:3]
        self.gain = RegisterMap.sensor_range[value][1]
        print("Sensor Field Range (Ga)", RegisterMap.sensor_range[value][0])

    def gain_set(self, range):

        idx = [i[0] for i in list(RegisterMap.sensor_range.values())].index(range)
        bitstr = list(RegisterMap.sensor_range.keys())[idx]
        self.write_data(RegisterMap.CRB, bitstr+"00000")
        self.gain = [i[1] for i in list(RegisterMap.sensor_range.values())][idx]

    def mode_get(self):

        value = self.read_data(RegisterMap.MR, output="str")[6:]
        print("Device is in", RegisterMap.operating_mode[value], "mode")

    def mode_set(self, int_val):

        meas_mode = list(RegisterMap.operating_mode.keys())[int_val]
        mode_str = list(RegisterMap.operating_mode.values())[int_val]        
        self.write_data(RegisterMap.MR, "000000"+mode_str)
        print("Setting the device to", meas_mode, "measurement mode")

    def read_mag_x(self):

        raw_value = self.read_measurement(RegisterMap.DXRA)
        if raw_value == -4096:
            print("Measurement Error in x-axis")
        else: self.mag[0] = raw_value/self.gain * 1000 #value in mGa

    def read_mag_y(self):

        raw_value = self.read_measurement(RegisterMap.DYRA)
        if raw_value == -4096:
            print("Measurement Error in y-axis")
        else: self.mag[1] = raw_value/self.gain * 1000 #value in mGa

    def read_mag_z(self):

        raw_value = self.read_measurement(RegisterMap.DZRA)
        if raw_value == -4096:
            print("Measurement Error in z-axis")
        else: self.mag[2] = raw_value/self.gain * 1000 #value in mGa
    
    def read_mag(self):

        self.read_mag_x()
        self.read_mag_y()
        self.read_mag_z()
    
    def identify(self):

        intA = self.read_data(RegisterMap.IRA)
        intB = self.read_data(RegisterMap.IRB)
        intC = self.read_data(RegisterMap.IRC)

        asciiA = intA.to_bytes((intA.bit_length() + 7) // 8, 'big').decode()
        asciiB = intB.to_bytes((intB.bit_length() + 7) // 8, 'big').decode()
        asciiC = intC.to_bytes((intC.bit_length() + 7) // 8, 'big').decode()

        print(asciiA, asciiB, asciiC)

    def status(self):

        status = self.read_data(RegisterMap.SR)
        if status == 1: return True
        elif status == 0: return False
        elif status == 2: return -1

    def wakeup(self):

        self.write_data(RegisterMap.CRA, self.i2c.binary_string_to_int("01110000")) #01110000 8 samples averaged ("11"), 15Hz output rate ("100"), normal measurement mode ("00"), 
        self.write_data(RegisterMap.CRB, self.i2c.binary_string_to_int("10100000")) #10100000 Gain = "101" = 4.7 Ga
        self.write_data(RegisterMap.MR, self.i2c.binary_string_to_int("00000000"))  #00000000 Continuous-measurement mode

    def self_test(self):

        low_lim = 243
        high_lim = 575
        gain = 5
        axis = ["X", "Y", "Z"]

        self.write_data(RegisterMap.CRA, self.i2c.binary_string_to_int("01110001")) #01110000 8 samples averaged ("11"), 15Hz output rate ("100"), positive bias mode ("01"), 
        self.write_data(RegisterMap.CRB, self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(gain,3)+"00000")) #10100000 Gain = 5("101") = 4.7 Ga
        self.write_data(RegisterMap.MR, self.i2c.binary_string_to_int("00000000"))  #00000000 Continuous-measurement mode
        
        for gain in range(5, 8):
            
            self_test = 0
            print("Gain", gain)
            self.write_data(RegisterMap.CRB, self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(gain,3)+"00000")) #10100000 Gain = 5("101") = 4.7 Ga
            for i in range(2):
                if self.status:
                    self.read_mag()

            self.mag *= RegisterMap.sensor_range[self.i2c.int_to_binary_string(gain,3)]
            factor = RegisterMap.sensor_range[self.i2c.int_to_binary_string(gain,3)]/RegisterMap.sensor_range[self.i2c.int_to_binary_string(5,3)]
            
            for i in range(3):
                if self.mag[i] >= low_lim*factor and self.mag[i] <= high_lim*factor:
                    print(f'Self Test {axis[i]:1}-Axis: PASSED! :-)')
                    self_test += 1
                else: 
                    print(f'Self Test {axis[i]:1}-Axis: FAILED! :-(')
                    break

            if self_test == 2:
                print("Self Test Passed!")
                self.write_data(RegisterMap.CRA, self.i2c.binary_string_to_int("01110000")) #01110000 8 samples averaged ("11"), 15Hz output rate ("100"), normal measurement mode ("00"), 
                break
            else:
                print("Self Test Not Passed. Increasing Gain...")

    def temperature_calibration(self, option):
        pass

