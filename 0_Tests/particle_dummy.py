import pygame, sys, random
class ParticlePrincicple:
	def init(self):
		self.particles=[]
	def emit(self,color):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(screen, pygame.Color(color), particle[0], int(particle[1]))
	def add_particles(self):
		pos_x = pygame.mouse.get_pos()[0]/1.15
		pos_y = pygame.mouse.get_pos()[1]/1.15
		radius = 12
		direction_x = random.randint(0, 3)
		direction_y = random.randint(-3, 0)
		particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
		self.particles.append(particle_circle)
	def delete_particles(self):
		particles_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particle = particles_copy

pygame.init()
clock = pygame.time.Clock()

screen_width=(500)
screen_height=(500)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Name")

particle1 = ParticlePrincicple()
particle2 = ParticlePrincicple()
particle3 = ParticlePrincicple()
particle1.init()
particle2.init()
particle3.init()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 5)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == PARTICLE_EVENT:
			particle1.add_particles()
			particle2.add_particles()
			particle3.add_particles()
			
	screen.fill((30,30,30))
	particle1.emit("White")
	particle2.emit("Red")
	particle3.emit("Black")
	pygame.display.flip()
	clock.tick(60)
	print(clock.tick())