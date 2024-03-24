# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 21:24:10 2024

@author: Eugenio Calandrini
"""

# =============================================================================
# REGISTER MAP DEFINITION
# =============================================================================

class RegisterMap:
    CRA = 0x00
    CRB = 0X01
    MR = 0X02
    DXRA = 0X03
    DXRB = 0X04
    DYRA = 0X05
    DYRB = 0X06
    DZRA = 0X07
    DZRB = 0X08
    SR = 0X09
    IRA = 0X0A
    IRB = 0X0B
    IRC = 0X0C

    sample_average = {
        1 : "00",
        2 : "01",
        4 : "10",
        8 : "11"
    }

    output_rate = {
        0.75 : "000",
        1.5 : "001",
        3 : "010",
        7.5 : "011",
        15 : "100",
        30 : "101",
        75 : "110"
    }

    sensor_range = {
        "000" : [0.88, 1370],
        "001" : [1.3, 1090],
        "010" : [1.9, 820],
        "011" : [2.5, 660],
        "100" : [4.0, 440],
        "101" : [4.7, 390],
        "110" : [5.6, 330],
        "111" : [8.1, 230]
    }

    measurement_mode = {
        "Normal" : "00",
        "Positive bias" : "01",
        "Negative bias" : "10"
    }

    operating_mode = {
        "Continuous" : "00",
        "Single" : "01",
        "Idle" : "10"
    }