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
BladeControl_debug = False
BladeControl_enabled = False

# Collision Detection
CollisionDetection_debug = False
CollisionDetection_enabled = False

# Drive Control
DriveControl_debug = False
DriveControl_enabled = False

# Navigation
Navigation_debug = True
Navigation_enabled = True

# Remote Control
RemoteControl_debug = False
RemoteControl_enabled = False

# Message Handler
MessageHandler_debug = False
MessageHandler_enabled = False

# ---------- Firmware ----------
# AMT103 - Encoders
leftEncoder_debug = False
leftEncoder_enabled = False

rightEncoder_debug = False
rightEncoder_enabled = False

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
accelerometer_debug = False
accelerometer_enabled = False

# UART 
uart_debug = False
uart_enabled = False