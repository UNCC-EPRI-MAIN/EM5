## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file UART.py
# Sends and receive messages through uart.

import serial
import time

## This class is used start uart on the GPIO
# The class setup the uart pins, send and receive messages, and cleans up.
class UART:

    ##  Constructor for UART module.
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out.
    def __init__(self, debugFlag, enabledFlag):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag

        ## Boolean to indicate if UART should be used.
        self.enabled = enabledFlag

        ## String for debugging
        self.debugPrefix = "[UART]"

        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"

        try:
            self.uart = serial.Serial("/dev/ttyAMA0", baudrate=9600)

            # Wait until the port is ready to send and receive data.
            while not self.uart.is_open:
                time.sleep(0.1)

            if self.debug:
                print(self.debugPrefix + "[__init__()]: Using Tx and Rx Pins.")
                print(self.debugPrefix + "[__init__()]: Completed Setup of UART.")

        except:
            if self.debug:
                print(self.debugPrefix + "[__init__()]: Failed to setup UART.")
            self.uart = None

    ## Return a line from the other microcontroller.
    def ReadMessage(self):
        recv_message = ""

        if self.uart != None:
            recv_message = self.uart.readline()
        elif self.debug:
            print(self.debugPrefix + "Can't read the port, UART is not setup.")
            time.sleep(1)

        return recv_message

    ## Send a message over UART with a newline.
    def SendMessage(self, message):
        if self.uart != None:
            self.uart.write(message + '\n')
        elif self.debug:
            print(self.debugPrefix + "Failed to send the message")
        

    ## Close the port.
    def CleanUp(self):
        self.uart.flushInput()
        self.uart.flushOutput()
        self.uart.close()
