x=int(input())
g=x/2
while True:
 y=(g+x/g)/2
 if abs (g-y)<0.00001:
  break
 g=y
g="%.3f"%g
print(g)
