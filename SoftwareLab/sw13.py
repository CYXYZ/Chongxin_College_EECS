import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = ('L','L','L','L')
   legalInputs = ['takeNone','takeGoat','takeWolf','takeCabbage']
      
   def getNextValues(self, state, action):
      lstate = list(state)
      if action == 'takeNone':
         if lstate[1] == lstate[3] or lstate[1] == lstate[2]:
            lstate[0] = keep(lstate[0])
         else:
            lstate[0] = transform(lstate[0])

      elif action == 'takeGoat':
         if lstate[0] != lstate[1]:
            lstate[0] = keep(lstate[0])
            lstate[1] = keep(lstate[1])
         else:
            lstate[0] = transform(lstate[0])
            lstate[1] = transform(lstate[1])

      elif action == 'takeWolf':
         if lstate[1] == lstate[3] or lstate[0] !=lstate[2]:
            lstate[0] = keep(lstate[0])
            lstate[2] = keep(lstate[2])
         else:
            lstate[0] = transform(lstate[0])
            lstate[2] = transform(lstate[2])

      elif action == 'takeCabbage':
         if lstate[1] == lstate[2] or lstate[0] != lstate[3]:
            lstate[0] = keep(lstate[0])
            lstate[3] = keep(lstate[3])
         else:
            lstate[0] = transform(lstate[0])
            lstate[3] = transform(lstate[3])
      
      return (tuple(lstate),tuple(lstate))
   
   def done(self, state):
      return state == ('R','R','R','R')
      
def transform(state0):
   if state0 == 'L':
      state0 = 'R'
   else:
      state0 = 'L'
   return state0
   
def keep(state1):
   if state1 == 'L':
      stata1 = 'L'
   else:
      state1 = 'R'
   return state1
   
print search.smSearch(FarmerGoatWolfCabbage(),depthFirst=False, DP=True)


