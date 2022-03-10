## @package mcs.PinAssignments
# Holds all the pins for the MCS to interface with.
#
# @file PinAssignments.py
# Auxillary file used to assign GPIO pin assignments for various purposes.
# This file ensures pin numbers do not conflict and provides a mechanism for quick changes.
# All pin numbers use BCM Mode mode. See Raspberry Pi GPIO for more information.

# Motor Signals
bladePWM = 5
leftMotorPWM = 12
rightMotorPWM = 13

rtkStatus = 26

# Relays
wheelRelay = 6
bladeRelay = 19

# Encoders
leftEncoderX = 24
leftEncoderA = 23
rightEncoderX = 8
rightEncoderA = 7

# Accelerometer
SDL = 3
SDA = 2
