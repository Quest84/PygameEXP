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

player_image = pygame.image.load('images/frog_r.png')#.convert()
player_image_mirror = pygame.image.load('images/frog_l.png')

player_image_jump = pygame.image.load('images/frog_jump_r.png')

player_image_jump_mirror = pygame.image.load('images/frog_jump_l.png')

#Objetos de fondo para el efect Parallax
background_object = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,50,30,300]]]



# ColorKey es el color clave para definir la transparencia del sprite
#player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load('images/grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('images/dirt.png')

moving_right = False
moving_left = False
right = False
left = False
air_timer = 0
player_y_momentum = 0

true_scroll = [0,0]


def load_map(path):
	f = open(path + '.txt','r')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map

game_map = load_map('maps/map')

# Fisicas, colisiones con los tiles
def collision_test(rect, tiles):
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move(rect, movement, tiles):
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
	rect.x += movement[0]
	hit_list = collision_test(rect, tiles)
	#Actualizar la 
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right']=True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left']=True
	rect.y += movement[1]
	hit_list = collision_test(rect, tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom']=True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top']=True
	return rect, collision_types

player_rect = pygame.Rect(30,30, player_image.get_width(), player_image.get_height())

test_rect = pygame.Rect(100, 100, 100, 50)

last_move = [0,0]

GAME_ON = True
while GAME_ON:  # Loop del Juego
	display.fill((146, 244, 255))

	true_scroll[0] += (player_rect.x-true_scroll[0]-140)/20
	true_scroll[1] += (player_rect.y-true_scroll[1]-110)/20
	scroll = true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])
	
	pygame.draw.rect(display,(7,80,75), pygame.Rect(0,120,300,80))
	for background_objects in background_object:
		obj_rect = pygame.Rect(background_objects[0],background_objects[1][0]-scroll[0]*background_objects[0],background_objects[1][1]-scroll[1]*background_objects[0],background_objects[1][2])


	# Bucle para generar los tiles en la pantalla
	tile_rects = []
	y = 0
	for layer in game_map:
		x = 0
		for tile in layer:
			if tile == '1':
				display.blit(dirt_image, (x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile == '2':
				display.blit(grass_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
			if tile != '0':
				tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
			x += 1
		y += 1

	

	player_movement = [0, 0]
	if moving_right:
		player_movement[0] += 2
		last_move[0] = player_movement[0]
		right = True
		
	if moving_left:
		player_movement[0] -= 2
		last_move[0] = player_movement[0]
		left = True	
			
	player_movement[1] += player_y_momentum
	player_y_momentum += 0.2
	last_move[1] = player_y_momentum
	if player_y_momentum > 3:
		player_y_momentum = 3

	player_rect, collisions = move(player_rect, player_movement, tile_rects)

	
	if collisions['bottom']:
		player_y_momentum = 0
		air_timer = 0
	else:
		air_timer += 1

	if collisions['top']:
		player_y_momentum = 0

	print(air_timer)
 

		
	if last_move[0] >= 0 and air_timer > 5:
		display.blit(player_image_jump, (player_rect.x-scroll[0], player_rect.y-scroll[1]))	
	elif last_move[0] >= 0:
		display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))
	if last_move[0] < 0 and air_timer > 5:
		display.blit(player_image_jump_mirror, (player_rect.x-scroll[0], player_rect.y-scroll[1]))
	elif last_move[0] < 0:
		 display.blit(player_image_mirror, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

	for event in pygame.event.get():  # Evento Loop
		if event.type == QUIT:  # Revisa si se cerró la pantalla
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
				# Solo permite saltar cuando el tiempo en el aire sea menor que 20
				if air_timer < 8:				
					player_y_momentum = -5
					print('up')

		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
					
	surf = pygame.transform.scale(display,WINDOW_SIZE)
	screen.blit(surf,(0,0))
	pygame.display.update()
	clock.tick(60)
