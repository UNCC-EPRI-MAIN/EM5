import time
import signal
from xbox360controller import Xbox360Controller

# module to be tested
#from mcs.ManualDriveControl import ManualDriveControl
import mcs.ManualDriveControl as ManualDriveControl
import mcs.TestFlags as flags
print("\n\n<---------- Testbench for Manual Drive Control ---------->\n")


# create relay instance
# relay should be open by default
#ManualDriveControl()
import mcs.ManualDriveControl as ManualDriveControl
#test routine
signal.pause()

print("\n<---------- Test Complete ---------->\n\n")
