# Written by Roderick Pike.
#
# There are some things I don't like about this codebase,
# nontheless I think it's good for a final programming
# assignment.
#

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

coins = 0
score = 0
lives = 5
time = 500

# Why falling AND grounded? It's for animation. If the Y acceleration is positive, we are falling.
falling = True
grounded = False
animationcounter = 0

# Mario's Y axis is not locked to the stage like the X axis is.
mariox = winx/2
marioy = winy/2

# colliders/objects in the level. Index:
# 1 = Question
# 2 = Hit Block
# 3 = Coin
# 4 = checkpost
# 5 = checkpost (used)
# 6 = goalpost
# 7 = koopa
# 10 = dragon coin
colliders = [
    (0, 767, 18000, 70, 0), # ground
    (3744, 735, 150, 61, 0), # ground stair 1
    (3904, 705, 150, 61, 0), # ground stair 2
    (4030, 672, 150, 61, 0), # ground stair 3
    (4130, 640, 445, 140, 0), # ground stair 4, platform
    (6978, 706, 317, 61, 0), # ground platform
    # semisolid
    (610, 671, 505, 4),
    (1410, 643, 221, 4),
    (5986, 674, 159, 4),
    (6050, 578, 254, 4),
    (6241, 674, 191, 4),
    (6786, 609, 318, 4),

    # Pipes
    (5409, 673, 64, 93),
    (5474, 642, 64, 127),
    (7743, 706, 64, 61),
    (8097, 675, 64, 93),
    (8641, 705, 64, 61),
    (8735, 674, 64, 93),

    # Coins
    (2471, 640, 22, 32, 3),
    (2502, 610, 22, 32, 3),
    (2568, 610, 22, 32, 3),
    (2599, 640, 22, 32, 3),
    (4582, 510, 22, 32, 3),
    (4614, 482, 22, 32, 3),
    (4646, 482, 22, 32, 3),
    (6885, 482, 22, 32, 3),
    (6918, 482, 22, 32, 3),
    (6951, 482, 22, 32, 3),

    # Dragon coins
    (2526, 580, 35, 54, 10),
    (3453, 580, 35, 54, 10),
    (4672, 451, 35, 54, 10),
    (7005, 454, 36, 51, 10),

    # special stuff
#    (5138, 635, 64, 136, 4),
#    (9656, 479, 42, 292, 6),

    # koopas
    (765, 740, 32, 28, 7),
    (845, 740, 32, 28, 7),
    (925, 740, 32, 28, 7),

    (1267, 740, 32, 28, 7),
    (1980, 740, 32, 28, 7),
    (3326, 740, 32, 28, 7),
    (3675, 740, 32, 28, 7),


    # berries
    (351, 705, 29, 21, 11),
    (2111, 674, 31, 25, 11),
    (2306, 705, 27, 23, 11),
    (2786, 705, 26, 21, 11),
    (3137, 673, 24, 26, 11),
    (3582, 704, 30, 23, 11),
    (4222, 577, 30, 26, 11),
    (4383, 540, 29, 27, 11),
    (5820, 702, 30, 26, 11),
    (6624, 704, 27, 26, 11),
    (7422, 705, 24, 23, 11),
    (7582, 671, 29, 30, 11),
    (7902, 670, 27, 28, 11),
    (8285, 707, 27, 18, 11),
    
]

# init pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((winx, winy))
clock = pygame.time.Clock()
pygame.mixer.music.load("sound/track1.mp3")

jump_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'sound', 'jump.wav'))
jump_sound.set_volume(0.5)

coin_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'sound', 'coin.wav'))
coin_sound.set_volume(0.5)

bump_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'sound', 'bump.wav'))
bump_sound.set_volume(0.5)

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


# images
walk_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "walk1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "walk2.png"))),
]
walk_index = 0
walk_timer = 0

# images

# KOOPA images
koopawalk_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "koopawalk1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "koopawalk2.png"))),
]
koopawalk_index = 0
koopawalk_timer = 0

# COIN images
coin_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "coin1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "coin2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "coin3.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "coin4.png"))),
]
coin_index = 0
coin_timer = 0

# DRAGON COIN images (big coin)
dragoncoin_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin3.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin4.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin5.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin6.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin7.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin8.png"))),
]
dragoncoin_index = 0
dragoncoin_timer = 0

# Berries
berry_frames = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "berry1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "berry2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "berry3.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "berry4.png"))),
]
berry_index = 0
berry_timer = 0

question_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "question.png")))
hit_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "hit.png")))
coin_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "coin.png")))
dragoncoin_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dragoncoin1.png")))
berry_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "berry1.png")))
checkpost_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "checkpost.png")))
checkpostused_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "checkpostused.png")))


titlescreen = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "titlescreen.png")))
titlebackground = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "titlebackground.png")))

background = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bggrass.png")))

stage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "test.png")))
mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioidle.png")))

hud = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "hud.png")))

direction = 1
prev_direction = 1

# This makes mario's hitbox a bit wonky, since he is a square.
# But, on the other hand, it makes it easier. Easy, and works enough
mario_width = 32
mario_height = 47

font = pygame.font.Font(os.path.join(os.getcwd(), 'world.ttf'), 16) # Custom font

dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

gamestate = 0
titlex = 0
titley = 0
titleborderx = 0
titlebordery = 0
titletimer = 0

titlefadetimer = 0
fadeout = 0
Running = True

koopa = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "koopawalk1.png")))

while Running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        #
        # This is never used in-game and is STRICTLY for
        # when creating levels.
        #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                dx, dy = event.pos
                lx = dx - x
                ly = dy - y
                drag_start = (lx, ly)
                drag_end = (lx, ly)

        if event.type == pygame.QUIT:
            Running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                mx, my = event.pos
                lx = mx - x
                ly = my - y
                drag_end = (lx, ly)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                dragging = False
                sx, sy = drag_start
                ex, ey = drag_end
                w = ex - sx
                h = ey - sy
                print("Box:", sx, sy, w, h)

    if gamestate == 0:
        screen.blit(titlebackground, (titlex, titley))

        screen.blit(titlescreen, (titleborderx, titlebordery))

        # how-to text and shadow
        text_surface = font.render("X to run  Z to jump  arrows to move!", True, (0, 0, 0))
        screen.blit(text_surface, (122, 302))

        text_surface = font.render("X to run  Z to jump  arrows to move!", True, (255, 255, 255))
        screen.blit(text_surface, (120, 300))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gamestate=1

        #    width, height = titlebackground.get_size()
        #    titlebackground = pygame.transform.scale(titlebackground, (width-2, height-2))
        #    screen.blit(titlebackground, (titlex, titley))

        pygame.display.flip()
        clock.tick(60)
    else:
            
# -------- movement --------

        time-=0.05

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            prev_direction = direction
            direction = 1
            velx += acceleration*friction
            if keys[pygame.K_x]:
                limit=6
            else:
                limit=3
        elif keys[pygame.K_LEFT]:
            prev_direction = direction
            direction = 0
            velx -= acceleration*friction
            if keys[pygame.K_x]:
                 limit=6
            else:
                 limit=3
        else:
            if velx > 0:
                velx -= acceleration*friction/1.5
                if velx < 0:
                    velx = 0
            if velx < 0:
                velx += acceleration*friction/1.5
                if velx > 0:
                    velx = 0

        if prev_direction != direction and grounded and abs(velx) > 1:
            skidding = True
            skid_timer = 0

        if skidding == True:
            skid_timer+=0.1

        x -= velx
        if velx > limit:
            velx = limit
        elif velx < - limit:
            velx = -limit
        # Jump logic
        if keys[pygame.K_z]:
            if grounded:
                jump_sound.play()
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
            x = 0
            marioy = winy/2

# -------- animation --------

        if not grounded:
            friction = 1.6
            if falling:
                mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mariofall.png")))
            else:
                mario = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mariojump.png")))
        else:
            friction = 1.8
            if skidding and skid_timer < 0.5:
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

# -------- mario collision --------

        mario_rect = pygame.Rect(mariox, marioy+44, mario_width, mario_height-44) # the red one
        horiz_rect = pygame.Rect(mariox-4, marioy+4, mario_width+8, mario_height-8) # the geen one
        for collider in colliders:
            platform_rect = pygame.Rect(collider[0] + x, collider[1] + y, collider[2], collider[3])

            # Main mario collision
            if collider[3] > 4:
                if horiz_rect.colliderect(platform_rect) and ((mario_rect.left < platform_rect.left and velx > 0) or (mario_rect.right > platform_rect.right and velx < 0)):
                    if len(collider) >= 5 and collider[4] == 99: # none
                        break
                    if len(collider) >= 5 and collider[4] == 5: # used checkpoint
                        break
                    if len(collider) >= 5 and collider[4] == 3: # coin
                        coin_sound.play()
                        coins+=1
                        if coins > 99:
                            coins = 0
                            lives+=1
                        score+=100
                        index = colliders.index(collider)
                        sx, sy, sw, sh, st = collider
                        colliders[index] = (sx, sy, sw, sh, 99)
                        break
                    if len(collider) >= 5 and collider[4] == 10: # dragon coin
                        coin_sound.play()
                        coins+=10
                        if coins > 99:
                            coins = 0
                            lives+=1
                        score+=1000
                        index = colliders.index(collider)
                        sx, sy, sw, sh, st = collider
                        colliders[index] = (sx, sy, sw, sh, 99)
                        break
                    if len(collider) >= 5 and collider[4] == 11: # berry
                        break

                    if len(collider) >= 5 and collider[4] == 4: # checkpost
                        index = colliders.index(collider)
                        sx, sy, sw, sh, st = collider
                        colliders[index] = (sx, sy, sw, sh, 5)
                        break

                    if len(collider) >= 5 and collider[4] == 6: # goalpost
                        index = colliders.index(collider)
                        sx, sy, sw, sh, st = collider
                        colliders[index] = (sx, sy, sw, sh, 5)
                        break
                    
                    x += velx
                    velx = 0;

            if mario_rect.colliderect(platform_rect):
                if len(collider) >= 5 and collider[4] == 99:
                    break
                if len(collider) >= 5 and collider[4] == 11:
                    break
                if len(collider) >= 5 and collider[4] == 3:
                    index = colliders.index(collider)
                    sx, sy, sw, sh, st = collider
                    colliders[index] = (sx, sy, sw, sh, 99)
                    break
                if len(collider) >= 5 and collider[4] == 10:
                    index = colliders.index(collider)
                    sx, sy, sw, sh, st = collider
                    colliders[index] = (sx, sy, sw, sh, 99)
                    break

                if len(collider) >= 5 and collider[4] == 5:
                    break
                if mario_rect.bottom > platform_rect.top and mario_vely > 0:
                    grounded = True
                    falling = False
                    marioy = platform_rect.top - mario_height
                    mario_vely = 0

            # Horizontal collision check

# -------- blit stuff --------
        
        # Before the stage is blitted, check bounds.
        if x > 0:
            x = 0
        if x < -9600:
            x = -9600

# -------- background stuff --------

        # various positions for paralax-like effect
        screen.blit(background, (x/4, -359))
        screen.blit(background, (x/4 + 1024, -350))
        screen.blit(background, (x/4 + 2048, -350))

        screen.blit(stage, (x, y))
        screen.blit(hud, (0, 0))
        text_surface = font.render(str(coins), True, (255, 255, 240))
        screen.blit(text_surface, (514, 24))
        text_surface = font.render(str(score), True, (255, 255, 240))
        screen.blit(text_surface, (434, 40))
        text_surface = font.render(str(round(time)), True, (255, 255, 240))
        screen.blit(text_surface, (372, 40))
        text_surface = font.render(str(lives), True, (255, 255, 240))
        screen.blit(text_surface, (138, 40))


# ANIMATIONS, for objects

        koopawalk_timer += 1
        if koopawalk_timer >= 8:
            koopawalk_timer = 0
            koopawalk_index = (koopawalk_index + 1) % len(koopawalk_frames)
            koopa = koopawalk_frames[koopawalk_index]

        coin_timer += 1
        if coin_timer >= 8:
            coin_timer = 0
            coin_index = (coin_index + 1) % len(coin_frames)
            coin_sprite = coin_frames[coin_index]

        dragoncoin_timer += 1
        if dragoncoin_timer >= 8:
            dragoncoin_timer = 0
            dragoncoin_index = (dragoncoin_index + 1) % len(dragoncoin_frames)
            dragoncoin_sprite = dragoncoin_frames[dragoncoin_index]

        berry_timer += 1
        if berry_timer >= 8:
            berry_timer = 0
            berry_index = (berry_index + 1) % len(berry_frames)
            berry_sprite = berry_frames[berry_index]

        # draw objects to the screen
        for c in colliders:
            if len(c) >= 5:
                if c[4] == 1:
                    screen.blit(question_sprite, (c[0] + x, c[1] + y))
                if c[4] == 2:
                    screen.blit(hit_sprite, (c[0] + x, c[1] + y))
                if c[4] == 3:
                    screen.blit(coin_sprite, (c[0] + x-5, c[1] + y))
                if c[4] == 4:
                    screen.blit(checkpost_sprite, (c[0] + x, c[1] + y))
                if c[4] == 5:
                    screen.blit(checkpostused_sprite, (c[0] + x, c[1] + y))
                if c[4] == 7:
                        index = colliders.index(c)
                        sx, sy, sw, sh, st = c
                        sx-=0.5
                        colliders[index] = (sx, sy, sw, sh, 7)
                        screen.blit(koopa, (c[0] + x, c[1] + y-34)) # the 34 is cause koopas are higher than hitbox
                if c[4] == 10:
                    screen.blit(dragoncoin_sprite, (c[0]+7 + x-5, c[1] + y))
                if c[4] == 11:
                    screen.blit(berry_sprite, (c[0]+7 + x-5, c[1] + y))
                
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

        # This code isn't very efficient and it lags a bunch.
        # set a lower baseline so lag spikes are lessened
        clock.tick(50)

pygame.quit()
