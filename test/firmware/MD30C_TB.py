import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)    # sets gpio mode to board

# module to be tested
from mcs.firmware.MD30C import MD30C

print("\n\n<---------- Testbench for MD30C (Blade Motor Driver) ---------->\n")

# declare instance of module
#   only testing a single motor
#   hardware requires second motor initialized
pinNumber = 16
enabledFlag = False
debugFlag = True
bladeMotor = MD30C(pinNumber, debugFlag, enabledFlag)

# test routine
time.sleep(3)
bladeMotor.spin()
time.sleep(15)
bladeMotor.stop()
time.sleep(5)

GPIO.cleanup()
print("\n<---------- Test Complete ---------->\n\n")
