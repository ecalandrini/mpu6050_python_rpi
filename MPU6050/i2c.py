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
        """
        Method to initialize the I2CInterface object.

        Parameters
        ----------
        bus_number : int 1
            bus number.

        Returns
        -------
        None.

        """
        self.bus = smbus2.SMBus(bus_number)

    def read_byte(self, address, register):
        """
        The function read a byte (8-bit) from a register

        Parameters
        ----------
        address : hex
            Address of the MPU6050 as an hex number.
        register : 
            Address of the register as an hex number.

        Returns
        -------
        int
            Value of the red byte in decimal.

        """
        return self.bus.read_byte_data(address, register)

    def write_byte(self, address, register, value):
        """
        The function write a byte (8-bit) in a register

        Parameters
        ----------
        address : hex
            Address of the MPU6050 as an hex number.
        register : hex
            Address of the register as an hex number.
        value : int
            Value to write in the register.

        Returns
        -------
        None.

        """
        self.bus.write_byte_data(address, register, value)
        
    def int_to_binary_string(self, number, length):
        """
        Utility function to transform an integer in a bit string.

        Parameters
        ----------
        number : int
            number to transform.
        length : int
            lenght in bit of the bit string.

        Returns
        -------
        binary_string : str
            String of bits.

        """
        binary_string = format(number, f'0{length}b')
        return binary_string
    
    def binary_string_to_int(self, binary_string):
        """
        Utility function to transform a bit string in an integer.

        Parameters
        ----------
        binary_string : str
            bit string to transform.

        Returns
        -------
        number : int
            int number transformed.

        """
        number = int(binary_string, 2)
        return number
    
    def convert_to_signed(self, value, num_bits):
        """
        Utility function to convert a number in a signed quantity.

        Parameters
        ----------
        value : int
            Number to tronsform.
        num_bits : int
            number of bits used to represent the number "value".

        Returns
        -------
        TYPE
            converted number with sign.

        """
        # If the value is negative, extend the sign bit to the left
        if value & (1 << (num_bits - 1)):
            return value - (1 << num_bits)
        else:
            return value
        
    def combine_bits(self, high_bits, low_bits, num_bits=8):
        """
        Utility function to combine high and low bits.

        Parameters
        ----------
        high_bits : int
            High bits.
        low_bits : TYPE
            low bits.
        num_bits : int, optional
            Number of low bits to shift. The default is 8.

        Returns
        -------
        combined_value : TYPE
            DESCRIPTION.

        """
        # Combine the values using bitwise operations
        combined_value = (high_bits << num_bits) | low_bits
      
        return combined_value
    
    def modify_bit_string(self, original_string, new_string, position):
        """
        Function to modify a portion of bits in a bit string
        Example: original string = "00000"
                new string = "11"
                position = 2
                Result = "00110"

        Parameters
        ----------
        original_string : str
            original bit string.
        new_string : str
            bit string to modify.
        position : int
            position of the first bit to modify in the original_string.

        Returns
        -------
        str
            modified bit string.

        """
        if position < 0 or position >= len(self):
            print("Invalid position.")
        elif position + len(new_string) > original_string:
            print("Invalid length")
        else:
            return original_string[:position] + new_string + original_string[position + len(new_string):]

