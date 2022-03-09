## @package mcs.Flags
# Test flag settings for individual modules

## @file Flags.py
# Most modules include standard test flags that can be used to facilitate
# testing and debugging.

# ---------- Controllers ----------
# Battery Monitor
BatteryMonitor_debug = False
BatteryMonitor_enabled = False

# Blade control
BladeControl_debug = False
BladeControl_enabled = True

# Collision Detection - Bumpers
CollisionDetection_debug = False
CollisionDetection_enabled = False

# Drive Control
DriveControl_debug = True
DriveControl_enabled = True

# Navigation
Navigation_debug = True
Navigation_enabled = True

# Remote Control
RemoteControl_debug = True
RemoteControl_enabled = True

# ---------- Firmware ----------
# AMT103 - Encoders
leftEncoder_debug = True
leftEncoder_enabled = True

rightEncoder_debug = False
rightEncoder_enabled = False

# MD30C - Blade Motor Driver
MD30C_debug = False
MD30C_enabled = True

# Relay Controls
wheelRelay_debug = False
wheelRelay_enabled = True

bladeRelay_debug = False
bladeRelay_enabled = False

chargeRelay_debug = False
chargeRelay_enabled = False

# Sabertooth2x60 - Wheel Motors
leftMotor_debug = False
leftMotor_enabled = True

rightMotor_debug = False
rightMotor_enabled = True

# Object Detection - LiDar
rpLiDAR_A2M4_R4_debug = False
rpLiDAR_A2M4_R4_enabled = False

# GPS 
NEO_M8P_debug = False
NEO_M8P_enabled = True
NEO_M8P_RTK_enabled = True