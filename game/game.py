import pygame
from abc import ABC, abstractmethod

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 0)
yellow = (255, 255, 0)

f1 = pygame.font.Font(None, 36)

def field_from_file():
	f = open('matrix2.txt','r')
	size = f.readline().split("x")
	lines = int(size[0])
	colums = int(size[1])
	wall_keys = []
	trap_keys = []
	money_keys = []
	way_keys = []
	players_keys = []
	c = 0
	for line in f:
		for i in range (colums):
			if line[i] == '&':
				players_keys.append(c)
			if line[i] == '_':
				way_keys.append(c)
			if line[i] == '$':
				money_keys.append(c)
			if line[i] == '0':
				wall_keys.append(c)
			if line[i] == '*':
				trap_keys.append(c)
			c +=1
	information = [players_keys, way_keys, money_keys, wall_keys, trap_keys, lines, colums]
	return information
	f.close()
	
field_information = field_from_file()
players_keys = field_information[0]
way_keys = field_information[1]
money_keys = field_information[2]
wall_keys = field_information[3]
trap_keys = field_information[4]
lines = field_information[5]
colums = field_information[6]
blockSize = 60
screen_indent = 350
screen_width = screen_indent+blockSize*colums+screen_indent
screen_height = screen_indent+blockSize*lines+screen_indent

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

score_for_winning = len(money_keys)

dog_img = pygame.image.load('dog.png')
cat_img = pygame.image.load('cat.png')
mouse_img = pygame.image.load('mouse.png')
wall_img = pygame.image.load('wall.png')
money_img = pygame.image.load('money.png')
trap_img = pygame.image.load('trap.png')
way_img = pygame.image.load('way.png')
dead_img = pygame.image.load('empty.png')


class Players(ABC):
	def __init__(self, x, y, width, lives, scores, image):
		self.x = x
		self.y = y
		self.width = blockSize
		self.lives = lives
		self.scores = scores
		self.image = image
		self.alive = True
	@abstractmethod
	def draw(self):
		pass
	@abstractmethod
	def move(self):
		pass
	def pick_money(self, money):
		if self.alive == True:
			for one_money in money:
				if self.x == one_money.x and self.y == one_money.y:
					self.scores +=1
					one_money.x = -200
					one_money.y = -200
					one_money.draw()
	def eating(self, player):
		if self.alive == True and player.alive == True :
			if (player.y < self.y < player.y + blockSize) or (player.y < self.y +  blockSize < player.y + blockSize) or (self.y == player.y):
					if (player.x < self.x < player.x + blockSize) or (player.x < self.x + blockSize < player.x + blockSize) or (self.x == player.x):
						self.lives -=1
						self.x = self.x_start
						self.y = self.y_start
						return True
		return False
	def game_finished(self, image):
		if self.lives == 0:
			self.image = image
			self.alive = False
			return True
		
class Dog(Players):
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
		print_text("Жизни собачки: " + str(self.lives), 100, 100)
		print_text("Очки собачки: " + str(self.scores), 600, 100)
	def move(self, x_change, y_change):
		self.x += x_change
		self.y += y_change
	def crash(self, x_change, y_change):
		if self.alive == True:
			if self.x == screen_indent+blockSize*colums or self.x < screen_indent or self.y == screen_indent+blockSize*lines or self.y < screen_indent:
				self.lives -=1
				self.x -= x_change
				self.y -= y_change
				return True
			else:
				return False
	def check_collision(self, barriers, x_change, y_change):
		if self.alive == True:
			for barrier in barriers:
				if self.x == barrier.x and self.y == barrier.y:
					self.lives -=1
					self.x -= x_change
					self.y -= y_change
					return True
		return False
		
class Cat(Players):
	def __init__(self, x, y, width, lives, scores, image):
		self.x_start = x
		self.y_start = y		
		self.x = x
		self.y = y
		self.width = blockSize
		self.lives = lives
		self.scores = scores
		self.image = image
		self.alive = True
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
		print_text("Жизни кошки: " + str(self.lives), 100, 140)
		print_text("Очки кошки: " + str(self.scores), 600, 140)
	def move(self, motion):
		if motion == "stop":
			self.x = self.x
			self.y = self.y
		if motion == "up":
			self.x += 0
			self.y -= 4
		if motion == "down":
			self.x += 0
			self.y += 4
		if motion == "left":
			self.x -= 4
			self.y += 0
		if motion == "right":
			self.x += 4
			self.y += 0
	def crash(self, barriers):
		if self.alive == True:
			if self.x+blockSize > screen_indent+blockSize*colums:
				self.x = screen_indent+blockSize*(colums-1)
				cat_motion = 'stop'
			elif self.x < screen_indent:
				self.x = screen_indent
				cat_motion = 'stop'
			if self.y+blockSize > screen_indent+blockSize*lines:
				self.y = screen_indent+blockSize*(lines-1)
				cat_motion = 'stop'
			elif self.y < screen_indent:
				self.y = screen_indent
				cat_motion = 'stop'
			
			for barrier in barriers:
				if self.y == barrier.y + blockSize - 4:
					if  (barrier.x < self.x < barrier.x + blockSize) or (barrier.x < self.x + blockSize < barrier.x + blockSize) or (self.x == barrier.x):
						self.y = self.y + 4
						cat_motion = 'stop'
				if self.y + blockSize == barrier.y + 4:
					if  (barrier.x < self.x < barrier.x + blockSize) or (barrier.x < self.x + blockSize < barrier.x + blockSize) or (self.x == barrier.x):
						self.y = self.y - 4
						cat_motion = 'stop'
				if self.x == barrier.x + blockSize - 4:
					if (barrier.y < self.y < barrier.y + blockSize) or (barrier.y < self.y + blockSize < barrier.y + blockSize) or (self.y == barrier.y):
						self.x = self.x + 4
						cat_motion = 'stop'
				if self.x + blockSize == barrier.x + 4:
					if (barrier.y < self.y < barrier.y + blockSize) or (barrier.y < self.y + blockSize < barrier.y + blockSize) or (self.y == barrier.y):
						self.x = self.x - 4
						cat_motion = 'stop'			
				
	def check_collision(self, barriers):
		if self.alive == True:
			for barrier in barriers:
				if (barrier.y < self.y < barrier.y + blockSize) or (barrier.y < self.y +  blockSize < barrier.y + blockSize) or (self.y == barrier.y):
					if (barrier.x < self.x < barrier.x + blockSize) or (barrier.x < self.x + blockSize < barrier.x + blockSize) or (self.x == barrier.x) :
						self.lives -=1
						self.x = self.x_start
						self.y = self.y_start
						return True
		return False
					
class Mouse(Players):
	def __init__(self, x, y, width, lives, scores, image):
		self.x_start = x
		self.y_start = y		
		self.x = x
		self.y = y
		self.width = blockSize
		self.lives = lives
		self.scores = scores
		self.image = image
		self.alive = True
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
		print_text("Жизни мышки: " + str(self.lives), 100, 180)
		print_text("Очки мышки: " + str(self.scores), 600, 180)
	def move(self, motion):
		if motion == "stop":
			self.x = self.x
			self.y = self.y
		if motion == "up":
			self.x += 0
			self.y -= 4
		if motion == "down":
			self.x += 0
			self.y += 4
		if motion == "left":
			self.x -= 4
			self.y += 0
		if motion == "right":
			self.x += 4
			self.y += 0
	def crash(self, barriers):
		if self.alive == True:
			if self.x+blockSize > screen_indent+blockSize*colums:
				self.x = screen_indent+blockSize*(colums-1)
				mouse_motion = 'stop'
			elif self.x < screen_indent:
				self.x = screen_indent
				mouse_motion = 'stop'
			if self.y+blockSize > screen_indent+blockSize*lines:
				self.y = screen_indent+blockSize*(lines-1)
				mouse_motion = 'stop'
			elif self.y < screen_indent:
				self.y = screen_indent
				mouse_motion = 'stop'
			
			for barrier in barriers:
				if self.y == barrier.y + blockSize - 4:
					if  (barrier.x < self.x < barrier.x + blockSize) or (barrier.x < self.x + blockSize < barrier.x + blockSize) or (self.x == barrier.x):
						self.y = self.y + 4
						mouse_motion = 'stop'
				if self.y + blockSize == barrier.y + 4:
					if  (barrier.x < self.x < barrier.x + blockSize) or (barrier.x < self.x + blockSize < barrier.x + blockSize) or (self.x == barrier.x):
						self.y = self.y - 4
						mouse_motion = 'stop'
				if self.x == barrier.x + blockSize - 4:
					if (barrier.y < self.y < barrier.y + blockSize) or (barrier.y < self.y + blockSize < barrier.y + blockSize) or (self.y == barrier.y):
						self.x = self.x + 4
						mouse_motion = 'stop'
				if self.x + blockSize == barrier.x + 4:
					if (barrier.y < self.y < barrier.y + blockSize) or (barrier.y < self.y + blockSize < barrier.y + blockSize) or (self.y == barrier.y):
						self.x = self.x - 4
						mouse_motion = 'stop'
class Wall:
	def __init__(self, x, y, width, image):
		self.x = x
		self.y = y
		self.width = blockSize
		self.image = image
	def draw(self):
		screen.blit(self.image, (self.x, self.y))

class Money:
	def __init__(self, x, y, width, image):
		self.x = x
		self.y = y
		self.width = blockSize
		self.image = image
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
	
class Trap:
	def __init__(self, x, y, width, image):
		self.x = x
		self.y = y
		self.width = blockSize
		self.image = image
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
class Way:
	def __init__(self, x, y, width, image):
		self.x = x
		self.y = y
		self.width = blockSize
		self.image = image
	def draw(self):
		screen.blit(self.image, (self.x, self.y))

def create_wall_arr(array):
	for k in wall_keys:
		array.append(Wall(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, wall_img))

def create_trap_arr(array):
	for k in trap_keys:
		array.append(Trap(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, trap_img))

def create_money_arr(array):
	for k in money_keys:
		array.append(Money(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, money_img))
		
def create_way_arr(array):
	for k in way_keys:
		array.append(Way(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, way_img))

def create_player_arr(array):
	for k in players_keys:
		if players_keys.index(k) == 0:
			array.append(Dog(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, 4, 0, dog_img))
		elif players_keys.index(k) == 1:
			array.append(Cat(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, 3, 0, cat_img))
		else:
			array.append(Mouse(screen_indent+blockSize*(k-(k//colums*colums)), screen_indent+blockSize*(k//colums), blockSize, 2, 0, mouse_img))

def draw_walls(array):
	for wall in array:
		wall.draw()
def draw_money(array):
	for money in array:
		money.draw()
def draw_trap(array):
	for trap in array:
		trap.draw()
def draw_way(array):
	for way in array:
		way.draw()
def draw_player(array):
	for player in array:
		player.draw()	

def who_winner(dog_player, cat_player, mouse_player):
	winner = ""
	if dog_player.scores + cat_player.scores + mouse_player.scores == score_for_winning:
		max_score = max(dog_player.scores, cat_player.scores, mouse_player.scores)
		if dog_player.scores == max_score:
			winner = "собачкой"
		if cat_player.scores == max_score:
			if winner == "":
				winner = "кошкой"
			else:
				winner = winner + ", кошкой"
		if mouse_player.scores == max_score:
			if winner == "":
				winner = "мышкой"
			else:
				winner = winner + ", мышкой"	
		return winner
	return False
def game_winning(text, dog_player, cat_player, mouse_player):
	paused = True
	while paused:
		screen.fill(black)
		print_text("Все монетки собраны", 30, screen_width//2-25)
		print_text("Победа одержена " + text, 30, screen_width//2)
		print_text("Очки собачки: " + str(dog_player.scores), 30, screen_width//2+25)
		print_text("Очки кошки: " + str(cat_player.scores), 30, screen_width//2+50)
		print_text("Очки мышки: " + str(mouse_player.scores), 30, screen_width//2+75)
		print_text("Нажмите Enter, чтобы закончить", 30, screen_width//2+125)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: 
					paused = False
		pygame.display.update()
		clock.tick(15)	
	
def pause(text):
	paused = True
	while paused:
		screen.fill(black)
		print_text(text, 30, screen_width//2-25)
		print_text("Нажмите Enter, чтобы продолжить игру", 30, screen_width//2+25)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: 
					paused = False	
		pygame.display.update()
		clock.tick(15)
		
def game_finish(dog_player, cat_player, mouse_player):
	paused = True
	while paused:
		screen.fill(black)
		print_text("Жизни всех персонажей закончились", 30, screen_width//2-25)
		print_text("Очки собачки: " + str(dog_player.scores), 30, screen_width//2)
		print_text("Очки кошки: " + str(cat_player.scores), 30, screen_width//2+25)
		print_text("Очки мышки: " + str(mouse_player.scores), 30, screen_width//2+50)
		print_text("Нажмите Enter, чтобы закончить", 30, screen_width//2+100)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: 
					paused = False	
		pygame.display.update()
		clock.tick(15)

def game_start():
	paused = True
	while paused:
		screen.fill(black)
		print_text("Добро пожаловать в игру!", 100, screen_width//2-75)
		print_text("Управление:", 100, screen_width//2-25)
		print_text("Собачка ходит стрелками на один блок при нажатии", 100, screen_width//2)
		print_text("Кошка ходит a-w-s-d плавно, пока клавиша нажата", 100, screen_width//2+25)
		print_text("Мышка ходит i-j-k-l плавно даже после отпускания клавиши", 100, screen_width//2+50)
		print_text("Собачка съедает кошку, кошка съедает мышку", 100, screen_width//2+75)
		print_text("Если герой съеден, он возвращается на клетку начала", 100, screen_width//2+125)
		print_text("Цель – собрать монетки", 100, screen_width//2+175)
		print_text("Нажмите Enter для начала игры", 100, screen_width//2+225)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: 
					paused = False	
		pygame.display.update()
		clock.tick(15)
		
def print_text(message, x, y, font_color = red, font_type='TLHeader-Regular-RUS.otf', font_size=25):
	font_type = pygame.font.Font(font_type, font_size)
	text = font_type.render(message, True, font_color)
	screen.blit(text,(x,y))
			
def run_game():
	global score, lines, score_for_winning
	game_over = False
	wall_arr = []
	way_arr = []
	trap_arr = []
	money_arr = []
	players_arr = []
	x1_change = 0
	y1_change = 0
	mouse_motion = "stop"
	cat_motion = "stop"
	
	create_wall_arr(wall_arr)
	create_way_arr(way_arr)
	create_money_arr(money_arr)
	create_trap_arr(trap_arr)
	create_player_arr(players_arr)
	
	dog_player = players_arr[0]
	cat_player = players_arr[1]
	mouse_player = players_arr[2]
	
	game_start()
	
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w: 
					cat_motion = "up"
				if event.key == pygame.K_s: 
					cat_motion = "down"
				if event.key == pygame.K_a: 
					cat_motion = "left"
				if event.key == pygame.K_d: 
					cat_motion = "right"
					
				if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
					if event.key == pygame.K_UP: 
						y1_change = -blockSize
						x1_change = 0
					if event.key == pygame.K_DOWN: 
						y1_change = blockSize
						x1_change = 0
					if event.key == pygame.K_LEFT: 
						y1_change = 0
						x1_change = -blockSize
					if event.key == pygame.K_RIGHT: 
						y1_change = 0
						x1_change = blockSize
					dog_player.move(x1_change, y1_change)
					
				if event.key == pygame.K_i: 
					mouse_motion = "up"
				if event.key == pygame.K_k: 
					mouse_motion = "down"
				if event.key == pygame.K_j: 
					mouse_motion = "left"
				if event.key == pygame.K_l: 
					mouse_motion = "right"
					
			if event.type == pygame.KEYUP:
				if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
					cat_motion = "stop"
		cat_player.move(cat_motion)
		cat_player.crash(wall_arr)
		mouse_player.move(mouse_motion)
		mouse_player.crash(wall_arr+trap_arr)
		
		if dog_player.crash(x1_change, y1_change) or dog_player.check_collision(wall_arr+trap_arr, x1_change, y1_change):
			if dog_player.game_finished(dead_img):
				pause("У собачки закончились жизни")
			else:
				pause("Собачка ударилась о границы поля, стену или попала в ловушку")

		if cat_player.check_collision(trap_arr):
			if cat_player.game_finished(dead_img):
				pause("У кошки закончились жизни")
			else:
				cat_motion = 'stop'
				pause("Кошка попала в ловушку")
					
		if cat_player.eating(dog_player):
			if cat_player.game_finished(dead_img):
				pause("У кошки закончились жизни")
			else:
				cat_motion = 'stop'
				pause("Кошка была съедена")
				
		if mouse_player.eating(cat_player):
			if mouse_player.game_finished(dead_img):
				pause("У мышки закончились жизни")
			else:
				mouse_motion = 'stop'
				pause("Мышка была съедена")
					
		dog_player.pick_money(money_arr)
		cat_player.pick_money(money_arr)
		mouse_player.pick_money(money_arr)
		
		winner = who_winner(dog_player, cat_player, mouse_player)
		if winner != False:
			game_winning(winner, dog_player, cat_player, mouse_player)
			game_over = True	
		
		if dog_player.lives == 0 and cat_player.lives == 0 and mouse_player.lives == 0:
			game_finish(dog_player, cat_player, mouse_player)
			game_over = True
		
		screen.fill(white)
		draw_walls(wall_arr)
		draw_way(way_arr)
		draw_money(money_arr)
		draw_trap(trap_arr)
		draw_player(players_arr[::-1])
			
		pygame.display.update()
		clock.tick(20)


run_game()

pygame.quit()
