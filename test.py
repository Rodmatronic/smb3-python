import os
import pygame

# Enable stuff for debugging, looks ugly
DEBUG = True

# variables for the x/y. Do not change winx and winy
x = 0
y = -455
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
# 830 Y is the ground plane.
colliders = [
    # Ground
    (0, 830, 1300, 70),
    (2274, 415, 2205, 70),
    # Pipes
    (710, 755, 60, 60),
]

# init pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
running = True
pygame.mixer.music.load("sound/track1.mp3")
pygame.mixer.music.play(-1)

# images
stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))
hud = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "hud.png")))
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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        direction = 1
        velx += acceleration
        x -= velx
        if velx > limit:
            velx = limit
        print(velx)
    elif keys[pygame.K_LEFT]:
        direction = 0
        velx += acceleration
        x += velx
        if velx > limit:
            velx = limit
    elif keys[pygame.K_UP]:
        marioy -= 5
    elif keys[pygame.K_DOWN]:
        marioy += 5
    else:
        velx = 0

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
    screen.blit(hud, (0, 400))
    
    # very important to blit debug AFTER hud, so hitboxes may be viewed
    if DEBUG:
        for collider in colliders:
            pygame.draw.rect(screen, (255, 0, 0), 
                             (collider[0] + x, collider[1] + y, collider[2], collider[3]), 2)

    # Once the stage is done, render mario in whatever state he is set in.
    if direction == 1:
        flipped_mario = pygame.transform.flip(mario, True, False)
        screen.blit(flipped_mario, (mariox, marioy))
    else:
        screen.blit(mario, (mariox, marioy))


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
