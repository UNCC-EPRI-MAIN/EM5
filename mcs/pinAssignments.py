## @package mcs.pinAssignments
# Pin assignments for Raspberry Pi GPIO
#
# This file is an auxillary file used to assign GPIO pin assignments for various purposes.
# This file ensures pin numbers do not conflict and provides a mechanism for quick changes.
# All pin numbers use BCM mode. See Raspberry Pi GPIO for more information.
# @author Keith
# @note 03/19/2021: Updated documentation -KS

# motor signals
bladePWM = 0
leftMotorPWM = 13
rightMotorPWM = 12

rtkStatus = 4

# relays
wheelRelay = 19
bladeRelay = 6

# encoders
leftEncoderX = 24
leftEncoderA = 23
rightEncoderX = 15
rightEncoderA = 14

# bumpers
bumper1 = 25 
bumper2 = 8
bumper3 = 7
bumper4 = 1
bumper5 = 16
bumper6 = 20
bumper7 = 21
