from pygame.locals import *
import pygame
import sys

clock = pygame.time.Clock()

pygame.init()  # inicializa pygame

pygame.display.set_caption('Pygame Window')  # Le da un nombre a la pantalla

WINDOW_SIZE = (600, 400)  # Establece el tamaño de la pantalla

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # Inicializa la pantalla

display = pygame.Surface((300, 200))
# Se puede proyectar una imagen en una superficie y escalar
# esa superficie independientemente del resto de elemtnos

player_image = pygame.image.load('images/frog_r.png')
# ColorKey es el color clave para definir la transparencia del sprite
player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load('images/grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('images/dirt.png')



game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2'],
			['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1'],
			['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
			['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
			['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
			['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
			['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

moving_right = False
moving_left = False
moving_up = False
moving_down = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(
	player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while True:  # Loop del Juego
	display.fill((146, 244, 255))

	# Bucle para generar los tiles en la pantalla
	tile_rects = []
	y = 0
	for row in game_map:
		x = 0
		for tile in row:
			if tile == '1':
				display.blit(dirt_image, (x*16,y*16))
			if tile == '2':
				display.blit(grass_image, (x*16, y*16))
			if tile != '0':
				tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
			x += 1
		y += 1

	display.blit(player_image, player_location)

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

	for event in pygame.event.get():  # Evento Loop
		if event.type == QUIT:  # Revisa si se cerró la ptnalla
			# print('moving_i dont wanna close')
			pygame.quit()  # Detiene pygame
			sys.exit() 	# Detiene el script
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
				print('right')
			if event.key == K_LEFT:
				print('left')
				moving_left = True
			if event.key == K_UP:
				moving_up = True
				print('up')
			if event.key == K_DOWN:
				print('down')
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
	
	surf = pygame.transform.scale(display,WINDOW_SIZE)
	screen.blit(surf,(0,0))
	pygame.display.update()
	clock.tick(60)