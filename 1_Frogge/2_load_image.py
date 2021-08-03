import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # inicializa pygame

pygame.display.set_caption('Pygame Window') # Le da un nombre a la pantalla

WINDOW_SIZE = (400, 400) # Establece el tamaño de la pantalla

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)	# Inicializa la pantalla

player_image = pygame.image.load('data/images/magician.png')	

while True:	# Loop del Juego
	screen.blit(player_image, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))	

	for event in pygame.event.get(): # Evento Loop
		if event.type == QUIT: # Revisa si se cerró la ptnalla
			#print('i dont wanna close')
			pygame.quit() # Detiene pygame
			sys.exit() 	# Detiene el script

	pygame.display.update() #Actualiza la pantalla
	clock.tick(60) # Mantiene 60 fps