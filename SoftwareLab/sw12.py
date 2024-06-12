import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        (o, i) = inp
        #Get B= Pr(St|Ot)
        total = 0.0
        afterObs = state.d.copy()
        for s in state.support():
                afterObs[s] *= self.model.observationDistribution(s).prob(o)
                total += afterObs[s]
        B = {}
        for s in afterObs.keys():
                B[s] = afterObs[s] / total
        #Get Pr(St+1|Ot)
        new = {}
        tDist = self.model.transitionDistribution(i)
        for s in afterObs.keys():
                NtDist = tDist(s)
                for sPrime in NtDist.support():
                    dist.incrDictEntry(new, sPrime, NtDist.prob(sPrime) * B[s])

        dSPrime = dist.DDist(new)
        return (dSPrime, dSPrime)


# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print cmse.transduce(obs)


