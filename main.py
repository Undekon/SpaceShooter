import pygame
import sys
from player import Player
import asteroids
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FONT
import enemies
import collectable
import random

pygame.init()

#Window config
background = pygame.transform.scale(pygame.image.load("assets/background.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#global variables
asteroids_tab = []
enemies_tab = []
coins_tab = []
collectables_tab = []
coins_value = 0
points = 0
player = Player()
font = pygame.font.Font(FONT, 30)

#music and sounds main theme
pygame.mixer.music.load("sounds/main_theme.mp3")
pygame.mixer.music.play(5)
pygame.mixer.music.set_volume(0.5)

hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")

def check_bullet_collisions(bullet, targets_tab):
    global points
    for target in targets_tab:
        if bullet.hitbox.colliderect(target.hitbox):
            hit_sound.play()
            target.health -= bullet.dmg
            if target.is_dead():
                explosion_sound.play()
                points += target.points
                # print(f"Points: {points}")
                if isinstance(target, asteroids.ExplosiveAsteroid):
                    if target.health == 0:
                        new_asteroids = target.divide()
                        asteroids_tab.extend(new_asteroids)

                if isinstance(target, enemies.Enemy) and random.random() < collectable.Coin.spawn_ratio:
                    coins_tab.append(collectable.Coin(target.x_cord, target.y_cord))

                targets_tab.remove(target)
            return True
        
def check_player_collisions(player, asteroids_tab, enemies_tab):
    global coins_value
    #collisions with asteroids
    for asteroid in asteroids_tab:
        if player.hitbox.colliderect(asteroid.hitbox):
            player.update_health(asteroid.collision_dmg)
            asteroids_tab.remove(asteroid)
            hit_sound.play()
        
    for coin in coins_tab:
        if player.hitbox.colliderect(coin.hitbox):
            coins_value += 1
            # print(f"Coins: {coins_value}")
            coins_tab.remove(coin)

    #boosters
    for booster in collectables_tab:
        if isinstance(booster, collectable.BoostUpgrade):
            if player.hitbox.colliderect(booster.hitbox):
                if player.boost < 100:
                    player.boost = min(player.boost + booster.boost_value, 100)
                collectables_tab.remove(booster)

        if isinstance(booster, collectable.HealthUpgrade):
            if player.hitbox.colliderect(booster.hitbox):
                if player.health < 100:
                    player.health = min(player.health + booster.health_value, 100)
                collectables_tab.remove(booster)
        


    #collisions with enemies
    for enemy in enemies_tab:
        if isinstance(enemy, enemies.Rocket):
            for rocket_bullet in enemy.bullets:
                if player.hitbox.colliderect(rocket_bullet.hitbox):
                    player.update_health(rocket_bullet.dmg)
                    enemy.bullets.remove(rocket_bullet)
                    hit_sound.play()
        if player.hitbox.colliderect(enemy.hitbox):
            player.update_health(enemy.collision_dmg)
            enemies_tab.remove(enemy)
            hit_sound.play()

def main():
    clock = 0
    while True:
        score_text = font.render(f"Score     {points}", True, (255,255,255))
        coins_text = font.render(f"Coins     {coins_value}", True, (255,255,255))
        clock += pygame.time.Clock().tick(120)/1000

        #Game over test
        if player.health == 0:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #Shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        keys = pygame.key.get_pressed()
        
        window.blit(background, (0,0))

        #Bullets
        for bullet in player.bullets:
            bullet.draw(window)
            bullet.move()
            player.check_remove_bullets()
                
        #Create new objects
        if clock >= 2:
            clock = 0
            asteroids_tab.append(asteroids.RegularAsteroid())
            asteroids_tab.append(asteroids.ExplosiveAsteroid())
        
            enemies_tab.append(enemies.Drone())
            enemies_tab.append(enemies.Rocket())

            collectables_tab.append(collectable.BoostUpgrade())
            collectables_tab.append(collectable.HealthUpgrade())
        
        #Asteroids
        for asteroid in asteroids_tab:
            asteroid.draw(window)
            asteroid.move()

            if asteroid.check_if_off_screen():
                asteroids_tab.remove(asteroid)     

        #EnemieswdA
        for enemy in enemies_tab:
            enemy.draw(window)
            enemy.move()
            if enemy.check_if_off_screen():
                enemies_tab.remove(enemy)

            if isinstance(enemy, enemies.Rocket):
                enemy.shoot(player.rect.centerx, player.rect.centery)
                enemy.update_bullets(window)

        #Collectables
        #---Coins
        for coin in coins_tab:
            coin.draw(window)

        #---Boosters
        for booster in collectables_tab:
            booster.draw(window)
            booster.move()

        #collisions
        for bullet in player.bullets:
            if check_bullet_collisions(bullet, asteroids_tab):
                player.bullets.remove(bullet)
                continue
            if check_bullet_collisions(bullet, enemies_tab):
                player.bullets.remove(bullet)
                continue
        
        check_player_collisions(player, asteroids_tab, enemies_tab)
        player.draw(window)
        player.move(keys)
        player.draw_boost_bar(window)
        player.draw_health_bar(window)

        window.blit(score_text, (10, 10))
        window.blit(coins_text, (10, 50))

        pygame.display.update()

if __name__ == "__main__":
    main()