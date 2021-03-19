import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module to be tested
from mcs.firmware.RelayControl import RelayControl

print("\n\n<---------- Testbench for RelayControl ---------->\n")


# create relay instance
# relay should be open by default
r1Pin = 23
r1DebugFlag = True
r1EnabledFlag = True
r1DebugName = "relay1"
r2Pin = 24
r2DebugFlag = True
r2EnabledFlag = True
r2DebugName = "relay1"
r3Pin = 25
r3DebugFlag = True
r3EnabledFlag = True
r3DebugName = "relay1"
r1 = RelayControl(r1Pin, r1DebugFlag, r1EnabledFlag, False, r1DebugName)
r2 = RelayControl(r2Pin, r2DebugFlag, r2EnabledFlag, False, r2DebugName)
r3 = RelayControl(r3Pin, r3DebugFlag, r3EnabledFlag, False, r3DebugName)


#test routine
time.sleep(2)
r1.enable()
time.sleep(2)
r1.disable()
time.sleep(2)
r2.enable()
time.sleep(2)
r2.disable()
time.sleep(2)
r3.enable()
time.sleep(2)
r3.disable()
time.sleep(2)

GPIO.cleanup()
print("\n<---------- Test Complete ---------->\n\n")