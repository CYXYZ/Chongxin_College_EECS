import lib601.sig as sig
import lib601.ts as ts
import lib601.poly as poly
import lib601.sf as sf

from cmath import *
import math

def controller(k):

   return sf.Gain(k)

   pass

def plant1(T):

   return sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))
   
   pass

def plant2(T, V):

   return sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T*V)),sf.FeedbackAdd(sf.Gain(1),sf.R()))

   pass

def wallFollowerModel(k, T, V):

   return sf.FeedbackSubtract(sf.Cascade(sf.Cascade(controller(k),plant1(T)),plant2(T,V)),sf.Gain(1))

   pass

##This is Wk5.3.4##
##def wallFollowerModel(k, T, V):
##
##   return sf.FeedbackSubtract(sf.Cascade(sf.Cascade(sf.Gain(k),sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))),sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T*V)),sf.FeedbackAdd(sf.Gain(1),sf.R()))),sf.Gain(1))
##
##   pass   

a= wallFollowerModel(1,0.1,0.1).dominantPole()
print(a)
b=polar(a)
print(b)
period=2*math.pi/b[1]
print(period)
