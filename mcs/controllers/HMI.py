def getTestNum():
    # get test number
    while True:
        testNum = input("Enter Test Number: ")
        
        try:
            testNum = int(testNum)
            return testNum
        except ValueError:
            print("Invaild Test number. Enter Test Number: ")
