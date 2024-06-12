import lib601.sm as sm
import lib601.util as util
import math

class FollowFigure(sm.SM):

    def __init__(self, points):
        self.startState = 0
        self.points = points

    def getNextValues(self, state, inp):
        lens = len(self.points)
        p0=inp.odometry.point()
        i=state
        while i < lens-1 :
                if p0.isNear(self.points[i],0.03):
                    return (state+1,self.points[i+1])
                else:
                    return (state,self.points[i])
        return (state,self.points[i])
