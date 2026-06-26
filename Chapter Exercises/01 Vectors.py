import math, random, pygame, noise


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

    @staticmethod
    def vectorAddition(u, v):
        wx = u.x + v.x
        wy = u.y + v.y
        if u.z and v.z:
            wz = u.z + v.z
            w = Vector(wx, wy, wz)
        else:
            w = Vector(wx, wy)
        return w

    @staticmethod
    def vectorSubtraction(u, v):
        if isinstance(u, tuple):
            u = Vector(u[0],u[1])
        if isinstance(v, tuple):
            v = Vector(v[0],v[1])
        wx = u.x - v.x
        wy = u.y - v.y
        if u.z and v.z:
            wz = u.z - v.z
            w = Vector(wx, wy, wz)
        else:
            w = Vector(wx, wy)
        return w

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
        if self.z and self.z > max:
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

class vectorAccelerator:
    def __init__(self, window, position = (0,0), velocity = (1,1), color = (0,0,0),
                 topSpeed = 10):
        self.window = window
        self.position = Vector(position[0],position[1])
        self.velocity = Vector(velocity[0],velocity[1])
        self.color = color
        self.topSpeed = topSpeed
        self.acceleration = Vector(0,0)

    def move(self):
        self.acceleration = Vector(random.uniform(-1,1)*0.1, random.uniform(-1,1)*0.1)
        self.velocity.addVector(self.acceleration)
        self.velocity.limit(self.topSpeed)
        self.position.addVector(self.velocity)
        # Wrap to other side of screen
        if self.position.x > self.window.get_width():
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = self.window.get_width()
        if self.position.y > self.window.get_height():
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = self.window.get_height()

    def show(self):
        self.window.set_at((self.position.x, self.position.y), self.color)

class perlinAccelerator:
    def __init__(self, window, position = (0,0), velocity = (1,1), color = (0,0,0),
                 topSpeed = 10, noise = 0.01):
        self.window = window
        self.position = Vector(position[0],position[1])
        self.velocity = Vector(velocity[0],velocity[1])
        self.color = color
        self.topSpeed = topSpeed
        self.acceleration = Vector(0,0)
        self.noise = noise
        self.tx = 2
        self.ty = 1

    @staticmethod
    def range_map(value, base_range = (0,1), target_range = (0,10)):

        new = (target_range[0] +
               ((value - base_range[0]) * (target_range[1]-target_range[0])) /
               (base_range[1]-base_range[0]))

        return new

    def move(self):
        accVec = Vector(self.range_map(noise.pnoise1(self.tx), target_range=(-.1,.1)),
                        self.range_map(noise.pnoise1(self.ty), target_range=(-.1,.1)))

        self.acceleration.addVector(accVec)
        self.tx += self.noise
        self.ty += self.noise
        self.velocity.addVector(self.acceleration)
        self.velocity.limit(self.topSpeed)
        self.position.addVector(self.velocity)
        # Wrap to other side of screen
        if self.position.x > self.window.get_width():
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = self.window.get_width()
        if self.position.y > self.window.get_height():
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = self.window.get_height()

    def show(self):
        self.window.set_at((self.position.x, self.position.y), self.color)

class mouseAccelerator:
    def __init__(self, window, position = (0,0), velocity = (0,0), color = (0,0,0),
                 topSpeed = 10):
        self.window = window
        self.position = Vector(position[0],position[1])
        self.velocity = Vector(velocity[0],velocity[1])
        self.acceleration = Vector(0,0)
        self.color = color
        self.topSpeed = topSpeed

    def move(self):
        direction = Vector.vectorSubtraction(pygame.mouse.get_pos(), self.position)
        direction.normalize()
        direction.multScalar(0.5)
        self.acceleration = direction
        self.velocity.addVector(self.acceleration)
        self.velocity.limit(self.topSpeed)
        self.position.addVector(self.velocity)

    def show(self):
        self.window.set_at((self.position.x, self.position.y), self.color)

def draw(walkers):
    for walker in walkers:
        walker.move()
        walker.show()

if __name__ == "__main__":
    # Initialize PyGame
    pygame.init()
    WIDTH = 1000
    HEIGHT = 700

    # Set up the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill((255, 255, 255))
    pygame.display.set_caption("Vector Walker Simulation")

    # Game loop
    #vw1 = vectorWalker(window, (500, 350), (3,3), (0.001, 0.005), color = (0,0,200))
    vw2 = vectorAccelerator(window, (WIDTH/2, HEIGHT/2), (0.1, 0.1), color=(0, 0, 200),
                            topSpeed=3)
    vw3 = perlinAccelerator(window, (WIDTH / 2, HEIGHT / 2), (.1, .1),
                            color=(200, 0, 200),
                            noise = 0.03, topSpeed=1)
    vw4 = mouseAccelerator(window, (WIDTH/3, HEIGHT/3), color = (0,200,0), topSpeed=5)

    walkers = [vw2, vw3, vw4]
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(walkers)
        # vw1.speed_up()
        pygame.display.flip()
        clock.tick(100)

# Quit Pygame
pygame.quit()