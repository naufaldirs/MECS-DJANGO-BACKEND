# apps/master/services/production_capacity.py
from math import floor

def calculate_capacity(ascast, cycle_time, cavity):
    kg = 1000

    one_hour = 3600
    one_hour_pcs = one_hour / cycle_time * cavity

    shift_8 = round(one_hour_pcs * 7.5)
    shift_7 = round(one_hour_pcs * 6.5)
    shift_6 = round(one_hour_pcs * 5.5)

    normal = (ascast * (shift_8 / cavity)) / kg
    overtime = (ascast * (shift_7 / cavity)) / kg
    dandory = (ascast * (shift_6 / cavity)) / kg

    return {
        "one_hour_pcs": one_hour_pcs,
        "eight_hour_pcs": shift_8,
        "seven_hour_pcs": shift_7,
        "six_hour_pcs": shift_6,
        "normal_kg": normal,
        "overtime_kg": overtime,
        "dandory_kg": dandory,
    }
