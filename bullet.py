import pygame
import math
from settings import WINDOW_HEIGHT, WINDOW_WIDTH

class Bullet:
    def __init__(self, image_path, x, y, angle, speed, dmg):
        self.original_image = pygame.image.load(image_path)
        self.speed = speed
        self.angle = angle
        self.x_cord = x
        self.y_cord = y
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        self.dmg = dmg
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

        #Rotate image
        radians = math.radians(-angle)
        self.dx = math.cos(radians) * self.speed
        self.dy = math.sin(radians) * self.speed
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        self.rect = self.image.get_rect(center=(self.x_cord, self.y_cord))

    def move(self):
        self.x_cord += self.dx
        self.y_cord += self.dy
        self.rect.center = (self.x_cord, self.y_cord)

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class PlayerBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__("assets/laser.png", x, y, angle, 14, 1)

class EnemyBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__('assets/enemy_laser.png', x, y, angle, 5, 5)