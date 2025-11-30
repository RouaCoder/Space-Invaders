import math
import random
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
try:
    mixer.music.load("background.wav")
    mixer.music.play(-1)
except Exception as e:
    print(f"Error loading background music: {e}")

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Players
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Second Player
player2Img = pygame.image.load('player2.png')
player2X = 430
player2Y = 480
player2X_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Second Player Bullet
bullet2Img = pygame.image.load('bullet2.png')
bullet2X = 0
bullet2Y = 480
bullet2X_change = 0
bullet2Y_change = 10
bullet2_state = "ready"

# Scores
score_value = 0
score2_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

text2X = 650
text2Y = 10

# Game Over and Winner Message
over_font = pygame.font.Font('freesansbold.ttf', 48)

def show_score(x, y, score):
    score_display = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_display, (x, y))

def game_over_text(winner):
    over_text = over_font.render("GAME OVER - " + winner + " Wins", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(400, 300))
    screen.blit(over_text, text_rect)

def player(x, y):
    screen.blit(playerImg, (x, y))

def player2(x, y):
    screen.blit(player2Img, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_bullet2(x, y):
    global bullet2_state
    bullet2_state = "fire"
    screen.blit(bullet2Img, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    try:
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                    except Exception as e:
                        print(f"Failed to load/play bullet sound: {e}")
            if event.key == pygame.K_q:
                player2X_change = -5
            if event.key == pygame.K_d:
                player2X_change = 5
            if event.key == pygame.K_w:
                if bullet2_state == "ready":
                    try:
                        bulletSound2 = mixer.Sound("laser2.wav")
                        bulletSound2.play()
                        bullet2X = player2X
                        fire_bullet2(bullet2X, bullet2Y)
                    except Exception as e:
                        print(f"Failed to load/play bullet2 sound: {e}")

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_a, pygame.K_d]:
                player2X_change = 0

    # Player 1 Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Player 2 Movement
    player2X += player2X_change
    if player2X <= 0:
        player2X = 0
    elif player2X >= 736:
        player2X = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Move enemies off screen
            if score_value > score2_value:
                game_over_text("Player 1")
            elif score2_value > score_value:
                game_over_text("Player 2")
            else:
                game_over_text("No Winner")
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision Detection for both players
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            try:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
            except Exception as e:
                print(f"Failed to load/play explosion sound: {e}")
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        collision2 = isCollision(enemyX[i], enemyY[i], bullet2X, bullet2Y)
        if collision2:
            try:
                explosionSound2 = mixer.Sound("explosion.wav")
                explosionSound2.play()
            except Exception as e:
                print(f"Failed to load/play explosion2 sound: {e}")
            bullet2Y = 480
            bullet2_state = "ready"
            score2_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement for both players
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet2Y <= 0:
        bullet2Y = 480
        bullet2_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bullet2_state == "fire":
        fire_bullet2(bullet2X, bullet2Y)
        bullet2Y -= bullet2Y_change

    player(playerX, playerY)
    player2(player2X, player2Y)
    show_score(textX, textY, score_value)
    show_score(text2X, text2Y, score2_value)
    pygame.display.update()
