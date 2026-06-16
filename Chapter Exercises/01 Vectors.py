import math, random, pygame

class Vector:
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z

    def addVector(self, v):
        self.x += v.x
        self.y += v.y
        if self.z and v.z:
            self.z += v.z

    def addScalar(self, index, n):
        if index == 'x':
            self.x += n
        elif index == 'y':
            self.y += n
        elif index == 'z':
            self.z += n
        else:
            raise IndexError("Please provide 'x', 'y', or 'z' for 'index'")

    def subVector(self, v):
        self.x -= v.x
        self.y -= v.y
        if self.z and v.z:
            self.z -= v.z

    def subScalar(self, index, n):
        if index == 'x':
            self.x -= n
        elif index == 'y':
            self.y -= n
        elif index == 'z':
            self.z -= n
        else:
            raise IndexError("Please provide 'x', 'y', or 'z' for 'index'")

    def multScalar(self,n):
        self.x = self.x*n
        self.y = self.y*n
        if self.z:
            self.z = self.z*n

    def divScalar(self, n):
        self.x = self.x/n
        self.y = self.y/n
        if self.z:
            self.z = self.z/n

    def magnitude(self):
        sumsq = self.x*self.x + self.y*self.y
        if self.z:
            sumsq += self.z*self.z
        try:
            mag = math.sqrt(sumsq)
        except ImportError:
            raise NotImplementedError("This function requires the math package")
        else:
            return mag

    def normalize(self):
        mag = self.magnitude()
        self.x = self.x/mag
        self.y = self.y/mag
        if self.z:
            self.z = self.z/mag

    def limit(self, max):
        if self.x > max:
            self.x = max
        if self.y > max:
            self.y = max
        if self.z > max:
            self.z = max

class vectorWalker:
    def __init__(self, window, position = (0,0), velocity = (1,1), acceleration = (0,0),
                 color = (0,0,0)):
        self.window = window
        self.position = Vector(position[0],position[1])
        self.velocity = Vector(velocity[0],velocity[1])
        self.acceleration = Vector(acceleration[0],acceleration[1])
        self.color = color

    def move(self):
        direction = random.randint(0,7)
        if direction == 0:
            self.position.addScalar('x', self.velocity.x)
        elif direction == 1:
            self.position.addVector(self.velocity)
        elif direction == 2:
            self.position.addScalar('y', self.velocity.y)
        elif direction == 3:
            self.position.subScalar('x', self.velocity.x)
            self.position.addScalar('y', self.velocity.y)
        elif direction == 4:
            self.position.subScalar('x', self.velocity.x)
        elif direction == 5:
            self.position.subVector(self.velocity)
        elif direction == 6:
            self.position.subScalar('y',self.velocity.y)
        else:
            self.position.addScalar('x', self.velocity.x)
            self.position.subScalar('y', self.velocity.y)

    def speed_up(self):
        self.velocity.addVector(self.acceleration)

    def slow_down(self):
        self.velocity.subVector(self.acceleration)

    def show(self):
        self.window.set_at((self.position.x, self.position.y), self.color)

def draw(walkers):
    for walker in walkers:
        walker.move()
        walker.show()

if __name__ == "__main__":
    # Initialize PyGame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((1000, 700))
    window.fill((255, 255, 255))
    pygame.display.set_caption("Vector Walker Simulation")

    # Game loop
    vw1 = vectorWalker(window, (500, 350), (3,3), (0.001, 0.005), color = (0,0,200))

    walkers = [vw1]
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(walkers)
        vw1.speed_up()
        pygame.display.flip()
        clock.tick(100)

# Quit Pygame
pygame.quit()