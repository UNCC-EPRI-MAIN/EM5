# from LSM303DLHC_tc import *
# import mcs.LSM303DLHC_tc as compass
import mcs.Sabertooth2x60 as motor
import mcs.RelayControl as rc
import mcs.MD30C as mcs
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class SystemFlags:
    RelayControl_debug = True
    RelayControl_enabled = True
    Sabertooth2x60_debug = True
    Sabertooth2x60_enabled = True
    bladeMotor_debug = True
    bladeMotor_enabled = True

flags = SystemFlags()

bladeMotor = mcs.MD30C(16, flags)

leftMotor = motor.Sabertooth2x60(17, flags, "Left")
rightMotor = motor.Sabertooth2x60(27, flags, "Right")

testRelay1 = rc.RelayControl(24, flags, "relay1")
testRelay2 = rc.RelayControl(25, flags, "relay2")
#time.sleep(5)
testRelay1.enable()
#time.sleep(2)
testRelay2.enable()
time.sleep(1)

# heading_straight = compass.tc_heading()
bladeMotor.spin()
leftMotor.forward(100)
rightMotor.forward(100)
## Testing compas readout with blade motors spinning
# for i in range(1000):
#     print(compass.tc_heading())
#     time.sleep(1)

# forward_speed_lt = 50
# forward_speed_rt = 50

# leftMotor.forward(forward_speed_lt)
# rightMotor.forward(forward_speed_rt)
# time.sleep(5)
# for i in range(10):
#     time.sleep(1)
#     print("left: " + str(forward_speed_lt))
#     print("right: " + str(forward_speed_rt))
#     #if forward_speed_lt < 100 & forward_speed_lt > 0:
#     leftMotor.forward(forward_speed_lt)
#     #if forward_speed_rt < 100 & forward_speed_rt > 0:
#     rightMotor.forward(forward_speed_rt)
#     if( compass.tc_heading() < (heading_straight - 2)):
#         if forward_speed_lt < 100:
#             forward_speed_lt = forward_speed_lt + 1
#     elif (compass.tc_heading() > (heading_straight + 2)):
#         if forward_speed_rt > 0:
#             forward_speed_lt = forward_speed_lt - 1 
#     else: 
#         forward_speed_lt = 50
#         forward_speed_rt = 50
time.sleep(10)
bladeMotor.stop()

testRelay1.disable()
testRelay2.disable()

print("test over")
GPIO.cleanup()

