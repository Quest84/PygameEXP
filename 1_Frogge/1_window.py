import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # inicializa pygame
WINDOW_SIZE = (400, 400)

screen = pygame.display.set_mode(WINDOW_SIZE)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			#print('i dont wanna close')
			pygame.quit()
			sys.exit()

	pygame.display.update()
	clock.tick(60)