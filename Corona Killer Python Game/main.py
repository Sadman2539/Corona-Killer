import pygame
import math
import random
from pygame import mixer

# initialization
pygame.init()

# Game display
screen = pygame.display.set_mode((800, 600))

# Background
backgroundImg = pygame.image.load("background.png")

# caption and icon
pygame.display.set_caption("CORONA KILLER")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player variable
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy variables
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_number = 6
for i in range(enemy_number):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

# Bullet variables
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score = 0
score_font = pygame.font.Font("font.ttf", 35)
# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Game over font
over_font = pygame.font.Font("over.ttf", 40)
over_textX = 120
over_textY = 250


def background():
    screen.blit(backgroundImg, (0, 0))


def show_score():
    score_text = score_font.render("Corona Killed : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 15))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# bullet control function
# ready = can't see on screen
# fire = moving on the screen
def bullet(x, y):
    screen.blit(bulletImg, (x + 16, y + 10))
    global bullet_state
    bullet_state = "fire"


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

def game_over(x,y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (x,y))

# Game loop
running = True
while running:
    # RGB = Red Green Blue
    screen.fill((0, 87, 51))
    # Game window background function call
    background()

    # Game window control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # player control so that it doesn't go out of the boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy control
    for i in range(enemy_number):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 1
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -1

        # Game over Check
        if enemyY[i] >= 440:
            for j in range(enemy_number):
                enemyY[j] = 2000
            game_over(over_textX,over_textY)
            break
        # Collision Check
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            score += 1
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet control
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 50:
            bulletY = 480
            bullet_state = "ready"

    # Player call
    player(playerX, playerY)
    show_score()
    # Display update
    pygame.display.update()
