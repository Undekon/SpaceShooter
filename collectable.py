#health, ammo, boost, bigger dmg

import pygame
import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH

class Coin:
    spawn_ratio = 0.5

    def __init__(self, x, y):
        self.image = pygame.image.load("assets/coin.png")
        self.x_cord = x
        self.y_cord = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.image, (self.x_cord, self.y_cord))


class Boosters:
    spawn_ratio = 0.3

    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.x_cord = 0
        self.y_cord = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.direction = 0
        self.speed = 3

        self.spawn()

    def spawn(self):
        side = random.choice(["left", 'right'])
        self.y_cord = random.randint(0, WINDOW_HEIGHT)
        if side == "left":
            self.direction = 1
            self.x_cord = 0
        if side == "right":
            self.direction = -1
            self.x_cord = WINDOW_WIDTH
        print(f"Spawned new booster at: X: {self.x_cord}, Y: {self.y_cord}")    

    def move(self):
        self.x_cord += self.speed * self.direction
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.image, (self.x_cord, self.y_cord))

class BoostUpgrade(Boosters):
    def __init__(self):
        super().__init__("assets/boost_collect.png")
        self.boost_value = 50

class HealthUpgrade(Boosters):
    def __init__(self):
        super().__init__("assets/health_collect.png")
        self.health_value = 50
