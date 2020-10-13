import pygame
import random
import math
from pygame import mixer
import os

# after import initilize methods(Good practice)
pygame.init()
# initilizies a screen takes tuple (width,height)
width_of_screen = 800
height_of_screen = 800
screen = pygame.display.set_mode((800, 800))
# screen is created but immediately closes, need to use an infinite for loop to maintain it until the screen is closed(base condition)
screen_open = True
# setting title of pygame window
pygame.display.set_caption("Space Invaders")

# setting the logo of the pygame window
alien_logo_file = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader",
                               "images/alien logo.png")
alien_logo = pygame.image.load(alien_logo_file)
pygame.display.set_icon(alien_logo)
# Creating player
player_img_file = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader", "images/robot.png")
player_img = pygame.image.load(player_img_file)
# background, is a normal image that most constantly be loaded
background_file = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader",
                               "images/space background.jpg")
background = pygame.image.load(background_file)
# Level variable each level the aliens get faster and background changes
# since the image is 62 bits and we want it in the middle of screen we place it at (370,480)
player_x = 370
player_y = 680
x_change = 0
y_change = 0
score_val = 0
game_ended = False
# background music
background_music_file = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader",
                                     "sounds/background.wav")
background_music = pygame.mixer.Sound(background_music_file)
background_music.set_volume(0.02)
background_music.play(-1)
# create score font
score_font = pygame.font.SysFont("comicsansms",16)
score_pos_x = 10
score_pos_y = 10
# creating enemies
# reading file with enemy picture names
enemies = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader", "enemy.txt")
file_reader = open(enemies, "r")
list_of_enemies = file_reader.readlines()
num_of_enemies = 6
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = [4] * num_of_enemies
enemy_y_change = [40] * num_of_enemies
# +1 since one line shows the level that the enemies are located at
# each enemy has img, (x,y) and change in x y these values are not shared
for i in range(num_of_enemies + 1):
    list_of_enemies[i] = list_of_enemies[i].rstrip("\n")
    if list_of_enemies[i] == "Level 1:":
        continue
    enemy_path = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader\\images", list_of_enemies[i])
    enemy_img.append(pygame.image.load(enemy_path))
    enemy_x.append(random.randint(0, 800))
    enemy_y.append(random.randint(0, 50))

# creating bullet
bullet_file = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader", "images/bullet.png")
bullet_img = pygame.image.load(bullet_file)
bullet_fired = False
bullet_y_start = player_y
bullet_x_start = player_x


def player(img, x, y):
    # Blit draws a surface on  another surface
    # takes second  parameter of coordinates(as a tuple) where to draw the surface
    screen.blit(img, (x, y))


def display_Font():
    score = score_font.render("Score: " + str(score_val), True, (255, 0, 0))
    screen.blit(score, (score_pos_x, score_pos_y))


def collision(bullet_x, bullet_y, enm_x, enm_y):
    distance_between = math.sqrt(math.pow((enm_x - bullet_x), 2) + math.pow((enm_y - bullet_y), 2))
    return distance_between <= 64


def collision_detected(index):
    global score_val, bullet_fired, bullet_y_start, enemy_y, enemy_x
    bullet_y_start = player_y
    bullet_fired = False
    score_val += 1
    if score_val % 10 == 0:
        print("Level 2")
        enemy_x[index] = random.randint(0, 800)
        enemy_y[index] = random.randint(0, 50)
    enemy_x[index] = random.randint(0, 800)
    enemy_y[index] = random.randint(0, 50)


def game_over(i):
    if (enemy_y[i] - 32 <= player_y <= enemy_y[i] + 32) and (enemy_x[i] - 32 <= player_x <= enemy_x[i] + 32):
        return True
    else:
        return False


def ending_screen():
    global game_ended
    for i in range(num_of_enemies):
        enemy_y[i] = height_of_screen * 2
    game_over_font = pygame.font.SysFont("comicsansms",32)
    game_over_img = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_img, (400, 400))
    game_ended = True


while screen_open:
    # fills the screen created by pygame with RGB combination, black so that a new screen is created each time the
    # loop is run
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    # for loop used to check events
    for e in pygame.event.get():
        # closes screen when close button is hit
        if e.type == pygame.QUIT:
            screen_open = False

        # KeyDown means key has been pressed, KeyUp key has been released
        # e.type to compare event type to see if it is a key press or key release
        # e.key usd to see which key is pressed
        # Every iteration check for key pressed or not if still pressed increment the change accordingly

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                # Left key is pressed
                x_change = -7
            if e.key == pygame.K_RIGHT:
                # Right key is pressed
                x_change = 7
            if e.key == pygame.K_UP:
                y_change = -7
            if e.key == pygame.K_DOWN:
                y_change = 7
            if e.key == pygame.K_SPACE:
                '''print("readying bullet")
                '''
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                # either left or right key are released
                x_change = 0
            if e.key == pygame.K_DOWN or e.key == pygame.K_UP:
                y_change = 0
            if e.key == pygame.K_SPACE:
                bullet_fired = True
                # subtract by 40 such that the bullet is released from tip of image
                bullet_y_start = player_y - 40
                bullet_x_start = player_x
                # bullet sound
                bullet_sound_path = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader",
                                                 "sounds/laser.wav")
                bullet_sound = pygame.mixer.Sound(bullet_sound_path)
                bullet_sound.set_volume(0.03)
                bullet_sound.play()
    if (width_of_screen - 64) > (player_x + x_change) > 0:
        player_x += x_change
    if (height_of_screen - 64) > (player_y + y_change) > 0:
        player_y += y_change
    # 64 are the width and length of the image used
    # need to add elif statements such that the enemy continues moving in the opposite directions
    for i in range(num_of_enemies):
        if game_over(i) or game_ended:
            ending_screen()
        if (enemy_x[i] + enemy_x_change[i]) < 0:
            enemy_x_change[i] = 3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] > (width_of_screen - 64):
            enemy_x_change[i] = -3
            enemy_y[i] += enemy_y_change[i]
        # check to see if bullet is fired and if it collides with any of the nemies
        if bullet_fired:
            screen.blit(bullet_img, (bullet_x_start, bullet_y_start))
            bullet_y_start -= 2
        if bullet_y_start < 0:
            bullet_fired = False
        # check if collision occurs before drawing enemy
        if collision(bullet_x_start, bullet_y_start, enemy_x[i], enemy_y[i]):
            # collision sound
            #mp3 file is causing an error, dont think this is supported
            '''
            enemy_death_sound_path = os.path.join("F:\\Users\\Mohamed\\PycharmProjects\\PyGameProjects\\SpaceInvader",
                                                  "ping_missing.mp3")
            pygame.mixer.music.load(enemy_death_sound_path)
            mixer.music.set_volume(0.05)
            mixer.music.play()
            '''
            # reset bullet and set fired to false since it hit the target and increase score
            # reset enemy coordinates
            collision_detected(i)
        enemy_x[i] += enemy_x_change[i]
        player(enemy_img[i], enemy_x[i], enemy_y[i])
    player(player_img, player_x, player_y)
    display_Font()
    pygame.display.update()
if not screen_open:
    print("Final score is " + str(score_val))
