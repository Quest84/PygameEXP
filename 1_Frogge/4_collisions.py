import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # inicializa pygame

pygame.display.set_caption('Pygame Window') # Le da un nombre a la pantalla

WINDOW_SIZE = (600, 400) # Establece el tamaño de la pantalla

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)	# Inicializa la pantalla

player_image = pygame.image.load('images/magician.png')	

moving_right = False
moving_left = False
moving_up = False
moving_down = False

player_location = [50,50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True:	# Loop del Juego
	screen.fill((146, 244, 255))

	screen.blit(player_image, player_location)
	
	if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
		player_y_momentum = -player_y_momentum
	else:
		player_y_momentum += 0.2
	player_location[1] += player_y_momentum


	print(player_location)
	if moving_right == True:
		player_location[0] += 10
	if moving_left == True:
		player_location[0] -= 10
	if moving_up == True:
		player_location[1] -= 10
	if moving_down == True:
		player_location[1] += 10

	player_rect.x = player_location[0]
	player_rect.y = player_location[1]

	if player_rect.colliderect(test_rect):
		pygame.draw.rect(screen,(250,0,0), test_rect)
	else:
		pygame.draw.rect(screen,(0,0,0), test_rect)

	for event in pygame.event.get(): # Evento Loop
		if event.type == QUIT: # Revisa si se cerró la ptnalla
			#print('moving_i dont wanna close')
			pygame.quit() # Detiene pygame
			sys.exit() 	# Detiene el script
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
				print ('right')
			if event.key == K_LEFT:
				print ('left')
				moving_left = True
			if event.key == K_UP:
				moving_up = True
				print ('up')
			if event.key == K_DOWN:
				print ('down')
				moving_down = True

		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
			if event.key == K_UP:
				moving_up = False
			if event.key == K_DOWN:
				moving_down = False

	pygame.display.update() #Actualiza la pantalla
	clock.tick(60) # Mantiene 60 fps