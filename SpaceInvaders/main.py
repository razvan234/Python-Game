import pygame
import math
import random

# Intialize the pygame module
pygame.init()
# create the screen
screen = pygame.display.set_mode((900, 700))  # 900 weight and 700 height
# background
background = pygame.image.load("3d-hyperspace-background-with-warp-tunnel-effect.jpg")
# Title and Icon
pygame.display.set_caption("Students and the magic five Project")  # we set the name of the window
icon = pygame.image.load("student.png")  # we set the icon
pygame.display.set_icon(icon)  # we initialize the icon
# Player
player_Img = pygame.image.load("spaceship 1.png")  # the player icon
playerX = 430  # the coordonates where we want the player to be on the weight (x axis)
playerY = 590  # the coordonates where we want the player to be on the height (y axis)
playerX_change = 0

# Enemy
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_enemies = 6
for i in range(number_enemies):
    enemy_Img.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 835))
    enemyY.append(random.randint(57, 130))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

# Bullet

# Ready - the bullet can't be seen on the screen
# Fire  - the bullet is moving

Bullet_Img = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 590
BulletX_change = 0
BulletY_change = 1
Bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)  # ttf is the extension of the font

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)  # ttf is the extension of the font


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(over_text, (250, 300))


def restart_game():

    restart_test = over_font.render(input('Do you wish to restart ? Y/N '), True, (255, 255, 255))
    screen.blit(restart_test, (250, 300))
    if restart_test == 'Y':
        return True
    else:
        return False




def player(x, y):
    screen.blit(player_Img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = 'fire'
    screen.blit(Bullet_Img, (x + 16, y + 10))


def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
# without this my window will only hold for 1 sec
while running:
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # this basically gives me an exit button on my screen
            running = False
        # if key is pressed check if its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            elif event.key == pygame.K_SPACE:
                if Bullet_state is 'ready':
                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_r:
                restart_test = over_font.render(input('Do you wish to restart ? Y/N '), True, (255, 255, 255))
                screen.blit(restart_test, (250, 300))
                if restart_test =='Y':
                    continue
                else:
                    break



    playerX += playerX_change
    #  Checking for Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:  # because my image is 64 pixels
        playerX = 836
    # Enemy movement
    for i in range(number_enemies):

        # Game Over
        if enemyY[i] > 645:
            for j in range(number_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            # Collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            BulletY = 590
            Bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 835)
            enemyY[i] = random.randint(57, 130)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if BulletY <= 0:
        BulletY = 590
        Bullet_state = 'ready'
    if Bullet_state is 'fire':
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
