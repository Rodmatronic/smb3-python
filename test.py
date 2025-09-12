import pygame
import os

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

ground_platforms = [
    (0, 415, 2150, 50),      # Main ground platform
    (900, 355, 60, 60),
    (1200, 320, 60, 100),
]

# init pygame
pygame.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
running = True
stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))

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

    # mario gravity
    mario_vely += fall_acceleration
    if mario_vely > fall_limit:
        mario_vely = fall_limit
    marioy += mario_vely

    if marioy > 410:
        print("test")

    # Check for collisions with platforms
    mario_rect = pygame.Rect(mariox, marioy, mario_width, mario_height)
    for platform in ground_platforms:
        platform_rect = pygame.Rect(platform[0] + x, platform[1] + y, platform[2], platform[3])
        
        if mario_rect.colliderect(platform_rect):
            # Collision from above (landing on platform)
            if mario_rect.bottom > platform_rect.top and mario_vely > 0:
                marioy = platform_rect.top - mario_height
                mario_vely = 0
            # Collision from below (hitting platform from underneath)
            elif mario_rect.top < platform_rect.bottom and mario_vely < 0:
                marioy = platform_rect.bottom
                mario_vely = 0

    # Before the stage is blitted, check bounds.
    if x > 0:
        x = 0
    if x < -4830:
        x = -4830

    screen.blit(stage, (x, y))

    for platform in ground_platforms:
        pygame.draw.rect(screen, (255, 0, 0), 
                         (platform[0] + x, platform[1] + y, platform[2], platform[3]), 2)

    # Once the stage is done, render mario in whatever state he is set in.
    screen.blit(mario, (mariox, marioy))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
