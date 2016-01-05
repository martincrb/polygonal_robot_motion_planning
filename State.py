
class State:
    def __init__(self):
        self.states = ["None",
                       "COMPUTING_MINKOWSKI_SUMS",
                       "DRAWING_ROBOT",
                       "DRAWING_OBSTACLE",
                       "SELECT_TARGET"]
        self.actual = "None"

    def getActualState(self):
        return self.actual

    def setActualState(self, actual):
        if actual == None: actual = "None"
        if actual not in self.states:
            print "State not valid"
        else:
            self.actual = actual