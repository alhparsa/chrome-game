import pygame

pygame.init()
win  = pygame.display.set_mode((1000,1000))

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
