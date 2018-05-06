import pygame,random
pygame.init()
win=pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")
colours = {"Red":   (255,0,0),      "Green":    (0,255,0),
          "White":  (255,255,255),  "Blue":     (0,0,255),
          "Black":  (0,0,0)}
run =True
x=80
y=350
width=10
height=30
vel=6
init_vel = vel
init=y
accel = -1 
pressed = False
counter = 2
obs_maxh=65
obs_minh=35
obs_endh=random.randint(obs_minh,obs_maxh)
while run:
    pygame.time.delay(13)
    if  pressed == True:
        vel += accel
        y -= vel
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and (counter<10) and y==init:
        counter += 1
    else:
        if y>=init and pressed==True:
            vel = init_vel
            y=init
            pressed = False
        elif(counter>2 and pressed==False):
            vel*=round(counter/(1.5**2.8))
            pressed = True
            counter = 2

    
    
    win.fill(colours["White"])
    pygame.draw.rect(win,colours["Red"],(x,y-height,width,height))
    pygame.draw.rect(win,colours["Blue"],(250,350-obs_endh,width,obs_endh))
    pygame.display.update()
            
pygame.quit()
            
