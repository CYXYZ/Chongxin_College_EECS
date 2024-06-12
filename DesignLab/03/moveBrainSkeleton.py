import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
print 'setting labPath to', labPath

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Remember to change the import in dynamicMoveToPointSkeleton in order
# to use it from inside soar
import dynamicMoveToPointSkeleton
reload(dynamicMoveToPointSkeleton)

import ffSkeleton
reload(ffSkeleton)

from secretMessage import secret

# Set to True for verbose output on every step
verbose = True

# Rotated square points

squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]

lovePoints = [util.Point(0.63,0.51), util.Point(1.00,1.00),
                util.Point(1.14,1.51), util.Point(1.08,1.85),
                util.Point(0.87,2.13), util.Point(0.54,2.24),
                util.Point(0.26,2.19), util.Point(0,2.01),
                util.Point(-0.25,2.18), util.Point(-0.56,2.23),
                util.Point(-0.87,2.13),util.Point(-1.09,1.84),
                util.Point(-1.14,1.53),util.Point(-1.00,1.00),
                util.Point(-0.62,0.50),util.Point(0,0)]

checkpoint = [util.Point(1.0,0.5)]

GoalGenerator = ffSkeleton.FollowFigure(squarePoints)
DynamicMoveToPoint = dynamicMoveToPointSkeleton.DynamicMoveToPoint()

def condition(inp):
    for i in range (7):
        if inp.sonars[i]<0.3:
            return True
    return False

class stop(sm.SM):
    def getNextValues(self, state, inp):
        return (state,io.Action(fvel=0,rvel=0))

# Put your answer to step 1 here
mySM = sm.Switch(condition,stop(),sm.Cascade(sm.Parallel(GoalGenerator,sm.Wire()),DynamicMoveToPoint))

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail = True)
    robot.behavior = mySM

def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(),
                         verbose = verbose)

def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())

def brainStop():
    pass

def shutdown():
    pass
