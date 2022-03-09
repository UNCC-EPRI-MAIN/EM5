## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file HMI.py
# Takes a test input number from the user in the console.

def getTestNum():
    # get test number
    while True:
        testNum = input("Enter Test Number (enter 0 for normal operation): ")
        
        try:
            testNum = int(testNum)
            return testNum
        except ValueError:
            print("Invaild Test number. Enter Test Number: ")
