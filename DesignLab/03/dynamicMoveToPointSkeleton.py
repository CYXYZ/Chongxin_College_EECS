import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
##import lib601.io as io
# Use this line for testing in soar
from soar.io import io

class DynamicMoveToPoint(sm.SM):
    def getNextValues(self, state, inp):
        (goalPoint,sensors)=inp
        p0=sensors.odometry
        if abs(p0.point().distance(goalPoint))<0.02:
            return (state,io.Action(fvel=0,rvel=0))

        elif util.nearAngle(p0.theta,p0.point().angleTo(goalPoint),0.03):
            return (state,io.Action(fvel=(p0.point().distance(goalPoint))/1.2,rvel=0))        

        else:
            return (state,io.Action(fvel=0,rvel= util.fixAnglePlusMinusPi(p0.point().angleTo(goalPoint)-p0.theta)))
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'
        return (state, io.Action())
