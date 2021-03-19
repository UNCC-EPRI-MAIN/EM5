import math

AX = -80.7096746
AY = 35.2376407
BX = -80.70963189999
BY = 35.2376935
CX = -80.70962349999
CY = 35.23761299999
DX = -80.7095595
DY = 35.2375543

EAY = 39.099912
EAX = -94.581213
EBY = 38.627089
EBX = -90.200203

def getCompassHeading(TAX, TAY, TBX, TBY):
    TAX = math.radians(TAX)
    TAY = math.radians(TAY)
    TBX = math.radians(TBX)
    TBY = math.radians(TBY)
    y = math.cos(TBY) * math.sin(TBX - TAX)
    print(str(y))
    x = math.cos(TAY) * math.sin(TBY) - math.sin(TAY) * math.cos(TBY) * math.cos(TBX - TAX)
    print(str(x))
    heading = math.atan2(x, y)
    heading = math.degrees(heading)
    if heading < 0:
        heading += 360
    print(str(heading))

A1X = -80.7096718999999
A1Y = 35.2376376
A2X = -80.7096722
A2Y = 35.2376383

getCompassHeading(AX, AY, DX, DY)

from geopy.distance import great_circle
#from geopy.distance import vincenty

p1 = (A1Y, A1X)
p2 = (A2Y, A2X)

distance = great_circle(p1, p2)
distance = distance * 3280.84
#print(str(vincenty(p1, p2)))
print(str(distance))