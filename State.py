
class State:
    def __init__(self):
        self.states = [None,
                       "DRAWING_ROBOT",
                       "DRAWING_OBSTACLE",
                       "SELECT_TARGET"]
        self.actual = None

    def getActualState(self):
        return self.actual

    def setActualState(self, actual):
        if actual not in self.states:
            print "State not valid"
        else:
            self.actual = actual