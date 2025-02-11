import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption('Space Invader')
icon = pygame.image.load('Space-Invader-Images\Rocket.png')
pygame.display.set_icon(icon)

background = pygame.image.load('Space-Invader-Images\Bgimg.png')

#player
playerImg = pygame.image.load('Space-Invader-Images\space-invaders.png')
playerX = 368
playerY = 480
playerX_change = 0

score_val = 0
font = pygame.font.Font('freesansbold.ttf',23)

#Enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

print(type(enemyX))

for i in range(6):
    enemyImg.append(pygame.image.load('Space-Invader-Images\enemies.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('Space-Invader-Images\Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

running = True

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score():
    score = font.render("Score : "+str(score_val), True, (255, 255, 255))
    screen.blit(score, (15, 15))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg,(x, y))

def enemy(x, y): 
    for i in range(6):
        screen.blit(enemyImg[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2))+ (math.pow(enemyY-bulletY, 2)))
    if distance <= 27:
        return True
    else:
        return False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Space-Invader-Sound\laser.wav')
                    bullet_sound.play()
                    fire_bullet(playerX, bulletY)
                    bulletX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    for i in range(6):
        enemy(enemyX[i], enemyY[i])
        
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX =736

    for i in range(6):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY) 
        bulletY -= bulletY_change
    
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    
    #Game Over
    for i in range(6):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if enemyY[i] > 416 and collision:
            for j in range(6):
                enemyY[j] = 2000
            game_over_text()
            break

    #Check Collision
    for i in range(0,6):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_sound = mixer.Sound('Space-Invader-Sound\mixkit-arcade-game-explosion-2759.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50,150)
            #increase Score
            score_val += 1
    
    player(playerX, playerY) #space-ship image
    #display Score
    show_score()
        
    pygame.display.update()
    

