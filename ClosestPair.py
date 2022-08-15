import pygame
import time
import pygame_menu
from pygame_menu import Theme
import math
import copy
import random
import time

WIDTH = 800
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))

fonte = pygame.font.SysFont("hack",50)

pygame.display.set_caption("Closest Pair Distance")

global pos_line

RED = (255, 0, 0)
GREEN = (0, 255, 100)
WHITE = (25, 25, 25)
GREY = (55,55,55)
BLACK = (0,0,0)
BLUE = (0,0,255)
white = (255,255,255)

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_pos(self):
		return self.x,self.y

class Spot:
	def __init__(self, row, col, width, total_rows,percent = 1):
		self.x = row
		self.y = col
		self.row = row * width
		self.col = col * width
		self.color = WHITE
		self.width = width
		self.total_rows = total_rows
		self.percent = percent

	def get_pos(self):
		return self.x, self.y
	
	def is_marked(self):
		return self.color == GREEN or self.color == BLUE or self.color == RED

	def make_point(self):
		self.color = GREEN

	def make_line(self):
		self.color = BLUE

	def make_area(self):
		self.color = GREY

	def unmake_point(self):
		self.color = WHITE
	
	def mark(self):
		self.color = RED

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.row, self.col, self.width * self.percent, self.width))
		#self.color = pygame.Color(0,0,0,a=0)

	def __lt__(self, other):
		return False
  
# A utility function to find the 
# distance between two points 
def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) * 
                     (p1.x - p2.x) +
                     (p1.y - p2.y) * 
                     (p1.y - p2.y)) 
  
def stripClosest(strip, size, d):
		
	# Initialize the minimum distance as d 
	min_val = d 

	#print(f"A distancia eh {d}")
		
	for i in range(size):
		j = i + 1
		while j < size and (strip[j].y - 
							strip[i].y) < min_val:
			min_val = dist(strip[i], strip[j])
			j += 1

	return min_val 

lista_d = []

def closestUtil(P, Q, n,grid,pos_line,aux):		
	# If there are 2 or 3 points, 	
	# then use brute force 
	if n <= 3:
		for i in P:
			X = i.x
			Y = i.y
			grid[X][Y].mark()

	if(n == 2):

		return dist(P[0],P[1])
	
	if(n == 3):
		return min(dist(P[0],P[1]),dist(P[1],P[2]),dist(P[0],P[2]))
	
	# Find the middle point 
	mid = n // 2
	midSpot = P[mid]

	#print(aux)

	#keep a copy of left and right branch
	Pl = P[:mid]
	Pr = P[mid:]

	time.sleep(1)

	for row in grid[midSpot.x]:
		if not row.is_marked():
			row.make_line()
		
	draw(win, grid, ROWS, width)
	

	dl = closestUtil(Pl, Q, mid,grid,pos_line,aux)
	dr = closestUtil(Pr, Q, n - mid,grid,pos_line,aux+mid) 

	# Find the smaller of two distances 
	d = min(dl, dr)
	lista_d.append(d)


	for row in grid[midSpot.x-int(d):midSpot.x + int(d) + 1]:
		for spot in row:
			if not spot.is_marked():
				spot.make_area()
	time.sleep(1)

	draw(win, grid, ROWS, width)
	
	stripP = []
	stripQ = []
	lr = Pl + Pr
	for i in range(n): 
		if abs(lr[i].x - midSpot.x) < d: 
			stripP.append(lr[i])
		if abs(Q[i].x - midSpot.x) < d: 
			stripQ.append(Q[i])

	stripP.sort(key = lambda point: point.y)

	min_a = min(d, stripClosest(stripP, len(stripP), d)) 
	min_b = min(d, stripClosest(stripQ, len(stripQ), d))


	# Find the self.closest points in strip. 
	# Return the minimum of d and self.closest 
	# distance is strip[] 
	return min(min_a,min_b)
  
# The main function that finds
# the smallest distance. 
# This method mainly uses closestUtil()
def closest(P, n,grid,pos_line):
    P.sort(key = lambda point: point.x)
    Q = copy.deepcopy(P)
    Q.sort(key = lambda point: point.y)    
  
    # Use recursive function closestUtil() 
    # to find the smallest distance 
    return closestUtil(P, Q, n,grid,pos_line,0)

def make_grid(rows, width):
	global grid
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def set_difficulty(value, difficulty):
	# Do the job here !

	global box

	box = 25

	#print(f"valor = {value}\nDificuldade = {difficulty}")

	if difficulty == 3:
		box = 10
		#print(f"box = {box}")
		return  
	elif difficulty == 2:
		box = 25
		#print(f"box = {box}")

		return 
	else:
		box = 50
		#print(f"box = {box}")
		return 

search = 1

win,width = WIN,WIDTH 


def start_the_game():
	global ROWS
	ROWS = box
	global grid
	grid = make_grid(ROWS, width)

	start = None
	end = None
	run = True
	futebol = True

	while run:

		if futebol:
			draw(win, grid, ROWS, width)
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				start = spot
				start.make_point()

			# clique com a direita do mouse significa não seleciona mais
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.unmake_point()
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					# lança o algoritmo
					# o objetivo é pegar quem é ponto marcado e quem não é 
					# ordenar quem é 
					# pegar o meio e desenhar a linha
					marked_points = []

					for row in grid:
						for point in row:
							if point.is_marked():
								x,y = point.get_pos()
								#print(x,y)
								p = Point(x,y)
								marked_points.append(p)

					#print(marked_points)

					# Driver code
					P = marked_points
					n = len(P)
					marked_points.sort(key = lambda point: point.x)
					
					pos_line  = n//2
					#print(f"Pos line = {pos_line}")
					
					for i in range(box):
						p = grid[marked_points[pos_line].x][i]
						if(not p.is_marked()):
							p.make_line()

					draw(win, grid, ROWS, width)
					
					distancee = closest(P, n,grid,pos_line)

					
					score = fonte.render(f"Closest Pair Distance :{distancee:.3f}" ,True,white)
					win.blit(score,[100,350])

					pygame.display.update()

					futebol = False
					

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

				if event.key == pygame.K_m:
					start = None
					end = None
					#grid = make_grid(ROWS, width)
					main(win,width)

				if event.key == pygame.K_r:
					lista = [ (i,j) for i in range(box) for j in range(box) ]
					random.shuffle(lista)
					for x,y in lista[:20]:
						grid[x][y].make_point()						

		
	pygame.quit()

def main(win, width):
	font = pygame_menu.font.FONT_FIRACODE

	mytheme = Theme(background_color=(0,0,0,0), # transparent background
                title_background_color=(4, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
				widget_font = font,
				widget_font_color = (255,255,255),
				widget_font_size = 15
                )

	#pygame_menu.themes.THEME_DARK
	menu = pygame_menu.Menu('Closest Pair Demostration', WIDTH, WIDTH,
		theme=mytheme)

	about_theme = pygame_menu.themes.THEME_DARK.copy()
	about_theme.widget_margin = (0, 0)
	about_theme.font = font

	about_menu = pygame_menu.Menu(
		'About', WIDTH, WIDTH,
		theme=mytheme
	)

	text = ["""Your objective is first :\n1 - Place the points or press r \n2 - Press Space\n'"""]

	for m in text:
		about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=15)
		about_menu.add.vertical_margin(30)
		about_menu.add.button('Return to menu', pygame_menu.events.BACK)

	menu.add.selector('Difficulty :', [('Easy 10 rows',3),('Medium 25 rows', 2),('Hard 50 rows', 1)],default = 1 ,onchange=set_difficulty)
	menu.add.button('Play', start_the_game)
	menu.add.button('Objective', about_menu)
	menu.add.button('Quit', pygame_menu.events.EXIT)

	menu.mainloop(WIN)

main(WIN,WIDTH)