import pygame
import os

# Enable stuff for debugging, looks ugly
DEBUG = True

# variables for the x/y. Do not change winx and winy
x = 0
y = 0
acceleration = 0.2
limit = 6
friction = 0.5
velx = 0

mario_vely = 0
fall_acceleration = 0.3
fall_limit = 6

winx = 640
winy = 480

# Mario's Y axis is not locked to the stage like the X axis is.
mariox = winx/2
marioy = winy/2

# boxes that define collision
colliders = [
    # Ground
    (0, 415, 2205, 70),
    (2274, 415, 2205, 70),
    # Pipes
    (900, 355, 60, 60),
    (1218, 320, 60, 100),
    (1475, 288, 60, 130),
    (1826, 288, 60, 130),
]

# init pygame
pygame.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
running = True

# images
stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))
direction = 1

# This makes mario's hitbox a bit wonky, since he is a square.
# But, on the other hand, it makes it easier. Easy, and works enough
mario_rect = mario.get_rect()
mario_width = mario_rect.width
mario_height = mario_rect.height

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # main key movement
    # Invert X, do not invert Y.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            direction = 1
            velx += acceleration
            x -= velx
            if velx > limit:
                velx = limit
            print(velx)
        if event.key == pygame.K_LEFT:
            direction = 0
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

    # mario gravity
    mario_vely += fall_acceleration
    if mario_vely > fall_limit:
        mario_vely = fall_limit
    marioy += mario_vely

    if marioy > 500:
        print("we are dead")
        x = 0
        marioy = winy/2

    mario_rect = pygame.Rect(mariox, marioy, mario_width, mario_height)
    for collider in colliders:
        platform_rect = pygame.Rect(collider[0] + x, collider[1] + y, collider[2], collider[3])

        # Main mario collision
        if mario_rect.colliderect(platform_rect):
            if mario_rect.bottom > platform_rect.top and mario_vely > 0:
                marioy = platform_rect.top - mario_height
                mario_vely = 0
            elif mario_rect.top < platform_rect.bottom and mario_vely < 0:
                marioy = platform_rect.bottom
                mario_vely = 0

    # Before the stage is blitted, check bounds.
    if x > 0:
        x = 0
    if x < -4830:
        x = -4830

    screen.blit(stage, (x, y))
    
    if DEBUG:
        for collider in colliders:
            pygame.draw.rect(screen, (255, 0, 0), 
                             (collider[0] + x, collider[1] + y, collider[2], collider[3]), 2)

    # Once the stage is done, render mario in whatever state he is set in.
    screen.blit(mario, (mariox, marioy))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
