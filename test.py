import os
import pygame
import sys

# Enable stuff for debugging, looks ugly
DEBUG = False

x = 0
y = -385
acceleration = 0.4
if DEBUG:
    limit = 50
limit = 6
friction = 1.2
velx = 0

mario_vely = 0
fall_acceleration = 0.42
fall_limit = 10

skid_timer = 0
skidding = False

winx = 640
winy = 480

# Why falling AND grounded? It's for animation. If the Y acceleration is positive, we are falling.
falling = True
grounded = False
animationcounter = 0

# Mario's Y axis is not locked to the stage like the X axis is.
mariox = winx/2
marioy = winy/2

# boxes that define collision
# 830 Y is the ground plane.
colliders = [
    (0, 767, 18000, 70), # ground
    (3744, 735, 150, 40), # ground stair 1
    (3904, 705, 150, 40), # ground stair 2
    (4030, 672, 150, 40), # ground stair 3
    (4130, 640, 445, 140), # ground stair 4, platform

    # semisolid
    (610, 671, 505, 6),
    # Pipes
]

# init pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
pygame.mixer.music.load("sound/track1.mp3")
pygame.mixer.music.play(-1)

# images

walk_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "walk1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "walk2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "walk3.png")))
]
walk_index = 0
walk_timer = 0

background = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bggrass.png")))
stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))
direction = 1
prev_direction = 1

# This makes mario's hitbox a bit wonky, since he is a square.
# But, on the other hand, it makes it easier. Easy, and works enough
mario_width = 32
mario_height = 47

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # main key movement
    # Invert X, do not invert Y.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        prev_direction = direction
        direction = 1
        velx += acceleration*friction
    elif keys[pygame.K_LEFT]:
        prev_direction = direction
        direction = 0
        velx -= acceleration*friction
    else:
        if velx > 0:
            velx -= acceleration*friction/1.5
            if velx < 0:
                velx = 0
        if velx < 0:
            velx += acceleration*friction/1.5
            if velx > 0:
                velx = 0

    if prev_direction != direction and grounded and abs(velx) > 2:
        skidding = True
        skid_timer = 0

    if skidding == True:
        skid_timer+=0.1
        print(skid_timer)

    x -= velx
    if velx > limit:
        velx = limit
    elif velx < - limit:
        velx = -limit
    # Jump logic
    if keys[pygame.K_z]:
        if grounded:
            mario_vely += -11
            falling = False
            grounded = False

    # mario gravity
    mario_vely += fall_acceleration
    if mario_vely > fall_limit:
        mario_vely = fall_limit
    if mario_vely >= 0:
        falling = True
    marioy += mario_vely

    if marioy > 500:
        print("we are dead")
        x = 0
        marioy = winy/2

    if not grounded:
        friction = 0.4
        if falling:
            mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mariofall.png")))
        else:
            mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mariojump.png")))
    else:
        friction = 1.1
        if skidding and skid_timer < 1.5:
                mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioskid.png")))
        else:
                skid_timer = 0
                skidding = False
                if abs(velx) > 0: # for negative and positive movement accel
                        step = max(1, int(20 / abs(velx)))
                        walk_timer += 1
                        if walk_timer >= step:
                               walk_timer = 0
                               walk_index = (walk_index + 1) % len(walk_frames)
                               mario = walk_frames[walk_index]
                else:
        	        mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))

    mario_rect = pygame.Rect(mariox, marioy+44, mario_width, mario_height-44) # the red one
    horiz_rect = pygame.Rect(mariox-4, marioy+4, mario_width+8, mario_height-8) # the geen one
    for collider in colliders:
        platform_rect = pygame.Rect(collider[0] + x, collider[1] + y, collider[2], collider[3])

        # Main mario collision
        if horiz_rect.colliderect(platform_rect) and ((mario_rect.left < platform_rect.left and velx > 0) or (mario_rect.right > platform_rect.right and velx < 0)):
            x += velx
            velx = 0;
            print("collided side")

        if mario_rect.colliderect(platform_rect):
            if mario_rect.bottom > platform_rect.top and mario_vely > 0:
                grounded = True
                falling = False
                marioy = platform_rect.top - mario_height
                mario_vely = 0

        # Horizontal collision check
    
    # Before the stage is blitted, check bounds.
    if x > 0:
        x = 0
    if x < -9600:
        x = -9600

    screen.blit(background, (0, -300))
    screen.blit(stage, (x, y))
    
    # Once the stage is done, render mario in whatever state he is set in.
    if direction == 1:
        flipped_mario = pygame.transform.flip(mario, True, False)
        screen.blit(flipped_mario, (mariox, marioy))
    else:
        screen.blit(mario, (mariox, marioy))

    if DEBUG:
        for collider in colliders:
            pygame.draw.rect(screen, (255, 0, 0), 
                             (collider[0] + x, collider[1] + y, collider[2], collider[3]), 2)
        pygame.draw.rect(screen, (255, 0, 0), (mariox, marioy+45, mario_width, mario_height-45)) # vert
        pygame.draw.rect(screen, (0, 255, 0), (mariox-4, marioy+4, mario_width+8, mario_height-8)) # horiz


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

print("why")
pygame.quit()
sys.exit()
