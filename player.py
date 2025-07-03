import pygame
import math
import bullet
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Player:
    def __init__(self):
        self.original_image = pygame.image.load("assets/player.png")  
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.speed = 4
        self.angle = 0
        self.boost = 100
        self.bullets = []
        self.health = 100
        self.hitbox = pygame.Rect(0, 0, self.original_image.get_width()-10, self.original_image.get_height()-10)
        self.hitbox.center = self.rect.center
        
        # sounds
        self.shoot_sound = pygame.mixer.Sound("sounds/shot.mp3")
    
    def shoot(self):
        self.bullets.append(bullet.PlayerBullet(self.rect.centerx, self.rect.centery, self.angle))
        self.shoot_sound.play()
        
    def move(self, keys):
        # boost
        if keys[pygame.K_LSHIFT] and self.boost > 0:
            speed = self.speed * 2.5
            self.boost -= 1
        else:
            speed = self.speed
            if self.boost < 100:
                self.boost += 0.1

        # movement
        if keys[pygame.K_a]:
            self.angle += 4  
        if keys[pygame.K_d]:
            self.angle -= 4  

        if keys[pygame.K_w]:
            radians = math.radians(-self.angle)
            dx = math.cos(radians) * speed
            dy = math.sin(radians) * speed
            self.rect.x += dx
            self.rect.y += dy

        self.hitbox.center = self.rect.center

    def update_health(self, dmg):
        self.health -= dmg
        print(f"Player health: {self.health}")

    def draw_boost_bar(self, surface):
        bar_width = 100
        bar_height = 10
        boost_ratio = self.boost / 100 
        # bar background
        pygame.draw.rect(surface, (50, 50, 50), (self.rect.centerx - bar_width//2, self.rect.centery + 70, bar_width, bar_height))
        # boost bar color
        pygame.draw.rect(surface, (0, 150, 255), (self.rect.centerx - bar_width//2, self.rect.centery + 70, bar_width * boost_ratio, bar_height))
    
    def draw_health_bar(self, surface):
        bar_width = 100
        bar_height = 10
        # bar background
        pygame.draw.rect(surface, (50, 50, 50), (self.rect.centerx - bar_width//2, self.rect.centery + 50, bar_width, bar_height))
        # health bar color
        pygame.draw.rect(surface, (34, 177, 76), (self.rect.centerx - bar_width//2, self.rect.centery + 50, self.health, bar_height))

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.image = rotated_image  
        self.rect = rotated_image.get_rect(center=self.rect.center)  
        surface.blit(rotated_image, self.rect.topleft)

        #draw hitbox
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def check_remove_bullets(self):
        for bullet in self.bullets:
            if bullet.x_cord > WINDOW_WIDTH or bullet.x_cord < 0 or bullet.y_cord > WINDOW_HEIGHT or bullet.y_cord < 0:
                self.bullets.remove(bullet)