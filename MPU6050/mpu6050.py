# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 22:09:54 2024

@author: calan
"""

# sensor.py
from i2c import I2CInterface
from register_map import RegisterMap
import numpy as np

class MPU6050:
    """
    Class for the MPU6050 sensor
    
    Attributes
    ----------
    address : hex
        address of the MPU6050 sensor.
    sr : float
        Sample rate in kHz.
    gyro_fs : float
        Full scale range of the gyro.
    accel_fs : float
        Full scale range of the accel.
    gyro_i : float
        Last measurement of the gyro i-axis.
    accel_i : float
        Last measurement of the accel i-axis.
    temp : float
        Last measurement of the temperature.
        
    Methods
    -------
    read_measurement:
        
    read_data:
        
    write_data:
    
    modify_register:
        
    sample_rate_get:
        
    sample_rate_set:
        
    config_get:
    
    config_set:
        
    gyro_config_get:
        
    gyro_config_set:
        
    accel_config_get:
        
    accel_config_set:
        
    who_am_i:
        
    wakeup:
    
    sleep:
        
    reset:
        
    cycle:
        
    temp_disable:
        
    temp_enable:
        
    read_gyro_i:
        
    read_gyro:
        
    read_accel_i:
    
    read_accel:
        
    selftest_gyro_i:
        
    selftest_gyro:
    
    selftest_accel_i:
        
    selftest_accel:
    
    standby_gyro_i_on:
        
    standby_gyro_on:
        
    standby_gyro_i_off:
        
    standby_gyro_off:
        
    standby_accel_i_on:
        
    standby_accel_on:
        
    standby_accel_i_off:
        
    standby_accel_off:
        
    mode_AOLP:
    """
    def __init__(self, address, bus_number=1):
        self.address = address
        self.i2c = I2CInterface(bus_number)
        self.sr = 0
        self.gyro = np.empty(3)
        self.accel = np.empty(3)
        self.temp = 0
        self.gyro_fs = 0
        self.accel_fs = 0
        
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
        print("Modifying register:", register, ":", bit_string, "->", new_string)
        self.write_data(register, new_data)

    def calibrate(self):
        # Example: Write calibration data to a specific register of the sensor
        self.i2c.write_byte(self.address, RegisterMap.REGISTER_B, RegisterMap.REGISTER_B_VALUE_1)
        
    def sample_rate_get(self):
        """
        Getter function of the Sample Rate for the MPU-6050. 
        The Sample Rate is generated by dividing the gyroscope output rate by SMPLRT_DIV.
        The sensor register output, FIFO output, and DMP sampling are all based on the Sample Rate.

        Returns
        -------
        None.

        """
        # read the register
        divider = self.read_data(RegisterMap.SMPLRT_DIV)
        
        # calculate the sample rate
        data = self.read_data(RegisterMap.CONFIG)
        DLPF_CFG = self.i2c.int_to_binary_string(data, 8)[-3:]
        DLPF = self.i2c.binary_string_to_int(DLPF_CFG)
        if DLPF == 0 or DLPF == 7:
            self.sr = 8/(1+divider)
        else: self.sr = 1/(1+divider)
                
        print("Present Configuration", self.i2c.int_to_binary_string(divider, 8))
        print("Sample rate is", self.sr, "kHz")
        
    def sample_rate_set(self, divider):
        """
        Setter function of the Sample Rate for the MPU-6050. 
        The Sample Rate is generated by dividing the gyroscope output rate by SMPLRT_DIV.
        The sensor register output, FIFO output, and DMP sampling are all based on the Sample Rate.
        
        Parameters
        ----------
        SMPLRT_DIV : int [0:256]
            Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV).

        Returns
        -------
        None.

        """
        # calculate the sample rate
        data = self.read_data(RegisterMap.CONFIG)
        DLPF_CFG = self.i2c.int_to_binary_string(data, 8)[-3:]
        DLPF = self.i2c.binary_string_to_int(DLPF_CFG)
        if DLPF == 0 or DLPF == 7:
            self.sr = 8/(1+divider)
        else: self.sr = 1/(1+divider)
                
        # calculate the new value
        divider_bits = self.i2c.int_to_binary_string(divider, 8)
        self.write_data(RegisterMap.SMPLRT_DIV, divider)
        print("New Configuration", divider_bits)
        print("Sample rate is", self.sr, "kHz")
        
        # write in the register
        self.write_data(RegisterMap.SMPLRT_DIV, divider)

    def config_get(self):
        """
        Getter function for the external Frame Synchronization (FSYNC) pin sampling and the Digital
        Low Pass Filter (DLPF) setting for both the gyroscopes and accelerometers.
        See register 26 for more information.
        
        Returns
        -------
        None.

        """
        # read the register
        data = self.read_data(RegisterMap.CONFIG)
        print("Present Configuration", self.i2c.int_to_binary_string(data, 8))
        
    def config_set(self, DLPF_CFG, EXT_SYNC_SET=0):
        """
        Getter function for the external Frame Synchronization (FSYNC) pin sampling and the Digital
        Low Pass Filter (DLPF) setting for both the gyroscopes and accelerometers.
        See register 26 for more information.
        
        Parameters
        ----------
        EXT_SYNC_SET: int [0:8] 
            to be implemented
        DLPF_CFG: int [0:8] 
            See register 26 for more information.

        Returns
        -------
        None.

        """
        # read the register
        data = self.read_data(RegisterMap.CONFIG)
        print("Present Configuration", self.i2c.int_to_binary_string(data, 8))
        
        # calculate the new value
        value = self.i2c.int_to_binary_string(EXT_SYNC_SET, 3) + self.i2c.int_to_binary_string(DLPF_CFG, 3) 
        new_bitstring = self.modify_register(RegisterMap.CONFIG, value, 2)
        print("New Configuration", new_bitstring)
        
        # write in the register
        self.write_data(RegisterMap.CONFIG, self.i2c.binary_string_to_int(new_bitstring))
        
    def gyro_config_get(self):
        """
        Getter function to trigger gyroscope self-test and configure the gyroscopes’ full scale range.
        See register 27 for more information.

        Returns
        -------
        None.

        """
        data = self.read_data(RegisterMap.GYRO_CONFIG)
        bit_string = self.i2c.int_to_binary_string(data, 8)
        XG_ST = bit_string[0]
        YG_ST = bit_string[1]
        ZG_ST = bit_string[2]
        FS_SEL = self.i2c.binary_string_to_int(bit_string[3:5])
        self.gyro_fs = RegisterMap.GYRO_LSB[FS_SEL]
        
        print("Self-Test activated on axis (x, y, z)", XG_ST, YG_ST, ZG_ST)
        print("Gyro full scale range +/-", 250*2**FS_SEL, "º/s")
        
    def gyro_config_set(self, XG_ST, YG_ST, ZG_ST, FS_SEL):
        """
        Setter function to trigger gyroscope self-test and configure the gyroscopes’ full scale range.
        See register 27 for more information.       

        Parameters
        ----------
        XG_ST : int [0:2]
            Activate the self-self on x-axis (1)
        YG_ST : int [0:2]
            Activate the self-self on y-axis (1)
        ZG_ST : int [0:2]
            Activate the self-self on z-axis (1)
        FS_SEL : int [0:4]
            Set the full scale range of the gyroscope

        Returns
        -------
        None.

        """
        bit_string = str(XG_ST) + str(YG_ST) + str(ZG_ST) + self.i2c.int_to_binary_string(FS_SEL, 2) + "000"
        self.write_data(RegisterMap.GYRO_CONFIG, self.i2c.binary_string_to_int(bit_string))
        self.gyro_fs = RegisterMap.GYRO_LSB[FS_SEL]
        
        print("Activation of Self-Test on axis (x, y, z)", XG_ST, YG_ST, ZG_ST)
        print("Setting the Gyro full scale range +/-", 250*2**FS_SEL, "º/s")

    def accel_config_get(self):
        """
        Getter function to retrieve the accelerometer self test settings and the accelerometer full scale
        range configuration. 
        See register 28 for more information. 

        Returns
        -------
        None.

        """
        data = self.read_data(RegisterMap.ACCEL_CONFIG)
        bit_string = self.i2c.int_to_binary_string(data, 8)
        XA_ST = bit_string[0]
        YA_ST = bit_string[1]
        ZA_ST = bit_string[2]
        AFS_SEL = self.i2c.binary_string_to_int(bit_string[3:5])
        self.accel_fs = RegisterMap.ACCEL_LSB[AFS_SEL]
        
        print("Self-Test activated on axis (x, y, z)", XA_ST, YA_ST, ZA_ST)
        print("Accel full scale range +/-", 2**(AFS_SEL+1), "g")
        
    def accel_config_set(self, XA_ST, YA_ST, ZA_ST, AFS_SEL):
        """
        Setter function to enable the accelerometer self test settings and configure the accelerometer full scale
        range. 
        See register 28 for more information.

        Parameters
        ----------
        XA_ST : int
            Set to 1 to enable the accelerometer x-axis self test.
        YA_ST : int
            Set to 1 to enable the accelerometer y-axis self test.
        ZA_ST : TYPE
            Set to 1 to enable the accelerometer z-axis self test.
        AFS_SEL : int [0:4]
            Settings of the accelerometer full scale range.

        Returns
        -------
        None.

        """
        bit_string = str(XA_ST) + str(YA_ST) + str(ZA_ST) + self.i2c.int_to_binary_string(AFS_SEL, 2) + "000"
        self.write_data(RegisterMap.ACCEL_CONFIG, self.i2c.binary_string_to_int(bit_string))
        self.accel_fs = RegisterMap.ACCEL_LSB[AFS_SEL]
        
        print("Activation of Self-Test on Accel axis (x, y, z)", XA_ST, YA_ST, ZA_ST)
        print("Setting the Accel full scale range +/-", 2**(AFS_SEL+1), "g")
        
    def who_am_i(self):
        """
        Function to verify the identity of the device.
        The default value of the register is 0x68.

        Returns
        -------
        None.

        """
        data = self.read_data(RegisterMap.WHO_AM_I)
        bit_string = self.i2c.int_to_binary_string(data, 8)
        new_value = hex(self.i2c.binary_string_to_int(bit_string))
        if new_value == '0x68':
            print("I'm a MPU-6050!")
        else: print("I'm not a MPU-6050 :(, my name is", new_value)
        
    def wakeup(self):
        """
        Function to wake up the MPU6050.

        Returns
        -------
        None.

        """
        print("MPU6050 is ON")
        self.modify_register(RegisterMap.PWR_MGMT_1, "0", 1)
        
    def sleep(self):
        """
        Function to turnoff up the MPU6050.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_1, "1", 1)
        
    def reset(self):
        """
        Function to reset the MPU6050.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_1, "1", 0)

    def cycle_enable(self, LP_WAKE_CTRL=0):
        """
        Function to activate the cycle mode of the MPU6050.

        Parameters
        ----------
        LP_WAKE_CTRL : int [0:4]
            Definition of the cycle frequency.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_1, "1", 2)
        data = self.i2c.int_to_binary_string(LP_WAKE_CTRL, 2)
        self.modify_register(RegisterMap.PWR_MGMT_2, data, 0)
        
    def temp_disable(self):
        """
        Function to disable the temperature sensor.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_1, "1", 4)
        print("Temperature Sensor disabled")
        
    def temp_enable(self):
        """
        Function to enable the temperature sensor.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_1, "0", 4)
        print("Temperature Sensor enabled")
    
    def standby_accel_x_on(self):
        """
        Function to set the accel x-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 2)
        
    def standby_accel_y_on(self):
        """
        Function to set the accel y-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 3)
 
    def standby_accel_z_on(self):
        """
        Function to set the accel z-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 4)
        
    def standby_accel_on(self):
        """
        Function to set the accel in standby mode.

        Returns
        -------
        None.

        """
        self.standby_accel_x_on()
        self.standby_accel_y_on()
        self.standby_accel_z_on()
    
    def standby_accel_x_off(self):
        """
        Function to disable the standby mode on the accel x-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 2)
        
    def standby_accel_y_off(self):
        """
        Function to disable the standby mode on the accel y-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 3)
 
    def standby_accel_z_off(self):
        """
        Function to disable the standby mode on the accel z-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 4)
        
    def standby_accel_off(self):
        """
        Function to disable the standby mode on the accel.

        Returns
        -------
        None.

        """
        self.standby_accel_x_off()
        self.standby_accel_y_off()
        self.standby_accel_z_off()
        
    def standby_gyro_x_on(self):
        """
        Function to set the gyro x-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 5)
        
    def standby_gyro_y_on(self):
        """
        Function to set the gyro y-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 6)
 
    def standby_gyro_z_on(self):
        """
        Function to set the gyro z-axis in standby mode.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "1", 7)
        
    def standby_gyro_on(self):
        """
        Function to set the gyro in standby mode.

        Returns
        -------
        None.

        """
        self.standby_gyro_x_on()
        self.standby_gyro_y_on()
        self.standby_gyro_z_on()
    
    def standby_gyro_x_off(self):
        """
        Function to disable the standby mode on the gyro x-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 5)
        
    def standby_gyro_y_off(self):
        """
        Function to disable the standby mode on the gyro y-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 6)
 
    def standby_gyro_z_off(self):
        """
        Function to disable the standby mode on the gyro z-axis.

        Returns
        -------
        None.

        """
        self.modify_register(RegisterMap.PWR_MGMT_2, "0", 7)
        
    def standby_gyro_off(self):
        """
        Function to disable the standby mode on the gyro.

        Returns
        -------
        None.

        """
        self.standby_gyro_x_off()
        self.standby_gyro_y_off()
        self.standby_gyro_z_off()
        
    def mode_AOLP(self):
        """
        Function to put the MPU6050 in the Accelerometer Only Low Power mode.
        See register 108 for more information.

        Returns
        -------
        None.

        """
        self.cycle_enable()
        self.wakeup()
        self.temp_disable()
        self.standby_gyro_on()
        
    def read_gyro_x(self):
        """
        Function to read the value of the gyro x-axis.

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.GYRO_XOUT_H)
        self.gyro[0] = raw_value/self.gyro_fs

    def read_gyro_y(self):
        """
        Function to read the value of the gyro y-axis.

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.GYRO_YOUT_H)
        self.gyro[1] = raw_value/self.gyro_fs

    def read_gyro_z(self):
        """
        Function to read the value of the gyro z-axis.

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.GYRO_ZOUT_H)
        self.gyro[2] = raw_value/self.gyro_fs        
        
    def read_gyro(self):
        """
        Function to read all the 3 axis of the gyro.

        Returns
        -------
        None.

        """
        self.read_gyro_x()
        self.read_gyro_y()
        self.read_gyro_z()
        
    def read_temperature(self):
        """
        Function to read the temperature    
    
        Returns
        -------
        None.
    
        """
        raw_temp = self.read_measurement(RegisterMap.TEMP_OUT_H)
        self.temp = raw_temp/340 + 36.53
       
    def read_accel_x(self):
        """
        Function to read the accel x-axis

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.ACCEL_XOUT_H)
        self.accel[0] = raw_value/self.accel_fs

    def read_accel_y(self):
        """
        Function to read the accel y-axis

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.ACCEL_YOUT_H)
        self.accel[1] = raw_value/self.accel_fs

    def read_accel_z(self):
        """
        Function to read the accel z-axis

        Returns
        -------
        None.

        """
        raw_value = self.read_measurement(RegisterMap.ACCEL_ZOUT_H)
        self.accel[2] = raw_value/self.accel_fs       
        
    def read_accel(self):
        """
        Function to read all the 3 axis of the accel.

        Returns
        -------
        None.

        """
        self.read_accel_x()
        self.read_accel_y()
        self.read_accel_z()
        
    def selftest_gyro_x(self):
        """
        Function to perform the self test on the gyro x-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.gyro_config_set(1, 0, 0, 0)
        self.read_gyro_x()
        gyro_selftest_enabled = self.gyro[0]
        
        self.gyro_config_set(0, 0, 0, 0)
        self.read_gyro_x()
        gyro_selftest_disabled = self.gyro[0]
        
        STR = gyro_selftest_enabled - gyro_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_X)
        XG_TEST = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[3:])
        if XG_TEST == 0:
            FT = 0 
        else: FT = 25 * 131 * 1.046**(XG_TEST-1)
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for gyro x-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for gyro x-axis", deltaFT, "%. Self Test not passed!") 
        
    def selftest_gyro_y(self):
        """
        Function to perform the self test on the gyro y-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """        
        self.gyro_config_set(0, 1, 0, 0)
        self.read_gyro_y()
        gyro_selftest_enabled = self.gyro[1]
        
        self.gyro_config_set(0, 0, 0, 0)
        self.read_gyro_y()
        gyro_selftest_disabled = self.gyro[1]
        
        STR = gyro_selftest_enabled - gyro_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_Y)
        YG_TEST = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[3:])
        if YG_TEST == 0:
            FT = 0 
        else: FT = - 25 * 131 * 1.046**(YG_TEST-1)
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for gyro y-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for gyro y-axis", deltaFT, "%. Self Test not passed!") 
        
    def selftest_gyro_z(self):
        """
        Function to perform the self test on the gyro y-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.gyro_config_set(0, 0, 1, 0)
        self.read_gyro_z()
        gyro_selftest_enabled = self.gyro[2]
        
        self.gyro_config_set(0, 0, 0, 0)
        self.read_gyro_z()
        gyro_selftest_disabled = self.gyro[2]
        
        STR = gyro_selftest_enabled - gyro_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_Z)
        ZG_TEST = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[3:])
        if ZG_TEST == 0:
            FT = 0 
        else: FT = - 25 * 131 * 1.046**(ZG_TEST-1)
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for gyro z-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for gyro z-axis", deltaFT, "%. Self Test not passed!") 
        
    def selftest_gyro(self):
        """
        Function to perform the self test on all the gyro axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """   
        self.selftest_gyro_x()
        self.selftest_gyro_y()
        self.selftest_gyro_z()
        
    def selftest_accel_x(self):
        """
        Function to perform the self test on the accel x-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.accel_config_set(1, 0, 0, 2)
        self.read_accel_x()
        accel_selftest_enabled = self.accel[0]
        
        self.accel_config_set(0, 0, 0, 2)
        self.read_accel_x()
        accel_selftest_disabled = self.accel[0]
        
        STR = accel_selftest_enabled - accel_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_X)
        high_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[:3])
        data = self.read_data(RegisterMap.SELF_TEST_A)
        low_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[2:4])
        
        XA_TEST = self.i2c.combine_bits(high_bits, low_bits, num_bits=2)
        if XA_TEST == 0:
            FT = 0
        else: FT = 4096 * 0.34 * 0.92/0.34 ** ((XA_TEST-1)/(2**5 - 2))
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for accel x-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for accel x-axis", deltaFT, "%. Self Test not passed!") 
       
    def selftest_accel_y(self):
        """
        Function to perform the self test on the accel y-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.accel_config_set(0, 1, 0, 2)
        self.read_accel_y()
        accel_selftest_enabled = self.accel[1]
        
        self.accel_config_set(0, 0, 0, 2)
        self.read_accel_y()
        accel_selftest_disabled = self.accel[1]
        
        STR = accel_selftest_enabled - accel_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_Y)
        high_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[:3])
        data = self.read_data(RegisterMap.SELF_TEST_A)
        low_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[2:4])
        
        YA_TEST = self.i2c.combine_bits(high_bits, low_bits, num_bits=2)
        if YA_TEST == 0:
            FT = 0
        else: FT = 4096 * 0.34 * 0.92/0.34 ** ((YA_TEST-1)/(2**5 - 2))
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for accel y-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for accel y-axis", deltaFT, "%. Self Test not passed!") 
        
    def selftest_accel_z(self):
        """
        Function to perform the self test on the accel z-axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.accel_config_set(0, 1, 0, 2)
        self.read_accel_z()
        accel_selftest_enabled = self.accel[2]
        
        self.accel_config_set(0, 0, 0, 2)
        self.read_accel_z()
        accel_selftest_disabled = self.accel[2]
        
        STR = accel_selftest_enabled - accel_selftest_disabled
        
        data = self.read_data(RegisterMap.SELF_TEST_Z)
        high_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[:3])
        data = self.read_data(RegisterMap.SELF_TEST_A)
        low_bits = self.i2c.binary_string_to_int(self.i2c.int_to_binary_string(data, 8)[2:4])
        
        ZA_TEST = self.i2c.combine_bits(high_bits, low_bits, num_bits=2)
        if ZA_TEST == 0:
            FT = 0
        else: FT = 4096 * 0.34 * 0.92/0.34 ** ((ZA_TEST-1)/(2**5 - 2))
        
        deltaFT = (STR-FT)/FT*100
        if deltaFT <= 14 and deltaFT >= -14:
            print("delta FT for accel z-axis", deltaFT, "%. Self Test OK!")
        else: print("delta FT for accel z-axis", deltaFT, "%. Self Test not passed!") 
        
    def selftest_accel(self):
        
        """
        Function to perform the self test on all the accel axis.
        See Register 11-16 for more information.

        Returns
        -------
        None.

        """
        self.selftest_accel_x()
        self.selftest_accel_y()
        self.selftest_accel_z()
       
    def temp_get(self):
        
        self.read_temperature()
        print("Temperature: ºC", self.temp)
        return self.temp 
        
    def gyro_get(self):
        
        self.read_gyro()
        print("Gyro: º/s", self.gyro)
        return self.gyro
        
    def accel_get(self):
        
        self.read_accel()
        print("Accel: g", self.accel)
        return self.accel
    
    def pass_through_mode_set(self, state):
        
        if state == True:
            self.modify_register(RegisterMap.INT_PIN_CFG, "1", 6)
            self.modify_register(RegisterMap.USER_CTRL, "0", 2)
        else: 
            self.modify_register(RegisterMap.INT_PIN_CFG, "0", 6)
            self.modify_register(RegisterMap.USER_CTRL, "1", 2)
    
    def pass_through_mode_get(self):
        I2C_BYPASS_EN = self.read_data(RegisterMap.INT_PIN_CFG, "str")[8]
        I2C_MST_EN = self.read_data(RegisterMap.USER_CTRL, "str")[2]
        
        if I2C_BYPASS_EN == "1" and I2C_MST_EN == "0":
            print("Pass-Through Mode Enabled")
        if I2C_BYPASS_EN == "0":
            print("Pass-Through Mode Disabled")