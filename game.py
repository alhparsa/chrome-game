import pygame
import random
from datetime import datetime
from math import atan

colours = {"Red": (255, 0, 0), "Green": (0, 255, 0),
           "White": (255, 255, 255), "Blue": (0, 0, 255),
           "Black": (0, 0, 0)}


class Player(pygame.sprite.Sprite):
    def __init__(self, width=10, height=30, x=80, y=350, velocity=6, acceleration=-1, color=colours["Blue"]):
        super(Player, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.counter = 2
        self.init_velocity = velocity
        self.init = y
        self.acceleration = acceleration
        self.velocity = velocity
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.fitness=-1

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

    def __init__(self, width=10, height=0, x_velocity=-3, color=colours["Green"], screen_width=500,
                 player_y_position=350):
        super(Barrier, self).__init__()
        self.x_velocity = x_velocity
        self.height_randomizer()
        self.image = pygame.Surface([width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = player_y_position - self.height + 30

    def height_randomizer(self):
        self.height = random.randint(15, 45)

    def update(self):
        self.rect.x += self.x_velocity


def outside_frame(barriers):
    for s in barriers.sprites():
        if s.rect.x < 0 - s.rect.width:
            barriers.remove(s)
    barriers.update()
    return barriers

def barrier_generator(barriers, speed_change, counter):
    new_barrier = Barrier(x_velocity=-3 + speed_change)
    new_barrier.height = random.randint(15, 45)
    barriers.add(new_barrier)
    return barriers


def player_generator():
    players = pygame.sprite.Group()
    for i in range(100):
        player = Player(velocity=random.randrange(1, 6),
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        players.add(player)
    return players

def fitness(player, barriers):
    if pygame.sprite.spritecollideany(player, barriers) is None:
        player.fitness+=1

def selection(selected,player):
            selected.add(player)



pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TRex")
barriers = pygame.sprite.Group()
speed_change = 0
counter = 1
players = player_generator()
select_players = pygame.sprite.Group()
run = True
timer = datetime.now()
clock = pygame.time.Clock()
parents_found=False

while run:
    secondary_timer = datetime.now()
    diff = secondary_timer - timer
    diff = diff.total_seconds()
    if diff >= 1.3 - 0.5 * atan(counter / 10):
        timer = datetime.now()
        barriers = barrier_generator(barriers, speed_change, counter)
        counter += 1
    if counter % 5 == 0:
        speed_change -= 0.01
    for s in players.sprites():
        if pygame.sprite.spritecollideany(s, barriers) is not None:
                if len(players.sprites())<=10:
                    selection(select_players,s)
                    print("done")
                players.remove(s)
        fitness(s,barriers)

    if not players:
        run == False
        pygame.quit()
        break
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
    barriers = outside_frame(barriers)
    barriers.draw(win)
    pygame.display.update()

pygame.quit()
