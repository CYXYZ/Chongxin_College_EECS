import lib601.sf as sf
import lib601.sig as sig
import lib601.ts as ts
import lib601.optimize as optimize
import math
import lib601.poly as poly
# 6.01 HomeWork 2 Skeleton File

#Constants relating to some properties of the motor
k_m = 1000
k_b = 0.5
k_s = 5
r_m = 20

def controllerAndSensorModel(k_c):
    return sf.Gain(k_c*k_s)

def integrator(T):
    sf1=sf.Cascade(sf.R(),sf.Gain(T))
    sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
    return sf.Cascade(sf1,sf2)

def motorModel(T):
    gain1=k_m*T/r_m
    gain2=(k_m*k_b*T-r_m)/r_m
    sf1=sf.Cascade(sf.R(),sf.Gain(gain1))
    sf2=sf.FeedbackSubtract(sf.Gain(1),sf.Cascade(sf.R(),sf.Gain(gain2)))
    return sf.Cascade(sf1,sf2)

def plantModel(T):
    return sf.Cascade(motorModel(T),integrator(T))
                       
def lightTrackerModel(T,k_c):
    sf1=sf.Cascade(controllerAndSensorModel(k_c),plantModel(T))
    return sf.FeedbackSubtract(sf1,sf.Gain(1))

def plotOutput(sfModel):
    """Plot the output of the given SF, with a unit-step signal as input"""
    smModel = sfModel.differenceEquation().stateMachine()
    outSig = ts.TransducedSignal(sig.StepSignal(), smModel)
    outSig.plot()
plotOutput(lightTrackerModel(0.005,1))
plotOutput(lightTrackerModel(0.01,1))
plotOutput(lightTrackerModel(0.001,1))



def bestkc(T,kcMin,kcMax,numSteps):
    def y(kc):
        sf1=sf.SystemFunction(poly.Polynomial([0.125*kc,0,0]),poly.Polynomial([0.125*kc+17.5,-37.5,20]))
        return sf1.dominantPole()
    print optimize.optOverLine(y,kcMin,kcMax,numSteps)
    print ('kcMin=%f'%kcMin,'kcMax=%f'%kcMax)
    
#bestkc(0.005,0,0.62,10000)
