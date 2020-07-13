from collections import defaultdict, deque
from copy import deepcopy

#Rule: (int, sign)
#Sign: -1, 0, 1 == dies, stays, lives

#Rules
conways = [(2,0),(3,1)]

#Neighborhoods
vonNeumann = [(-1,+0),(+1,+0),(-0,+1),(-0,-1)]
moore = vonNeumann + [(+1,+1),(+1,-1),(-1,+1),(-1,-1)]

class game:
	def __init__(self, height=50, width=50, rules=conways, liveCells=[], historySize=4):
		#Create matrix
		self.map = [[False for i in range(width)] for i in range(height)]
			
		#Populate matrix
		self.liveCells = set(liveCells)
		for pos in self.liveCells:
			self.map[pos[0]][pos[1]] = True
		
		self.auxMap = deepcopy(self.map)		# Equals the main map before and after the tick. During the tick it equals the map before the tick.

		self.cellsHistory = deque([self.liveCells],maxlen=historySize)

		#Store rules, with -1 (dies) being the default for non-declared number of  neighbors
		self.rules = defaultdict(lambda:-1, rules)

	def _evolveCell(self,x,y):
		
		neighbors = self._liveNeighbors(x,y)
		isAlive = self.auxMap[x][y]
		
		return self.rules[neighbors] == 1 or self.rules[neighbors] == 0 and isAlive
		

	def _liveNeighbors(self, x,y):
		count = 0
		for (side1, side2) in moore:
			i = (x + side1) % len(self.map)
			j = (y + side2) % len(self.map[0])
				
			count += self.auxMap[i][j]
		return count

		
	def _naiveTick(self):
		for i in range(len(self.map)):
			for j in range(len(self.map[i])):

				aliveBefore = self.auxMap[i][j]
				self.map[i][j] = self._evolveCell(i,j)
				aliveNow = self.map[i][j]
				
				if aliveBefore and not aliveNow:
					self.liveCells.remove((i,j))
				
				if not aliveBefore and aliveNow:
					self.liveCells.add((i,j))
			
	def _evolveLivingAndCo(self):
		
			
		for cell in self.cellsHistory[0].copy():
			for (side1, side2) in moore:
				i, j = cell[0]+side1, cell[1]+side2
				i %= len(self.map)
				j %= len(self.map[0])
	
				aliveBefore = self.map[i][j]
				self.map[i][j] = self._evolveCell(i,j)
				aliveNow = self.map[i][j]
					
				if aliveBefore and not aliveNow:
					self.liveCells.remove((i,j))
			
				if not aliveBefore and aliveNow:
					self.liveCells.add((i,j))
				

	def tick(self):
		
		if len(self.map[0]) * len(self.map) < 8 * len(self.liveCells):
			self._naiveTick()
		else:
			self._evolveLivingAndCo()
		self.auxMap = deepcopy(self.map)		
		self.cellsHistory.append(deepcopy(self.liveCells))		
		
		
