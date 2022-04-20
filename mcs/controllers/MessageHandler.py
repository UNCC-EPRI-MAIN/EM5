## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file MessageHandler.py
# Handles the messages and reads them and then runs a simple if statement to control the robot.

# Standard libraries
import importlib

# Firmware modules
import mcs.firmware.UART as uart

## The function that the spawned process uses.
def run(globals):

    # load test flags
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.MessageHandler_debug

    ## Boolean to indicate if the message handler should be used. 
    enabled = tFlags.MessageHandler_enabled

    command_mode = tFlags.MessageHandler_command

    ## String used for debugging
    debugPrefix = "[MessageHandler]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init message handler")

    if enabled:
        ## The uart class object.
        jetson_uart = uart.UART(tFlags.uart_debug, tFlags.uart_enabled)


    # main loop, run until end of program
    while globals['state'] != 'shutdown':

        recv_message = jetson_uart.ReadMessage()

        if debug and recv_message != b'':
            print(debugPrefix + "Message: " + str(recv_message))

        if recv_message == b'blocked\n':
            globals['blocked'] = True

        if recv_message == b'not blocked\n':
            globals['blocked'] = False

        # This allows us to command the RPI from the jetson
        if command_mode:
            if recv_message == b'Shutdown\n':
                globals['state'] = 'shutdown'

            if recv_message == b'PivotRight\n':
                globals['driveState'] = 'pivotRight'

            if recv_message == b'pivotLeft\n':
                globals['driveState'] = 'pivotLeft'

        

    jetson_uart.CleanUp()
    print(debugPrefix + "end of module")


