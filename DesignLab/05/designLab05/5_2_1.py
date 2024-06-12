import lib601.sf as sf

def controllerSF(k):

    return sf.Gain(k)

def plantSF(T):

    return sf.Cascade(sf.Cascade(sf.R(),sf.Gain(-T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))


def sensorSF():
    
    return sf.R()

def wallFinderSystem(T,k):
    
    return sf.FeedbackSubtract(sf.Cascade(controllerSF(k),plantSF(T)),sf.controllerSF(1))
