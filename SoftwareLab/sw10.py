"""
Discrete probability distributions
"""

import random
import operator
import copy

import lib601.util as util

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be
    sparse, in the sense that elements that are not explicitly
    contained in the dictionary are assumed to have zero probability.
    """
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def conditionOnVar(self, index, value):
        New = []
        for e in self.support():
            if e[index] == value:
                New.append(e)
        z = sum([ self.prob(e) for e in New ])
        return DDist(dict([ (removeElt(e, index), self.prob(e) / z) for e in New]))
    
    def marginalizeOut(self, index):
        result = {}
        for e in self.support():
            incrDictEntry(result, removeElt(e, index), self.prob(e))
        return DDist(result)

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__


######################################################################
#   Utilities


def removeElt(items, i):
    """
    non-destructively remove the element at index i from a list;
    returns a copy;  if the result is a list of length 1, just return
    the element  
    """
    result = items[:i] + items[i+1:]
    if len(result) == 1:
        return result[0]
    else:
        return result

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
# plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

# import lib601.sig as sig

# class IntDistSignal(sig.Signal):
#     def __init__(self, d):
#         self.dist = d
#     def sample(self, n):
#         return self.dist.prob(n)
# def plotIntDist(d, n):
#     IntDistSignal(d).plot(end = n, yOrigin = 0)

def PTgD(a):
    if a == 'disease':
        return DDist ({'posTest':0.9,'negTest':0.1})
    else:
        return DDist({'posTest':0.5,'negTest':0.5})

disease = DDist ({'disease':0.1,'noDisease':0.9})

def JDist(PA,PBgA):
    k = {}
    for a in PA.support():
        for b in PBgA(a).support():
            k[(a, b)] = PA.prob(a) * PBgA(a).prob(b)
    return DDist(k)

def bayesEvidence(PBgA,PA,b):
    return JDist(PA,PBgA).conditionOnVar(1,b)

print bayesEvidence(PTgD,disease,'posTest')
print bayesEvidence(PTgD,disease,'negTest')

def totalProbability(PBgA,PA):
    return JDist(PA, PBgA).marginalizeOut(0)

print totalProbability(PTgD,disease)
