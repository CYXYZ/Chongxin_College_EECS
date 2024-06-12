"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self,numeratorPoly,denominatorPoly):

        self.numerator = numeratorPoly
        self.denominator = denominatorPoly

    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__

    def poles(self):

         COEFFS = self.denominator.coeffs[:]
         COEFFS.reverse()
         return poly.Polynomial(COEFFS).roots()

    def poleMagnitudes(self):

        polemagnitudes=[abs(i) for i in self.poles()] 
        return polemagnitudes

    def dominantPole(self):

        return util.argmax(self.poles(),abs)
        
def Cascade(sf1,sf2):

    return SystemFunction(sf1.numerator*sf2.numerator,sf1.denominator*sf2.denominator)

    pass

def FeedbackSubtract(sf1, sf2=None):

    if sf2 == None:
        sf2 = SystemFunction(poly.Polynomial([1]), poly.Polynomial([1]))
    return SystemFunction(sf1.numerator * sf2.denominator, sf1.denominator * sf2.denominator + sf1.numerator * sf2.numerator)
    
    pass

