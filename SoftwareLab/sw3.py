class V2():
	def __init__(self, Vx,Vy):
		self.x = Vx
		self.y = Vy
	def __str__(self):
		return "V2[%f, %f]" % (self.x, self.y)
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def add(self, b):
		return V2(self.x+b.x,self.y+b.y)
	def mul(self, k):
		return V2(self.x*k,self.y*k)
	def __add__(self, v):
		return self.add(v)
	def __mul__(self, k):
		return self.mul(k)
