## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file Waypoints.py
# A class file to hold waypoints in a file and load waypoints from a file.

from dataclasses import dataclass

@dataclass
class waypoint:
    lat: float
    long: float

class Path:
    def __init__(self):
        self.path = []
        self.completedPath = []
        self.currentWaypoint = None
        self.currentWaypointIndex = 0
        self.RTB = False
    
    def print(self):
        for waypoint in self.path:
            print(waypoint)

    def IsRTB(self):
        return self.RTB

    def BackTrack(self):
        # Get the old path and reverse it.
        self.path = self.completedPath
        self.currentWaypointIndex = 0
        self.path.reverse()

        # Store the new waypoint
        self.currentWaypoint = self.path[self.currentWaypointIndex]

        # Set the returning to base flag to true
        self.RTB = True

        # Return
        return self.currentWaypoint

    def NextWaypoint(self):
        # Sanity check on the list.
        if len(self.path) <= self.currentWaypointIndex:
            print("[Path Class]: There is not a path to get. Need to load the waypoints in")
            return None

        # Save the completed path for later
        self.completedPath.append(self.path[self.currentWaypointIndex])

        # Get the next waypoint.
        self.currentWaypointIndex += 1
        self.currentWaypoint = self.path[self.currentWaypointIndex]

        return self.currentWaypoint

    def GetCurrentWaypoint(self):
        if self.currentWaypoint == None:

            if len(self.path) == 0:
                print("[Path Class]: There is not a path to get. Need to load the waypoints in")
            elif len(self.path) <= self.currentWaypointIndex:
                print("[Path Class]: There is not a path to get.")
            else:
                self.currentWaypoint = self.path[self.currentWaypointIndex]

        return self.currentWaypoint

    def NewWaypoint(self, lat, long):
        self.path.append(waypoint(lat, long))

    def WritePathToFile(self):
        with open('./GPSWaypoints.txt', 'w') as file:
            for waypoint in self.path:
                file.write(str(waypoint.lat) + ',' + str(waypoint.long) + '\n')

    def LoadPathFromFile(self):
        file_content = []
        with open('./GPSWaypoints.txt', 'r') as file:
            file_content = file.readlines()

        self.path.clear()

        for line in file_content:
            line = line.split(",")
            self.path.append(waypoint(float(line[0]), float(line[1])))
    
    