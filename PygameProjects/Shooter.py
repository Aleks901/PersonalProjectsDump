import pygame
import random
import math

class Player:
    
    def __init__(self, x, y, radius, health):
        self.x = x
        self.y = y
        self.radius = radius
        self.health = health
        self.speed = 5
        self.score = 0
        self.level = 1

    def move(self):
        keys = pygame.key.get_pressed()
        self.x += (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed

    def shoot(self):
        if len(bullets_on_screen) < 10:
            new_bullet = Bullet(self.x, self.y, 5)
            bullets_on_screen.append(new_bullet)

    def draw(self):
        pygame.draw.circle(screen, [255, 255, 255], [self.x, self.y], self.radius)
        
    def draw_score(self):
        score_font = pygame.font.SysFont('Comic Sans MS', 30)
        score_surface = score_font.render(f'Score: {self.score}. Level: {self.level}', False, (255, 255, 255))
        screen.blit(score_surface, (0, 0))
        
    
    def game_over(self):
        game_over_font = pygame.font.SysFont('Comic Sans MS', 30)
        game_over_surface = game_over_font.render(f'Game Over! Highscore: {self.score}', False, (255, 0, 0))
        screen.blit(game_over_surface, (300, 300))
        self.speed = 0
    
class Enemy:
    
    def __init__(self, x, y, radius, color1, color2, color3):
        self.x = x
        self.y = y
        self.radius = radius
        self.red = color1
        self.green = color2
        self.blue = color3
        self.speed = 0.3
        
    
    def draw(self):
        pygame.draw.circle(screen, [self.red, self.green, self.blue], [self.x, self.y], self.radius)
    
    def move(self):
        self.y += self.speed
        



class Bullet:
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, [255, 0, 0], [self.x, self.y], self.radius)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
player = Player(400, 500, 20, 100)
bullets_on_screen = []
enemy_instances = []
last_shot_time = 0
cooldown = 300


while running:
    pygame.font.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_shot_time > cooldown:
        player.shoot()
        last_shot_time = current_time



    for b in bullets_on_screen[:]:
        b.y -= b.speed
        if b.y < 0:
            bullets_on_screen.remove(b)
    
    if len(enemy_instances) < 10:
        enemy = Enemy(random.randint(10, 790),
                0,
                10,
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
        enemy_instances.append(enemy)
    
    for e in enemy_instances:
        if player.score == 30:
            e.speed = 0.5
            player.level = 2
        elif player.score == 60:
            e.speed = 1
            player.level = 3
        
        for b in bullets_on_screen:
            distance_from_eachother = math.sqrt((b.x - e.x) ** 2 + (b.y - e.y) ** 2)
            if distance_from_eachother <= b.radius + 5:
                try:
                    enemy_instances.remove(e)
                    player.score += 1
                    
                except ValueError:
                    print("Tried to delete enemy that was already deleted kek")
            
        
    screen.fill("black")
        
    for e in enemy_instances:
        e.draw()
        e.move()
        if e.y > 560:
            player.game_over()

    player.draw()
    player.move()
    player.draw_score()

    for b in bullets_on_screen:
        b.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
