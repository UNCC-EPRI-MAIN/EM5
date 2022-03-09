## @package mcs.PinAssignments
# Holds all the pins for the MCS to interface with.
#
# @file PinAssignments.py
# Auxillary file used to assign GPIO pin assignments for various purposes.
# This file ensures pin numbers do not conflict and provides a mechanism for quick changes.
# All pin numbers use board Mode mode. See Raspberry Pi GPIO for more information.

# Motor Signals
bladePWM = 27
leftMotorPWM = 32
rightMotorPWM = 33

rtkStatus = 37

# Relays
wheelRelay = 31
bladeRelay = 35

# Encoders
leftEncoderX = 18
leftEncoderA = 16
rightEncoderX = 24
rightEncoderA = 26
