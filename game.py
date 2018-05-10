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

    def __init__(self, width=10, height=random.randint(0, 65), x_velocity=-3, color=colours["Green"], screen_width=500,
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
            


#barrier = Barrier()
barriers = pygame.sprite.Group()
#barriers.add(barrier)
speed_change=0
barrier_speed=15;
counter=0


player = Player(win)
player_2 = Player(win, velocity=4, color=colours["Red"])
players = pygame.sprite.Group()
players.add(player)
players.add(player_2)

run = True

clock = pygame.time.Clock()
while run:
    if counter % 100 == 0:
        speed_change -= 0.2
        barrier_speed+=5
    clock.tick(100)
    win.fill(colours["White"])
    players.update()
    barriers.update()
    for s in barriers.sprites():
        if s.rect.x<0-s.rect.width:
            barriers.remove(s)
    if counter % barrier_speed == 0:
        new_barrier = Barrier()
        new_barrier.x_velocity+=speed_change
        print (new_barrier.height)
        new_barrier.height = random.randint(15, 45)
        barriers.add(new_barrier)
    
    barriers.draw(win)
    players.draw(win)
    pygame.display.update()
    counter+=1

pygame.quit()
