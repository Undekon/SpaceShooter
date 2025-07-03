import pygame
import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH

class Asteroid:
    def __init__(self, image_path, speed, health, name, dmg, points):
        self.image = pygame.image.load(image_path)
        self.x_cord = 0
        self.y_cord = 0
        self.speed = speed
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.health = health
        self.name = name
        self.collision_dmg = dmg
        self.points = points
        self.spawn()

    def is_dead(self):
        if self.health <= 0:
            return True

    def move(self):
        self.x_cord += self.speed * self.direction
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.image, (self.x_cord, self.y_cord))

    def spawn(self):
        side = random.choice(["left", 'right'])
        self.y_cord = random.randint(0 + self.height, WINDOW_HEIGHT - self.height)
        if side == "left":
            self.direction = 1
            self.x_cord = 0
        if side == "right":
            self.direction = -1
            self.x_cord = WINDOW_WIDTH
        print(f"Spawned new asteroid at: X: {self.x_cord}, Y: {self.y_cord}")
    
    def check_if_off_screen(self):
        if self.x_cord > WINDOW_WIDTH or self.x_cord < 0 or self.y_cord > WINDOW_HEIGHT or self.y_cord < 0:
            return True
        
class RegularAsteroid(Asteroid):
    def __init__(self):
        super().__init__("assets/regular_asteroid.png", 2, 1, "RegularAsteroid", 10, 100)

class MiniAsteroid(Asteroid):
    def __init__(self, x=None, y=None, x_direction=None, y_direction = None):
        super().__init__("assets/regular_asteroid.png", 3, 1, "MiniAsteroid", 5, 50)
        self.x_cord = x
        self.y_cord = y
        self.direction = x_direction
        self.y_direction = y_direction
        self.scale = 0.5
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
                
    def move(self):
        #Left -> right
        if self.direction > 0 and self.y_direction == 1:
            self.x_cord += self.speed
            self.y_cord -= self.speed
        if self.direction > 0 and self.y_direction == 0:
            self.x_cord += self.speed
            self.y_cord += self.speed 

        #Right -> left
        if self.direction < 0 and self.y_direction == 1:
            self.x_cord -= self.speed
            self.y_cord += self.speed
        if self.direction < 0 and self.y_direction == 0:
            self.x_cord -= self.speed
            self.y_cord -= self.speed 

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

class ExplosiveAsteroid(Asteroid):
    def __init__(self):
        super().__init__("assets/explosive_asteroid.png", 1.5, 3, "ExplosiveAsteroid", 10, 150)
    
    def divide(self):
        if self.is_dead():
            offset = 20
            child1 = MiniAsteroid(self.x_cord - offset, self.y_cord, self.direction, 1)
            child2 = MiniAsteroid(self.x_cord + offset, self.y_cord, self.direction, 0)
            return [child1, child2]
        