## @package mcs.Flags
# Test flag settings for individual modules

## @file Flags.py
# Most modules include standard test flags that can be used to facilitate
# testing and debugging.

# ---------- System Controller ----------
MowBotControl_debug = True

DriveSysControl_debug = True
DriveSysControl_enabled = True

InterruptControl_debug = True
InterruptControl_enabled = True

# ---------- Controllers ----------
# Battery Monitor
BatteryMonitor_debug = False
BatteryMonitor_enabled = False

# Blade control
BladeControl_debug = True
BladeControl_enabled = True

# Collision Detection
CollisionDetection_debug = True
CollisionDetection_enabled = True

# Drive Control
DriveControl_debug = True
DriveControl_enabled = True

# Navigation
Navigation_debug = True
Navigation_enabled = True

# Remote Control
RemoteControl_debug = False
RemoteControl_enabled = False

# Message Handler
MessageHandler_debug = True
MessageHandler_enabled = True

# ---------- Firmware ----------
# AMT103 - Encoders
leftEncoder_debug = True
leftEncoder_enabled = True

rightEncoder_debug = True
rightEncoder_enabled = True

# MD30C - Blade Motor Driver
MD30C_debug = False
MD30C_enabled = False

# Relay Controls
wheelRelay_debug = False
wheelRelay_enabled = False

bladeRelay_debug = False
bladeRelay_enabled = False

chargeRelay_debug = False
chargeRelay_enabled = False

# Sabertooth2x60 - Wheel Motors
leftMotor_debug = False
leftMotor_enabled = False

rightMotor_debug = False
rightMotor_enabled = False

# Object Detection - LiDar
rpLiDAR_A2M4_R4_debug = False
rpLiDAR_A2M4_R4_enabled = False

# GPS 
NEO_M8P_debug = True
NEO_M8P_enabled = True
NEO_M8P_RTK_enabled = False

# Accelerometer
accelerometer_debug = True
accelerometer_enabled = True

# UART 
uart_debug = True
uart_enabled = True