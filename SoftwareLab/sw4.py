import lib601.sm as sm


class BA1(sm.SM):
        startState = 0
        def getNextValues(self, state, inp):
            if inp != 0:
                newState = state * 1.02 + inp - 100
            else:
                 newState = state * 1.02
            return (newState, newState)

class BA2(sm.SM):
        startState = 0
        def getNextValues(self, state, inp):
            newState = state * 1.01 + inp
            return (newState, newState)
    

ba1=BA1()
ba2=BA2()
maxAccount = sm.Cascade(sm.Parallel(ba1,ba2),sm.PureFunction(max))
a=[1000,5000,2000,4000,500]
maxAccount.transduce(a,verbose = True)

def condition(inp):
        if inp>3000:
                return True
        else:
                return False
class switch(sm.Switch):
    startState = 0
    def __init__(self, condition, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.condition = condition
        return
        
    def getNextValues(self, state, inp):
        if self.condition:
            return (state, (inp, 0))
        else:
            return (state, (0, inp))

switchAccount = sm.Cascade(switch(), sm.Cascade(sm.Parallel2(ba1, ba2),sm.PureFunction(sum)))
a=[1000,5000,2000,4000,500]
switchAccount.transduce(a,verbose = True)
