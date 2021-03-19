"""
Rev 1.0 
11/XX/2020
Rene Nicklich for EPRI_MAIN5 Senior Design Project at the University of North Carolina at Charlotte
Contact: rene.nicklich92@gmail.com

This Tilt Compensation Code is based on an Arduino Script found on the following website:
https://www.instructables.com/Tilt-Compensated-Compass-With-LSM303DHLC/

This code will return calibrated and tilt compensated compass heading values.

This Code requires some libraries to be downloaded -->  run the following commands in bash on the rasPi:
$ sudo pip3 install adafruit-circuitpython-lsm303-accel
$ sudo pip3 install adafruit-circuitpython-lsm303dlh-mag

if Pip is not install run:
$ pip
--> follow instructions
OR:
$ sudo apt install python3-pip
"""

import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import busio
import board
import time
import numpy as np
from math import sqrt, cos, atan2, sin, pi, degrees

# # Calibratiuon Values found with compass_calibration.py
# mag_cal_val = [-9.818181818181817, -2.3636363636363633, -53.52040816326531]
# acc_cal_val = [0.21035264250000002, -0.5545660575, 0.13386077249999984]

i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)


# Transformation Matrices for the computation of calibrated and tilt compensated Heading values
# Calibration is compass specific, and these calibration matrices are working for LSM303DLHC with top mounted Pin connectors.
mag_transformation_matrix = np.array([[1.383, 0.108, 0.127], 
                            [-0.034, 1.374, 0.025], 
                            [0.205, -0.025, 1.47]])

acc_transformation_matrix = np.array([[1.007, 0.003, 0.006], 
                            [-0.001, 0.988, -0.005], 
                            [-0.022, 0.008, 1.007]])

# Bias Values for the computation of calibrated and tilt compensated Heading values
mag_bias = np.array([-15.156, -2.738, -53.182])
acc_bias = np.array([0.192, 0.054, -0.127])

# Function to read the raw X,Y,Z axis values for both the accelerometer and the magnetometer
# these values are in micro tesla and m/s^2 respectively.
# This function may later be optimized to return maximum/average values for a burst of readings, possibly reducing error.
def getRaw_Heading(): 
    mag_raw_x, mag_raw_y, mag_raw_z = mag.magnetic
    acc_raw_x, acc_raw_y, acc_raw_z = accel.acceleration
    magnetic_raw = np.array([mag_raw_x, mag_raw_y, mag_raw_z])
    accel_raw = np.array([acc_raw_x, acc_raw_y, acc_raw_z])

    # print("raw Vaules: ")
    # print(magnetic_raw)
    # print(accel_raw)
    # print("\n")

    return magnetic_raw, accel_raw

# A function to calculate the calibrated magnetometer and accelerometer values with the given biases and transformation matrices.

"""
change this, might have to do row by row, or try sum rows or dot product?
"""
def get_cal_heading(mag_raw, acc_raw):
    mag_biased = mag_raw - mag_bias
    acc_biased = acc_raw - acc_bias

    # print("biased mag and acc")
    # print(mag_biased)
    # print(acc_biased)
    # print("\n")

    mag_cal = np.zeros(3)
    acc_cal = np.zeros(3)
    for i in range(3):
        for j in range(3):
            mag_cal[i] = mag_cal[i] + (mag_biased[i] * mag_transformation_matrix[i][j])
            # print(mag_cal[i])

    for i in range(3):
        for j in range(3):
            acc_cal[i] = acc_cal[i] + (acc_biased[i] * acc_transformation_matrix[i][j])
            # print(acc_cal[i])

    # print("Mag cal & acc cal:")
    # print(mag_cal)
    # print(acc_cal)
    # print("\n")
    
    return mag_cal, acc_cal

# A function to normalize the obtained values by dividing by the sum of the square roots of its elements.
"""
Not Working, sqrt of negative numbers no bueno
"""
# def norm_values(magnet_val, accelerometer_val):
#     # temp = np.sqrt(magnet_val)
#     # print(temp)
#     xm_temp = magnet_val[0]
#     ym_temp = magnet_val[1]
#     zm_temp = magnet_val[2]

#     xa_temp = magnet_val[0]
#     ya_temp = magnet_val[1]
#     za_temp = magnet_val[2]

#     # norm_mag_val = np.sqrt(np.sqrt(magnet_val[0]) + np.sqrt(magnet_val[1]) + np.sqrt(magnet_val[2]) )
#     # norm_acc_val = np.sqrt(np.sqrt(accelerometer_val[0]) + np.sqrt(accelerometer_val[1]) + np.sqrt(accelerometer_val[2]))

#     norm_mag_val = np.sqrt(np.sqrt(xm_temp) + np.sqrt(ym_temp) + np.sqrt(zm_temp) )
#     norm_acc_val = np.sqrt(np.sqrt(xa_temp) + np.sqrt(ya_temp) + np.sqrt(za_temp))


#     norm_mag = magnet_val/norm_mag_val
#     norm_acc = accelerometer_val/norm_acc_val

#     # print("normalized mag & cal:")
#     # print(mag_cal)
#     # print(acc_cal)
#     # print("\n")

#     return norm_mag, norm_acc

# Low pass filter (not 100% sure why its needed but going off of an example code).
def lp_filter(norm_mag, norm_acc):
    alpha = 0.25
    filtered_mag = norm_mag * alpha + (norm_mag * (1 - alpha))
    filtered_acc = norm_acc * alpha + (norm_acc * (1 - alpha))

    # print("Filtered mag & acc:")
    # print(mag_cal)
    # print(acc_cal)
    # print("\n")

    return filtered_mag, filtered_acc

# Function to calculate the calibrated pitch and roll of the compass.
def pitch_roll(filtered_acc):

    pitch = np.arctan2(-filtered_acc[0], np.sqrt(filtered_acc[2]* filtered_acc[2] + filtered_acc[1] * filtered_acc[1]))
    roll = np.arctan2(filtered_acc[1], np.sqrt(filtered_acc[2]* filtered_acc[2] + filtered_acc[0] * filtered_acc[0]))

    # pitch = degrees(np.arcsin(filtered_acc[0]* -1))
    
    # roll = degrees(np.arcsin(filtered_acc[1])/np.cos(pitch))

    # print("Pitch & roll:")
    # print(pitch)
    # print(roll)
    # print("\n")

    return pitch, roll


def tc_heading():
    raw_mag, raw_acc = getRaw_Heading()
    cal_mag, cal_acc = get_cal_heading(raw_mag, raw_acc)
    # mag_normalized, acc_normalized = norm_values(cal_mag, cal_acc)
    mag_val, acc_val = lp_filter(cal_mag, cal_acc)
    pitch_val, roll_val = pitch_roll(acc_val)

    X_mag_val = mag_val[0]
    Y_mag_val = mag_val[1]
    Z_mag_val = mag_val[2]
    
    # print(X_mag_val)
    # print(Y_mag_val)
    # print(Z_mag_val)

    X_heading = mag_val[0] * np.cos(pitch_val) + mag_val[1] * np.sin(pitch_val) * np.sin(roll_val) + mag_val[2] * np.cos(roll_val) * np.sin(pitch_val)
    Y_heading = mag_val[1] * np.cos(roll_val) - mag_val[2] * np.sin(roll_val)

    heading = np.arctan2(Y_heading, X_heading) * 180/pi

    if heading < 0:
        heading = heading + 360
    
    print("heading: " , heading ,"\n")

    return heading

while True: 
    tc_heading()
    time.sleep(1)


