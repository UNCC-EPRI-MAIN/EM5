import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module to be tested
from mcs.DriveControl import DriveControl

print("\n\n<---------- Testbench for Drive Control ---------->\n")


# create relay instance
# relay should be open by default
drive = DriveControl()

#test routine
time.sleep(3)
drive.straight(100)
time.sleep(5)
drive.stop()
time.sleep(3)

GPIO.cleanup()
print("\n<---------- Test Complete ---------->\n\n")