import pygame


class Item:

    def __init__(self, power):
        self.power = power


class Player:

    def __init__(self):
        self.points = 0
        self.power = 1


class Cookie:

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.radius += 0.1


class Score:

    def __init__(self, player: Player):
        self.x = 800
        self.y = 600
        self.player = player

    def draw_score(self):
        score_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = score_font.render(f'Points: {self.player.points}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))


class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), hover_color=(0, 100, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, button_color, self.rect)

        # Render text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Void Clicker")
clock = pygame.time.Clock()
cookie = Cookie(400, 300, 100, "black")
playerCharacter = Player()
score = Score(playerCharacter)
shopButton = Button(0, 550, 200, 50, "+1: 100pts")
shopButton2 = Button(200, 550, 200, 50, "+2: 200pts")
shopButton3 = Button(400, 550, 200, 50, "+3: 500pts")
shopButton4 = Button(600, 550, 200, 50, "+4: 1000pts")

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                distance = ((mx - cookie.x) ** 2 + (my - cookie.y) ** 2) ** 0.5
                if distance <= cookie.radius:
                    cookie.radius -= playerCharacter.power
                    playerCharacter.points += 1

        if shopButton.is_clicked(event) and playerCharacter.points >= 100:
            playerCharacter.power += 1
            playerCharacter.points -= 100
        if shopButton2.is_clicked(event) and playerCharacter.points >= 200:
            playerCharacter.power += 2
            playerCharacter.points += 200
        if shopButton3.is_clicked(event) and playerCharacter.points >= 500:
            playerCharacter.power += 3
            playerCharacter.points -= 500
        if shopButton4.is_clicked(event) and playerCharacter.points >= 1000:
            playerCharacter.power += 4
            playerCharacter.points -= 1000

        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    cookie.draw()
    score.draw_score()
    shopButton.draw(screen)
    shopButton2.draw(screen)
    shopButton3.draw(screen)
    shopButton4.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
