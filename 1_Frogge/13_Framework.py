from pygame.locals import *
import pygame, sys, random
import data.engine as e

# TO-DO
# Generar infinitamente el efecto parallax
clock = pygame.time.Clock()

pygame.init()  # inicializa pygame

#Inicializando el sonido
pygame.mixer.pre_init(44100, -16, 2, 512)
# Caales para reproducir más sonidos a la vez
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('Pygame Window')  # Le da un nombre a la pantalla

WINDOW_SIZE = (600, 400)  # Establece el tamaño de la pantalla

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # Inicializa la pantalla

display = pygame.Surface((300, 200))
# Se puede proyectar una imagen en una superficie y escalar
# esa superficie independientemente del resto de elemtnos


#Objetos de fondo para el efect Parallax
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,70,50,400]],[0.5,[130,50,80,300]]]

# ColorKey es el color clave para definir la transparencia del sprite
#player_image.set_colorkey((255,255,255))

game_map = {}
# Dictionary - se pueden tener tramos vacios
#{'1;1':chunk_data,'1;2':chunk_data}

e.load_animations('data/images/entities/')

grass_image = pygame.image.load('data/images/grass.png')
dirt_image = pygame.image.load('data/images/dirt.png')
plant_image = pygame.image.load('data/images/plant.png').convert()
plant_image.set_colorkey((255,255,255))
TILE_SIZE = grass_image.get_width()

tile_index =    {1:grass_image,
				 2:dirt_image,
				 3:plant_image}

jump_sound = pygame.mixer.Sound('data/sounds/jump.wav')
jump_sound.set_volume(0.3)
grass_sounds = [pygame.mixer.Sound('data/sounds/grass_0.wav'), pygame.mixer.Sound('data/sounds/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

damage_sound = pygame.mixer.Sound('data/sounds/present.wav')
damage_sound.set_volume(0.4)

pygame.mixer.music.load('data/sounds/Noise.wav')
pygame.mixer.music.play(-1) #how many times it plays after the first play; -1 to play in loop, 0 just once


moving_right = False
moving_left = False
air_timer = 0
player_y_momentum = 0

true_scroll = [0,0]

CHUNK_SIZE = 8
def generate_chunk(x,y):
	""" Hola, esto es un docstring """
	chunk_data = []
	for y_pos in range(CHUNK_SIZE):
		for x_pos in range(CHUNK_SIZE):
			target_x = x * CHUNK_SIZE + x_pos
			target_y = y * CHUNK_SIZE + y_pos
			tile_type = 0 #nothing/air
			#true position of the chunk
			if target_y > 10:
				tile_type = 2   #dirt
			elif target_y == 10:
				tile_type = 1   # grass
			elif target_y == 9:
				if random.randint(1,5) == 1:
					tile_type = 3 #plant
			if tile_type != 0:
				chunk_data.append([[target_x,target_y], tile_type])
	return chunk_data

GAME_ON = True
while GAME_ON:  # Loop del Juego
	display.fill((255, 255, 255))

	# play the grass sound only when
	if grass_sound_timer > 0:
		grass_sound_timer -= 1

	true_scroll[0] += (player.x-true_scroll[0]-140)/20
	true_scroll[1] += (player.y-true_scroll[1]-110)/20
	scroll = true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])
	
	pygame.draw.rect(display,(0,0,0), pygame.Rect(0,120,300,80))
	# Efecto Parallax
	for background_object in background_objects:
		obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0], 50, 400)
		if background_object[0] == 0.5:
			pygame.draw.rect(display,(255,80,255),obj_rect)
		else:
			pygame.draw.rect(display,(80,0,80),obj_rect)

	# Bucle para generar los tiles en la pantalla
	tile_rects = []
	# Tile rendering
	for y in range(3):
		for x in range(4):
			target_x = x -1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
			target_y = y -1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
			# ; es la clave para el diccionario, para separar los datos
			target_chunk = str(target_x) + ';' + str(target_y)
			if target_chunk not in game_map:
				game_map[target_chunk] = generate_chunk(target_x, target_y)
				# genera los chunks solo para los que aparecen en pantalla
			for tile in game_map[target_chunk]:
				display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
				if tile[1] in [1,2]:
					tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))
				
	player_movement = [0, 0]
	if moving_right:
		player_movement[0] += 2
		last_move[0] = player_movement[0]
				
	if moving_left:
		player_movement[0] -= 2
		last_move[0] = player_movement[0]
					
	player_movement[1] += player_y_momentum
	player_y_momentum += 0.2
	last_move[1] = player_y_momentum
	if player_y_momentum > 3:
		player_y_momentum = 3


	collisions = player.move(player_movement, tile_rects)

	if collisions_types['bottom'] == True:
		player_y_momentum = 0
		air_timer = 0
		position_fall = []
		position_fall = player_rect.x, player_rect.y

		if player_movement[0] != 0:
			if grass_sound_timer == 0:
				grass_sound_timer - 30
				random.choice(grass_sounds).play()
	else:
		air_timer += 1

	if collisions_types['top']:
		player_y_momentum = 0

	# Banderas para las animaciones, orientación y caida segura
	if player_movement[0] > 0:
		player.set_action('run')
		player.set_flip(False)
	if player_movement[0] == 0 and last_move[0] >= 0:
		player.set_action('idle')
		player.set_flip(False)
	if player_movement[0] == 0 and last_move[0] < 0:
		player.set_action('idle')
		player.set_flip(True)
	if player_movement[0] < 0:
		player.set_action('run')
		player.set_flip(True)
	if last_move[0] > 0 and air_timer > 5:
		player.set_action('jump')
		player.set_flip(False)
	if last_move[0] < 0 and air_timer > 5:
		player.set_action('jump')
		player.set_flip(True)
				
	if player.y >= 230:
		damage_sound.play()
		removeTiles(-20)
		

	if  player.y >= 250:
		player.x = position_fall[0]
		player.y = position_fall[1]-30
		air_timer = 0
		death_count += 1
		
	def removeTiles(n):
		while(n < 20):
			a = random.randint(5, 11)
			b = random.randint(1, 80)
			# print(a, b)
			game_map[a][b] = '0'
			n+=1

	# Loop para repetir el frame inicial
	player.change_frame(1)
	player.display(display,scroll)
	
	for event in pygame.event.get():  # Evento Loop
		if event.type == QUIT:  # Revisa si se cerró la pantalla
			pygame.quit()  # Detiene pygame
			sys.exit() 	# Detiene el script
		if event.type == KEYDOWN:
			if event.key == K_z:
				removeTiles(-20)
			if event.key == K_w:
				pygame.mixer.music.fadeout(1000)
			if event.key == K_e:
				pygame.mixer.music.play(-1)
			if event.key == K_RIGHT:
				moving_right = True
				#print('right')
			if event.key == K_LEFT:
				print('left')
				moving_left = True
			if event.key == K_UP:
				# Solo permite saltar cuando el tiempo en el aire sea menor que 20
				if air_timer < 20:				
					player_y_momentum = -5
					#The sounds must be initialize - check the first lines of code
					jump_sound.play()
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
		
		print(death_count)

		if death_count > 3:
			display.fill((0, 0, 0))
		if death_count > 8:
			pygame.quit()
			sys.exit()
			
	screen.blit(game.transform.scale(display,WINDOW_SIZE),(0,0))
	pygame.display.update()
	clock.tick(60)
