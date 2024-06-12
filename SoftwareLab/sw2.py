cube = float( input( "请输入一个任意实数: "))
epsilon = 0.001
num_guesses = 0
if abs(cube) > 1 :
   low = 0
   high = abs(cube)

elif abs (cube) < 1 and abs (cube)>0 :
        low = 0
        high = 1
else :
     low = 0
     high = 0
guess = (high + low) / 2.0

while abs (guess **3 - abs (cube)) >= epsilon:
         if      guess **3 < abs (cube) :
                 low = guess 
         else :
                 high = guess
         guess = ( high + low ) / 2.0
         num_guesses +=1
print ( 'num_guesses = ',num_guesses )
if cube < 0 :
   print ( '%.4f' %-guess , ' is close to the cube root of ' , cube )
elif cube > 0 :
     print ( '%.4f' %guess , ' is close to the cube root of ' , cube )
else :
     print ( 0 ,' is close to the cube root of ' , cube )
