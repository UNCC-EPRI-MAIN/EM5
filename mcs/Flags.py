## @package mcs.Flags
# Test flag settings for individual modules

## @file Flags.py
# Most modules include standard test flags that can be used to facilitate
# testing and debugging.

# ---------- System Controller ----------
MowBotControl_debug = True

DriveSysControl_debug = False
DriveSysControl_enabled = True

InterruptControl_debug = False
InterruptControl_enabled = True

# ---------- Controllers ----------
# Battery Monitor
BatteryMonitor_debug = False
BatteryMonitor_enabled = True

# Blade control
BladeControl_debug = False
BladeControl_enabled = True

# Collision Detection
CollisionDetection_debug = False
CollisionDetection_enabled = True

# Drive Control
DriveControl_debug = False
DriveControl_enabled = True

# Navigation
Navigation_debug = False
Navigation_enabled = True

# Remote Control
RemoteControl_debug = False
RemoteControl_enabled = True

# ---------- Firmware ----------
# AMT103 - Encoders
leftEncoder_debug = False
leftEncoder_enabled = True

rightEncoder_debug = False
rightEncoder_enabled = True

# MD30C - Blade Motor Driver
MD30C_debug = False
MD30C_enabled = True

# Relay Controls
wheelRelay_debug = False
wheelRelay_enabled = True

bladeRelay_debug = False
bladeRelay_enabled = True

chargeRelay_debug = False
chargeRelay_enabled = True

# Sabertooth2x60 - Wheel Motors
leftMotor_debug = False
leftMotor_enabled = True

rightMotor_debug = False
rightMotor_enabled = True

# Object Detection - LiDar
rpLiDAR_A2M4_R4_debug = False
rpLiDAR_A2M4_R4_enabled = True

# GPS 
NEO_M8P_debug = False
NEO_M8P_enabled = True
NEO_M8P_RTK_enabled = True

# Accelerometer
accelerometer_debug = False
accelerometer_enabled = True