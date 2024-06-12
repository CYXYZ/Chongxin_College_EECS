import operator
import lib601.util as util

#-----------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------

class MixtureDist:
    def __init__(self, d1, d2, p):

        self.d1 = d1
        self.d2 = d2
        self.p = p
        
        pass
        
    def prob(self, elt):
        
        return self.d1.prob(elt)*self.p + self.d2.prob(elt)*(1.0-self.p)

        pass

    def support(self):

        return list(set(self.d1.support()+self.d2.support()))
        
        pass

    def __str__(self):
        result = 'MixtureDist({'
        elts = self.support()
        for x in elts[:-1]:
            result += str(x) + ' : ' + str(self.prob(x)) + ', '
        result += str(elts[-1]) + ' : ' + str(self.prob(elts[-1])) + '})'
        return result
    
    __repr__ = __str__


#生成矩形分布方法一，本方法使用简单的枚举法

def squareDist(lo, hi, loLimit = None, hiLimit = None):
    dist = {}
    p = 1.0/(hi-lo)
    
    if loLimit == hiLimit == None or loLimit < lo and hiLimit > hi:
        for i in range(lo, hi):
            dist [i] = p

    elif hi <= loLimit:
        dist[loLimit] = 1.0

    elif lo >= hiLimit:
        dist[hiLimit] = 1.0
        
    elif lo <= loLimit and hi > loLimit and hi < hiLimit:
        for i in range(loLimit, hi):
            dist [i] = p 
        dist [loLimit] = p+p * (loLimit - lo)

    elif lo < hiLimit and hi > hiLimit and lo >= loLimit:
        for i in range(lo, hiLimit):
            dist [i] = p 
        dist [hiLimit] = p+p * (hi - hiLimit-1)

    elif lo < hiLimit and hi == hiLimit and lo >= loLimit:
        for i in range(lo, hiLimit):
            dist [i] = p

    elif lo < loLimit and hiLimit < hi:
        for i in range(loLimit, hiLimit):
            dist [i] = p
        dist [loLimit] = p+p * (loLimit - lo)
        dist [hiLimit] = p+p * (hi - hiLimit-1)

    return DDist(dist)

#生成矩形分布方法二，采用incrDictEntry和util.clip方法

##def squareDist(lo, hi, loLimit = None, hiLimit = None):
##
##    d = {}
##    p = 1/(hi - lo)
##
##    for i in (lo, hi):
##        incrDictEntry(d, util.clip(i, loLimit, hiLimit), p)
##
##    return DDist(d)


#生成三角分布方法一，本方法依然采用枚举法，用数学方法观察到三角分布的最小概率值是 1.0/halfWidth**2

def triangleDist(peak, halfWidth, loLimit = None, hiLimit = None):

    dist = {}
    p=1.0/halfWidth**2
     
    if halfWidth == 1.0:
        dist[peak] = 1.0

    elif loLimit == hiLimit == None or (peak - halfWidth + 1) >= loLimit and (peak + halfWidth - 1) <= hiLimit:
        for i in range(peak - halfWidth + 1, peak + halfWidth ):
            if i<= peak:
                dist[i] = p+p*(i - (peak - halfWidth + 1))   
            else:
                dist[i] = p+p*(peak + halfWidth -1 -i)
        
    elif (peak + halfWidth - 1) <= loLimit:
        dist[loLimit] = 1.0

    elif (peak - halfWidth + 1) >= hiLimit:
        dist[hiLimit] = 1.0

    elif (peak - halfWidth +1) < loLimit and (peak + halfWidth - 1) <= hiLimit:
        dist[loLimit] = 1
        for i in range(loLimit+1 , peak + halfWidth ):
            if i<= peak:
                dist[i] = p+p*(i - (peak - halfWidth + 1))
            else:
                dist[i] = p+p*(peak + halfWidth -1 -i)
            dist[loLimit] = dist[loLimit] - dist [i]

    elif (peak - halfWidth + 1) >= loLimit and (peak + halfWidth - 1) > hiLimit:
        dist[hiLimit] = 1
        for i in range(peak - halfWidth + 1 , hiLimit):
            if i<= peak:
                dist[i] = p+p*(i - (peak - halfWidth + 1))
            else:
                dist[i] = p+p*(peak + halfWidth -1 -i)
            dist[hiLimit] = dist[hiLimit] - dist[i]

    elif loLimit+1 == hiLimit:
        dist[loLimit] = 0.5
        dist[hiLimit] = 0.5

    else:
        dist[loLimit] = (1.0- (p+p*(halfWidth-1)))/2.0
        dist[hiLimit] = (1.0- (p+p*(halfWidth-1)))/2.0
        for i in range(loLimit+1 , hiLimit):
            if i<= peak:
                dist[i] = p+p*(i - (peak - halfWidth + 1))  
            else:
                dist[i] = p+p*(peak + halfWidth -1 -i)

        for i in range(loLimit+1 , hiLimit):
            if i< peak:
                dist[loLimit] = dist[loLimit] - dist[i]
            if i> peak:
                dist[hiLimit] = dist[hiLimit] - dist[i]

    return DDist(dist)

#生成三角分布方法二，仍然采用incrDictEntry和util.clip方法，观察到最小概率仍然是1.0/halfWidth**2
#考虑矩形分布，三角分布可以看作几个矩形分布对应概率的和，因此使用两个for循环对其进行缩小区间的叠加

##def triangleDist(peak, halfWidth, loLimit = None, hiLimit = None):
##    d={}
##    p=1.0/halfWidth**2
##
##    for i in range(peak - halfWidth +1, peak + halfWidth):
##        for a in range(i, 2*peak-i+1):
##            incrDictEntry(d, util.clip(a, loLimit, hiLimit), p)
##    return DDist(d)









#-----------------------------------------------------------------------------
# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
#plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

import lib601.sig as sig

class IntDistSignal(sig.Signal):
     def __init__(self, d):
         self.dist = d
     def sample(self, n):
         return self.dist.prob(n)
def plotIntDist(d, n):
     IntDistSignal(d).plot(end = n, yOrigin = 0)

##plotIntDist(triangleDist(40,20),100)
##plotIntDist(triangleDist(30,20),100)
plotIntDist(MixtureDist(triangleDist(40,20), triangleDist(30,20),0.5), 100)
