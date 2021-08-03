from pygame.locals import *
import pygame, sys, random

class ParticlePrincicple():
	def init(self):
		self.particles=[]
	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(screen, pygame.Color("Red"), particle[0], int(particle[1]))
				
	def add_particles(self,increment):
		pos_x = (pygame.mouse.get_pos()[0])
		pos_y = (pygame.mouse.get_pos()[1])
		radius = increment
		direction_x = random.randint(0, 3)
		direction_y = random.randint(-3, 0)
		particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
		self.particles.append(particle_circle)
	def delete_particles(self):
		particles_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particle = particles_copy


pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((150, 100))


pygame.display.set_caption("Frogge")

particle1 = ParticlePrincicple()
particle1.init()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 10)
increment = 8
player_image = pygame.image.load('data/images/spin/spin.gif').convert()
player_image.set_colorkey((0,204,0))

player_location = [50,50]

while True:
	display.fill((30,30,30))
	player_location = [pygame.mouse.get_pos()[0]/4, pygame.mouse.get_pos()[1]/4]

	display.blit(player_image, player_location)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				increment += random.randint(1,5)
		if event.type == PARTICLE_EVENT:
			particle1.add_particles(increment)

		if event.type == KEYUP:
			if event.key == K_SPACE:
				increment = 8
				
			
	pygame.mouse.set_visible(False)

	surf = pygame.transform.scale(display,WINDOW_SIZE)
	screen.blit(surf,(0,0))
	particle1.emit()
	pygame.display.update()
	clock.tick(60)
