#breakout

import pygame, sys
from math import *
from pygame.locals import *

RED = (255,0,0)
BLACK = (0,0,0)
SCREEN_LEFT = 0
SCREEN_RIGHT = 1000
SCREEN_TOP = 0
SCREEN_BOTTOM = 800

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_RIGHT,SCREEN_BOTTOM))
bg = pygame.image.load('C:\Python27\PyGame Learning\smoke_cloud.jpg')

class PaddleSprite(pygame.sprite.Sprite):
	width = 50
	height = 10

	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position,(self.width,self.height))
		self.position = position
		self.rect.center = self.position
		pygame.mouse.set_pos(self.position)

	def update(self,surface):
		(mx,my) = pygame.mouse.get_pos()
		(x,y) = self.position
		x = mx
		self.position = (x,y)
		self.rect.center = self.position
		pygame.draw.rect(surface,BLACK,self.rect)

class BlockSprite(pygame.sprite.Sprite):
	width = 50
	height = 10
	image = pygame.image.load('C:\Python27\Pygame Learning\\block.png')
	mask = pygame.mask.from_surface(image)

	def __init__(self,position,surface):
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.center = position
		"""
		self.rect = pygame.Rect(position,(self.width,self.height))
		self.position = position
		self.rect.center = self.position
		pygame.draw.rect(surface,BLACK,self.rect)
		"""

class BallSprite(pygame.sprite.Sprite):
	width = 15
	height = 15
	image = pygame.image.load('C:\Python27\PyGame Learning\obstacle.png')
	mask = pygame.mask.from_surface(image)

	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.position = position
		self.direction = 45
		self.speed = 7

	def update(self,surface,paddle_coll,brick_coll):
		x,y = self.position
		if (paddle_coll == True) or (y <= SCREEN_TOP):
			self.direction = -self.direction
			self.speed = -self.speed
		if (x >= SCREEN_RIGHT) or (x <= SCREEN_LEFT) or (brick_coll == True):
			self.direction = -self.direction
		x += self.speed*sin(self.direction*pi/180)
		y += self.speed*cos(self.direction*pi/180)
		self.position = (x,y)
		self.rect.center = self.position
		#pygame.draw.rect(surface,BLACK,self.rect)

def create_blocks():
	x = 60
	y = 25
	offset_x = 250
	offset_y = 50
	x_max = 1024
	y_max = 786
	blocks = []
	for j in range(0,4):
		for i in range(0,10):
			blocks.append(BlockSprite((x*i+offset_x,y*j+offset_y),screen))
	return blocks


paddle = PaddleSprite((512,650))
ball = BallSprite((512,500))
blocks = create_blocks()
blocks_group = pygame.sprite.Group(*blocks)
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		if event.key == K_ESCAPE:
			sys.exit()
	screen.blit(bg,(0,0))	#have to do this before updating/drawing stuff on the screen
	hit_list = pygame.sprite.spritecollide(ball,blocks_group,True)
	if hit_list:
		brick_coll = pygame.sprite.collide_rect(ball,hit_list[0])
	else:
		brick_coll = 0
	paddle_coll = pygame.sprite.collide_rect(paddle,ball)
	blocks_group.draw(screen)
	paddle.update(screen)
	ball.update(screen,paddle_coll,brick_coll)
	pygame.display.flip()	#this redraws/updates the screen
