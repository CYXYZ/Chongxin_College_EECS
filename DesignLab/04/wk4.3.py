import lib601.sm as sm

def accumulator(init):
    gain=sm.Gain(1)
    delay=sm.R(init)
    accum=sm.FeedbackAdd(gain,delay)
    return accum

print(accumulator(0).transduce((range(10))))

def accumulatorDelay(init):
    delay=sm.R(init)
    accum=sm.Cascade(delay,accumulator(init))
    return accum

print(accumulatorDelay(0).transduce((range(10))))

def accumulatorDelayScaled(s,init):
    accum=sm.Cascade(sm.Gain(s),accumulatorDelay(init))
    return accum

print(accumulatorDelayScaled(0.1,0).transduce((range(10))))    
