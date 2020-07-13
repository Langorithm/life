import sys, pygame, gameOfLife
from random import randint
from copy import deepcopy
pygame.init()

size = X, Y = 100, 100
scale = int(input("scale: "))
black = 0, 0, 0
blackT = 10,10,10,250
white = 0xFF, 0xFF, 0xFF

lYellow = 255,255,210
yellow = 200,200,100
dYellow = 150,120,70
rdYellow = 140,140,70

p1 = pygame.Rect(0,0,15,60)

livingNum =int( input("# living cells: "))
livingCells = set()
while len(livingCells) < livingNum:
	livingCells.add((randint(0,X-1), randint(0,Y-1)))
glider = [(2,1),(3,2),(3,3),(2,3),(1,3)]	

#livingCells=glider
g = gameOfLife.game(height=X,width=Y,liveCells=livingCells)


colors = [white, lYellow, yellow, dYellow,rdYellow]
#colors.reverse()
f = pygame.BLEND_SUB
def draw():

	screen.fill(blackT,special_flags=f)

	#pygame.draw.rect(screen, white, p1)
	for cell in g.liveCells:
		x,y = cell

		age = 0
		while(age < len(g.cellsHistory) and cell in g.cellsHistory[age] ):
			age+=1
	
		x *= scale
		y *= scale
		sqr = pygame.Rect(x,y,scale,scale)
				
		pygame.draw.rect(screen,colors[age],sqr)

	pygame.display.flip()

screensize = X*scale, Y*scale
screen = pygame.display.set_mode(screensize)
screen.convert_alpha()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		draw()
		g.tick()

    
