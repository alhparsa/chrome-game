import pygame
import random

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TRex")
colours = {"Red": (255, 0, 0), "Green": (0, 255, 0),
           "White": (255, 255, 255), "Blue": (0, 0, 255),
           "Black": (0, 0, 0)}


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, width=10, height=30, x=80, y=350, velocity=6, acceleration=-1, color=colours["Blue"]):
        super(Player, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.counter = 2
        self.init_velocity = velocity
        self.init = y
        self.screen = screen
        self.acceleration = acceleration
        self.velocity = velocity
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def update(self):
        if self.pressed:
            self.velocity += self.acceleration
            self.rect.y -= self.velocity
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and (self.counter < 10) and self.rect.y == self.init:
            self.counter += 1
        else:
            if self.rect.y >= self.init and self.pressed:
                self.velocity = self.init_velocity
                self.rect.y = self.init
                self.pressed = False
            elif self.counter > 2 and not self.pressed:
                self.velocity *= round(self.counter / (1.5 ** 2.8))
                self.pressed = True
                self.counter = 2


class Barrier(pygame.sprite.Sprite):

    def __init__(self, width=10, height=random.randint(15, 45), x_velocity=-3, color=colours["Green"], screen_width=500,
                 player_y_position=350):
        super(Barrier, self).__init__()
        self.x_velocity = x_velocity
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = player_y_position - height + 30
        self.rect.x = screen_width

    def update(self):
        self.rect.x += self.x_velocity


def collision_test(players, barriers):

run = True

clock = pygame.time.Clock()
while run:
    clock.tick(100)
    win.fill(colours["White"])
    players.update()
    players.draw(win)
    for s in players.sprites():
        if pygame.sprite.spritecollideany(s, barriers) is not None:
            players.remove(s)
    if not players:
        run == False
        pygame.quit()
        break
    barriers.update()
    barriers.draw(win)
    pygame.display.update()

pygame.quit()
