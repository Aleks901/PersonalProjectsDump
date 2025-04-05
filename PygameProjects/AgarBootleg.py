import random
import math
import pygame


def split(event):
    if event.type == pygame.K_SPACE and event.button == 1:
        return True
    return False


class Player:

    def __init__(self, x, y, radius, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.name = name
        self.points = 0

    def draw(self):
        if not split(event):
            pygame.draw.circle(screen, [255, 0, 0], [self.x, self.y], self.radius)

    def move(self):
        if pygame.mouse.get_pos()[0] < self.x:
            self.x -= 1
        elif pygame.mouse.get_pos()[0] > self.x:
            self.x += 1
        if pygame.mouse.get_pos()[1] < self.y:
            self.y -= 1
        elif pygame.mouse.get_pos()[1] > self.y:
            self.y += 1

    # def draw_score(self):
    #    score_font = pygame.font.SysFont('Comic Sans MS', 30)
    #    text_surface = score_font.render(f'Points: {self.player.points}', False, (0, 0, 0))
    #    screen.blit(text_surface, (0, 0))

class Score:

    def __init__(self, player: Player):
        self.x = 800
        self.y = 600
        self.player = player

    def draw_score(self):
        score_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = score_font.render(f'Points: {self.player.points}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))


class Blob:

    def __init__(self, x, y, color1, color2, color3):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

    def draw(self):
        pygame.draw.circle(screen,
                           [self.color1, self.color2, self.color3],
                           [self.x, self.y], 5)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
playerBlob = Player(20, 20, 20, "Aleks")
score = Score(playerBlob)

blob_instances = []

while running:
    pygame.font.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if split(event):
            pygame.draw.circle(screen, [255, 0, 0], [playerBlob.x - 30, playerBlob.y + 30], playerBlob.radius / 2)
            pygame.draw.circle(screen, [255, 0, 0], [playerBlob.x + 30, playerBlob.y - 30], playerBlob.radius / 2)

    if len(blob_instances) < 100:
        blob = Blob(random.randint(0, 800),
                    random.randint(0, 600),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255))
        blob_instances.append(blob)

    screen.fill("white")

    playerBlob.draw()
    playerBlob.move()
    for b in blob_instances:
        b.draw()
        distance_from_eachother = math.sqrt((playerBlob.x - b.x) ** 2 + (playerBlob.y - b.y) ** 2)
        if distance_from_eachother <= playerBlob.radius:
            blob_instances.remove(b)
            playerBlob.radius += 1
            playerBlob.points += 1

    score.draw_score()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
