import pygame
import random
import numpy as np
import noise

width = 1000
height = 800
CENTER = [width/2, height/2]

class Walker:
    def __init__(self, window, coords = (0,0), color = (0,0,0)):
        self.window = window
        self.x = coords[0]
        self.y = coords[1]
        self.color = color

    def step(self):
        h_direction = random.randint(-2, 2)
        v_direction = random.randint(-2,2)

        # Bias the walk towards the center of the window
        if self.x > CENTER[0]:
            if h_direction < 1:
                self.x -= 1
            elif h_direction > 0:
                self.x += 1
        else:
            if h_direction < 0:
                self.x -= 1
            elif h_direction > -1:
                self.x += 1
        if self.y > CENTER[1]:
            if v_direction < 1:
                self.y -= 1
            elif v_direction > 0:
                self.y += 1
        else:
            if v_direction < 0:
                self.y -= 1
            elif v_direction > -1:
                self.y += 1


    def show(self):
        self.window.set_at((self.x, self.y), self.color)

class GaussianWalker(Walker):
    def __init__(self, window, coords = (0,0), color = (0,0,0),
                 mean = 0, sd = 1):
        super().__init__(window, coords, color)
        self.mean = mean
        self.sd = sd
        self.size = 1 # fixed number of steps

    def step(self):
        h_direction = round(np.random.normal(self.mean, self.sd, self.size)[0])
        v_direction = round(np.random.normal(self.mean, self.sd, self.size)[0])
        self.x += h_direction
        self.y += v_direction

class Jumper(Walker):
    def __init__(self, window, coords = (0,0), color = (0,0,0),
                 jump_prob = 0.1, jump_dist = 10):
        super().__init__(window, coords, color)
        self.jump_prob = jump_prob
        self.jump_dist = jump_dist
        self.jump_counter = 0

    def step(self):
        extra = 0
        if random.random() < self.jump_prob:
            extra = self.jump_dist

        h_direction = random.randint(-2, 2)
        v_direction = random.randint(-2,2)

        # Bias the walk towards the center of the window
        if self.x > CENTER[0]:
            if h_direction < 1:
                self.x -= 1 - extra
            elif h_direction > 0:
                self.x += 1 + extra
        else:
            if h_direction < 0:
                self.x -= 1 - extra
            elif h_direction > -1:
                self.x += 1 + extra
        if self.y > CENTER[1]:
            if v_direction < 1:
                self.y -= 1 - extra
            elif v_direction > 0:
                self.y += 1 + extra
        else:
            if v_direction < 0:
                self.y -= 1 - extra
            elif v_direction > -1:
                self.y += 1 + extra

class PerlinWalker(Walker):
    def __init__(self, window, coords = (0,0), color = (0,0,0),
                 range = (0,10), noise = 0.01):
        super().__init__(window, coords, color)
        self.range = range
        self.noise = noise
        self.tx = 0
        self.ty = 1

    def range_map(self, value, base_range = (0,1), target_range = (0,10)):

        new = (target_range[0] +
               ((value - base_range[0]) * (target_range[1]-target_range[0])) /
               (base_range[1]-base_range[0]))

        return new

    def step(self):

        if random.random() < 0.5:
            self.x += self.range_map(noise.pnoise1(self.tx))
        else:
            self.x -= self.range_map(noise.pnoise1(self.tx))

        if random.random() < 0.5:
            self.y += self.range_map(noise.pnoise1(self.ty))
        else:
            self.y -= self.range_map(noise.pnoise1(self.ty))

        self.tx += self.noise
        self.ty += self.noise

def draw(walkers):
    for walker in walkers:
        walker.step()
        walker.show()

if __name__ == "__main__":
    # Initialize PyGame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((1000, 700))
    window.fill((255, 255, 255))
    pygame.display.set_caption("Random Walker Simulation")

    # Game loop
    walker1 = Walker(window, [500, 500], (0,255,0))
    walker2 = Jumper(window, [100, 100], (0,0,255), 0.01, 5)
    walker3 = GaussianWalker(window, [200, 200], (255,0,0))
    walker4 = PerlinWalker(window, [700,300], range = [0,2], noise = 0.01)
    walkers = [walker1, walker2, walker3, walker4]
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(walkers)
        pygame.display.flip()
        clock.tick(100)

# Quit Pygame
pygame.quit()