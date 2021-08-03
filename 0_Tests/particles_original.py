import pygame, sys, random
class ParticlePrincicple:
    def init(self):
        self.particles=[]
    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(screen, pygame.Color("White"), particle[0], int(particle[1]))
    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 15
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
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

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
            
    screen.fill((30,30,30))
    particle1.emit()
    pygame.display.flip()
    clock.tick(60)