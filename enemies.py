import pygame
import random
import math
from settings import WINDOW_HEIGHT, WINDOW_WIDTH
import bullet

class Enemy:
    def __init__(self, image_path, speed, health, name, collision_dmg, points):
        self.image = pygame.image.load(image_path)
        self.x_cord = 0
        self.y_cord = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = speed
        self.direction = 0
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.name = name
        self.health = health
        self.collision_dmg = collision_dmg
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
        self.y_cord = random.randint(0, WINDOW_HEIGHT)
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

class Drone(Enemy):
    def __init__(self):
        super().__init__("assets/enemy_drone.png", 4, 2, "Drone", 10, 150)

class Rocket(Enemy):
    def __init__(self):
        super().__init__("assets/rocket.png", 3, 2, "Rocket", 10, 200)
        self.bullets = []
        self.shoot_cooldown = 60
        #set image direction
        if self.direction == -1:
            self.image = pygame.transform.rotate(self.image, 180)

        #sounds
        self.shoot_sound = pygame.mixer.Sound("sounds/shot.mp3")

    
    def shoot(self, player_x, player_y):
        if self.shoot_cooldown == 0:
            dx = player_x - self.x_cord
            dy = player_y - self.y_cord
            angle = math.degrees(math.atan2(-dy, dx))  

            rocket_laser = bullet.EnemyBullet(self.x_cord + self.width//2, self.y_cord + self.height//2, angle)
            self.bullets.append(rocket_laser)
            self.shoot_cooldown = 60 

            self.shoot_sound.play() 
    
    def update_bullets(self, surface):
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(surface)

            if (bullet.x_cord < 0 or bullet.x_cord > WINDOW_WIDTH or
                    bullet.y_cord < 0 or bullet.y_cord > WINDOW_HEIGHT):
                    self.bullets.remove(bullet)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        

