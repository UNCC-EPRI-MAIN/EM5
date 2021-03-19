import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# module to be tested
from mcs.firmware.Sabertooth2x60 import Sabertooth2x60

print("\n\n<---------- Testbench for Sabertooth2x60 ---------->\n")

# declare instance of module
#   only testing a single motor
#   hardware requires second motor initialized
lpin = 11
ldebugFlag = True
lenabledFlag = False
ldebugName = "Left"
rpin = 13
rdebugFlag = True
renabledFlag = False
rdebugName = "Right"
leftMotor = Sabertooth2x60(lpin, ldebugFlag, lenabledFlag, ldebugName)
rightMotor = Sabertooth2x60(rpin, rdebugFlag, renabledFlag, rdebugName)

# test routine
time.sleep(3)
leftMotor.forward(25)
time.sleep(2)
leftMotor.forward(50)
time.sleep(2)
leftMotor.forward(75)
time.sleep(2)
leftMotor.forward(100)
time.sleep(2)
leftMotor.forward(75)
time.sleep(2)
leftMotor.forward(50)
time.sleep(2)
leftMotor.forward(25)
time.sleep(2)
leftMotor.stop()
time.sleep(2)
leftMotor.backward(25)
time.sleep(2)
leftMotor.backward(50)
time.sleep(2)
leftMotor.backward(75)
time.sleep(2)
leftMotor.backward(100)
time.sleep(2)
leftMotor.backward(75)
time.sleep(2)
leftMotor.backward(50)
time.sleep(2)
leftMotor.backward(25)
time.sleep(2)
leftMotor.stop()
time.sleep(3)

GPIO.cleanup()
print("\n<---------- Test Complete ---------->\n\n")
