import pygame
import os

# variables for the x/y. Do not change winx and winy
x = 0
y = -266
acceleration = 0.2
limit = 6
friction = 0.5
velx = 0

mario_vely = 0

winx = 800
winy = 600

# Mario's Y axis is not locked to the stage like the X axis is.
mariox = winx/2
marioy = winy/2

# init pygame
pygame.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
running = True
stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # main key movement
    # Invert X, do not invert Y.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            velx += acceleration
            x -= velx
            if velx > limit:
                velx = limit
            print(velx)
        if event.key == pygame.K_LEFT:
            velx += acceleration
            x += velx
            if velx > limit:
                velx = limit
        if event.key == pygame.K_UP:
            marioy -= 5
        if event.key == pygame.K_DOWN:
            marioy += 5
    else:
        velx = 0
        print(velx)

    # Before the stage is blitted, check bounds.
    if x > 0:
        x = 0
    if x < -4830:
        x = -4830

    screen.blit(stage, (x, y))

    # Once the stage is done, render mario in whatever state he is set in.
    screen.blit(mario, (mariox, marioy))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
