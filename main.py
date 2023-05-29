#author : Nitin singh
#tech used : python pygame




import pygame
import random
import math
from pygame import mixer



# initialize the pygame
pygame.init()
# create the screen of size of 800pixel of width and 600 pixels of height
screen = pygame.display.set_mode((800, 600))
# event : any thing that happening in th game widndow
# since we didn't added event and quit command thats why game window is hanging


# background setting
background = pygame.image.load("background.png")


#background sond
mixer.music.load("background.mp3")
mixer.music.play(-1)


# Title and Icon
# image must be in the project file
pygame.display.set_caption("space Invanders")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

# how to add image in this game
# since we need exact cordinates to we need to put player at cordinates
playerimg = pygame.image.load("spaceship.png")
playerX = 370  # means adding value move in right and subtracting it goes left

playerY = 480  # same with  Y cordinates
# persistent in our eye tells that object didn't disapper insted moving
playerX_change = 0
playerY_change = 0

# enemy setting
enemyimg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies=6


for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load("skull.png"))
    enemyX.append(random.randint(0, 735 ))  # means adding value move in right and subtracting it goes left

    enemyY.append(random.randint(50, 150)) # same with  Y cordinates
    # persistent in our eye tells that object didn't disapper insted moving
    enemyX_change.append(0.3)
    enemyY_change.append(30)

# bullet setting
# Ready-you can't see the bullet on the window
# fire-bullet is being fired
bulletimg = pygame.image.load("bullet3.png")
bulletX = 0  # means adding value move in right and subtracting it goes left
bulletY = 480  # same with  Y cordinates
# persistent in our eye tells that object didn't disapper insted moving
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"



#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10
#game over txt
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score=font.render("score :" +str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def game_over_text():
    over_text = over_font.render("Game over ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))
    # to draw the player image on window


# to draw the enemy image on window
def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))


# for bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

'''**************************************************************************************************'''
# GAME LOOP

running = True
while running:
    # RGB=red,green,blue range is 255 that is white and 000 is black
    screen.fill((155, 150, 90))

    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right of left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser-gun.mp3")
                    bullet_sound.play()
                    # it get current x cordinate of the player in bullet and save
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0




        # if event.type == pygame.KEYUP:
        # if event.key == pygame.K_UP:
        # playerY_change = -0.3
        # if event.key == pygame.K_DOWN:
        # playerY_change = 0.3

    # anything that you want to be persistent in window and doesnot want to be disappear the use this

    # this is how movment mechanics of  player
    # playerX+=0.2
    # playerY-=0.2
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 736 because it pixel of player is taken in consideration

    if playerY <= 0:
        playerY = 0
    elif playerY >= 526:
        playerY = 526



    for i in range(number_of_enemies):
        #game over
        if enemyY[i] >480:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # for enemy boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]


        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("enemyloss.mp3")
            explosion_sound.play()

            bulletY = 480
            bullet_state = "ready"

            score_value += 1

            enemyX[i] = random.randint(0, 735)

            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)

    # bulletmovement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change







    # always put all image below screen so that the image will not be undrneath of the color of window
    player(playerX, playerY)
    show_score(textX,textY)

    # since we are constantly updating our window thats why using update method
    pygame.display.update()
