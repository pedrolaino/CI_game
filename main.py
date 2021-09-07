import pygame
from pygame import mixer
import random
import math

# inicializa pygame
pygame.init()
# crea screen
screen = pygame.display.set_mode((800, 600))
# creo variables para sonidos
musica_fondo = "aud/bgjuego.wav"
sonido_disparo = "aud/laser.wav"
sonido_colision = "aud/hit.wav"
# fondo
bg = pygame.image.load('img/bg.png')
# musica bg
mixer.music.load(musica_fondo)
mixer.music.play(-1)
# titulo e icono
pygame.display.set_caption("Cachen Invaders")
icon = pygame.image.load('img/ufo.png')
pygame.display.set_icon(icon)

# Jugador
playerImg = pygame.image.load('img/nave.png')
velocidad_player = 0.3
playerX = 370
playerY = 480
playerX_change = 0
# Enemigo
# ignorar esta linea:
enemyImg = [pygame.image.load('img/cachen1.png'), pygame.image.load('img/cachen2.png'),
            pygame.image.load('img/cachen3.png'),
            pygame.image.load('img/cachen4.png'), pygame.image.load('img/cachen5.png'),
            pygame.image.load('img/cachen6.png')]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

contador_cachen = 1


def eleccion_sprite():
    for cachen in range(6):
        return f'img/cachen1.png'

velocidad_enemigo = 0.2
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(eleccion_sprite()))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))

    enemyX_change.append(velocidad_enemigo)
    enemyY_change.append(40)

# Bala

bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_ready = True

# Puntuación

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textX = 10
textY = 10
color_fuente = (255, 255, 255)
contador_velocidad = 0

# game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 62)


def show_score(x, y):
    score = font.render("Cachens eliminados: " + str(score_value), True, color_fuente)
    screen.blit(score, (x, y))
    global contador_velocidad
    global velocidad_enemigo
    if contador_velocidad == 10:
        velocidad_enemigo += 0.05
        contador_velocidad = 0


def game_over_text():
    over_text = game_over_font.render("PERDISTE PETE", True, color_fuente)
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_ready
    bullet_ready = False
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distancia = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distancia < 27:
        return True
    else:
        return False


# Game Loop


running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -velocidad_player
            if event.key == pygame.K_RIGHT:
                playerX_change = velocidad_player
            if event.key == pygame.K_SPACE:
                if bullet_ready is True:
                    bullet_sound = mixer.Sound(sonido_disparo)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # limites de la pantalla para la nave
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # movimiento enemigo
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = velocidad_enemigo
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -velocidad_enemigo
            enemyY[i] += enemyY_change[i]
        # colisión
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_sound = mixer.Sound(sonido_colision)
            bullet_sound.play()
            bulletY = 480
            bullet_ready = True
            score_value += 1
            contador_velocidad += 1

            ############################################################

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # movimiento bala
    if bulletY <= 0:
        bulletY = 480
        bullet_ready = True

    if bullet_ready is False:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
