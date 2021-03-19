import time
import serial
from ublox_gps import UbloxGps

# system flags used by the module under test
class TestFlags:
    NEO_M8P_debug = True
    NEO_M8P_enabled = True

# initialize flags to be passed
flags = TestFlags()

# module to be tested
import mcs.NEO_M8P as mcs

print("\n\n<---------- Testbench for NEO-M8P ---------->\n")

# declare instance of module
#   only testing a single motor
#   hardware requires second motor initialized
gps = mcs.NEO_M8P(flags)

# test routine
while True:
    time.sleep(3)
    x = gps.getX()
    y = gps.getY()
    heading = gps.compass()
    print("GPS: " + str(x) + ", " + str(y))
    print("Heading: " + str(heading))

print("\n<---------- Test Complete ---------->\n\n")
