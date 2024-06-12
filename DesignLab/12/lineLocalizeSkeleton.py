import lib601.util as util
import lib601.dist as dist
import lib601.distPlot as distPlot
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.sonarDist as sonarDist
import lib601.move as move
import lib601.seGraphics as seGraphics
import lib601.idealReadings as idealReadings

# For testing your preprocessor
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

preProcessTestData = [SensorInput([0.8, 1.0], util.Pose(1.0, 0.5, 0.0)),
                       SensorInput([0.25, 1.2], util.Pose(2.4, 0.5, 0.0)),
                       SensorInput([0.16, 0.2], util.Pose(7.3, 0.5, 0.0))]
testIdealReadings = ( 5, 1, 1, 5, 1, 1, 1, 5, 1, 5 )
testIdealReadings100 = ( 50, 10, 10, 50, 10, 10, 10, 50, 10, 50 )


class PreProcess(sm.SM):
    
    def __init__(self, numObservations, stateWidth):
        self.startState = (None, None)
        self.numObservations = numObservations
        self.stateWidth = stateWidth

    def getNextValues(self, state, inp):
        (lastUpdatePose, lastUpdateSonar) = state
        currentPose = inp.odometry
        currentSonar = idealReadings.discreteSonar(inp.sonars[0],
                                                   self.numObservations)
        # Handle the first step
        if lastUpdatePose == None:
            return ((currentPose, currentSonar), None)
        else:
            action = discreteAction(lastUpdatePose, currentPose,
                                    self.stateWidth)
            print (lastUpdateSonar, action)
            return ((currentPose, currentSonar), (lastUpdateSonar, action))

# Only works when headed to the right
def discreteAction(oldPose, newPose, stateWidth):
    return int(round(oldPose.distance(newPose) / stateWidth))

pp1=PreProcess(10, 1.0)
##print pp1.transduce(preProcessTestData,verbose=True)

####noise = 3
def makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations):
    
    startDistribution = dist.squareDist(0,numStates)    
    
    def observationModel(ix):
        noise = 3
        Fully_triangular_distribution = dist.triangleDist(ideal[ix],noise,0,numObservations-1)
        Fully_square_distribution = dist.squareDist(0,numObservations)
        Delta_distribution = dist.DeltaDist(numObservations-1)
        
        return dist.MixtureDist(Fully_triangular_distribution,
                                dist.MixtureDist(Fully_square_distribution
                                                 ,Delta_distribution,0.5)
                                ,0.8)

    def transitionModel(a):
        noise = 3
        def transitionGivenI(oldState):
##            print dist.triangleDist(util.clip(oldState+a, 0, numStates-1),
##                                     noise, 0, numStates-1)
            return dist.triangleDist(util.clip(oldState+a, 0, numStates-1),
                                     noise, 0, numStates-1)
        
        return transitionGivenI

##    distPlot.plot(transitionModel(2)(5))
##    distPlot.plot(observationModel(7))
        
    return ssm.StochasticSM(startDistribution, transitionModel,
                            observationModel)

##model100 = makeRobotNavModel(testIdealReadings100, 0.0, 10.0, 10, 100)

##model = makeRobotNavModel(testIdealReadings, 0.0, 10.0, 10, 10)
##model.observationDistribution
##model.transitionDistribution
##pp1=PreProcess(10, 1.0)
##pp2 = seGraphics.StateEstimator(model)
##ppEst = sm.Cascade(pp1,pp2)
##print ppEst.transduce(preProcessTestData,verbose = True)
    
####
# Main procedure
def makeLineLocalizer(numObservations, numStates, ideal, xMin, xMax, robotY):
    stateWidth = (xMax-xMin)/float(numStates)
    pp1=PreProcess(numObservations,stateWidth)
    model = makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations)
    pp2 = seGraphics.StateEstimator(model)
    ppEst = sm.Cascade(pp1,pp2)
    driver = move.MoveToFixedPose(util.Pose(xMax, robotY, 0.0), maxVel = 0.5)
    return sm.Cascade(sm.Parallel(ppEst, driver), sm.Select(1))

