import lib601.sig  as sig # Signal
import lib601.ts as ts  # TransducedSignal
import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def plant(T, initD):
    sm1=sm.Cascade(sm.Gain(-T),sm.R(0))
    return sm.Cascade(sm1,sm.FeedbackAdd(sm.Gain(1),sm.R(initD)))

def controller(k):
    gain=sm.Gain(k)
    return gain

def sensor(initD):
    delay=sm.R(initD)
    return delay

def wallFinderSystem(T, initD, k):
    sm1=sm.Cascade(controller(k),plant(T,initD))
    sm2=sensor(initD)
    return sm.FeedbackSubtract(sm1,sm2)

# Plots the sequence of distances when the robot starts at distance
# initD from the wall, and desires to be at distance 0.7 m.  Time step
# is 0.1 s.  Parameter k is the gain;  end specifies how many steps to
# plot. 

initD = 1.5

def plotD(k, end = 100):
  d = ts.TransducedSignal(sig.ConstantSignal(0.7),
                          wallFinderSystem(0.1, initD, k))
  d.plot(0, end, newWindow = 'Gain '+str(k))

plotD(-1,100)
plotD(-9,100)
plotD(-11,100)
