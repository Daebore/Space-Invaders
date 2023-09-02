import pygame
import random
import math
from pygame import mixer

# Start the game
pygame.init()

# Screen's size configuration
screen = pygame.display.set_mode((800, 600))

# Title, icon and background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)
background = pygame.image.load("space.jpg")

# Music
mixer.music.load("starfox.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Player's variables
img_player = pygame.image.load("cuterocket.png")
player_x = 368
player_y = 500
player_x_np = 0

# Enemies's variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_np = []
enemy_y_np = []
number_of_enemies = 8

for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 100))
    enemy_x_np.append(0.3)
    enemy_y_np.append(50)

# Bullets' variables
img_bullet= pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 500
bullet_x_np = 0
bullet_y_np = 0.65
bullet_vision = False

# Score variables
score = 0
font_family = pygame.font.Font("bubblecute.ttf", 32)
text_x = 10
text_y = 10


# Game Over function
final_text = pygame.font.Font("bubblecute.ttf", 40)


# When an enemy reach the player's location, the game is over and the final score is shown
def game_over():
    my_final_text = final_text.render("GAME OVER", True, (255, 255, 255))
    my_final_text2 = final_text.render(f"Your Score: {score}", True, (255, 255, 255))
    screen.blit(my_final_text, (300, 320))
    screen.blit(my_final_text2, (300, 370))


# Show score function
def show_score(x, y):
    text = font_family.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


# This function creates the player
def player(x, y):
    screen.blit(img_player, (x, y))


# This function creates the enemies
def enemy(x, y, enemy):
    screen.blit(img_enemy[enemy], (x, y))


# This function allows the player to shoot
def shoot_bullets(x, y):
    global bullet_vision
    bullet_vision = True
    screen.blit(img_bullet, (x + 16, y + 10))


# Colliders function
def collider_finder(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False


# Loop which controls the game
playing = True
while playing:

    # Screen's background configuration
    screen.blit(background, (0, 0))

    # If the player is playing the game, he enters a non-stop loop, which can be broken if the player decide to stop
    # playing by pressing the x buttom
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        # Control of the characters possition by using <- -> keys or space key
        if event.type == pygame.KEYDOWN:
            # To move left
            if event.key == pygame.K_LEFT:
                player_x_np -= 0.3
            # To move right
            if event.key == pygame.K_RIGHT:
                player_x_np += 0.3
            # To shoot
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("starwars.mp3")
                bullet_sound.play()
                if not bullet_vision:
                    bullet_x = player_x
                    shoot_bullets(bullet_x, bullet_y)

        # To reset player_x_np variable to 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_np = 0

    # Update the player's possition
    player_x += player_x_np

    # To make sure the spaceship does not go away
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Update the enemies' possition
    for i in range(number_of_enemies):
        # Game Over
        if enemy_y[i] > 445:
            for e in range(number_of_enemies):
                enemy_y[e] = 999
            game_over()
            break

        enemy_x[i] += enemy_x_np[i]

        # To make sure the enemies do not go away
        if enemy_x[i] <= 0:
            enemy_x_np[i] = 0.3
            enemy_y[i] += enemy_y_np[i]
        elif enemy_x[i] >= 736:
            enemy_x_np[i] = -0.3
            enemy_y[i] += enemy_y_np[i]

        # To check if there is a collision
        collision = collider_finder(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            hit_sound = mixer.Sound("hit.mp3")
            hit_sound.play()
            bullet_y = 500
            bullet_vision = False
            score += 1
            enemy_x[i] = (random.randint(0, 736))
            enemy_y[i] = (random.randint(50, 100))

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullets' movement
    if bullet_y <= -64:
        bullet_y = 500
        bullet_vision = False
    if bullet_vision:
        shoot_bullets(bullet_x, bullet_y)
        bullet_y -= bullet_y_np

    player(player_x, player_y)

    show_score(text_x, text_y)

    # After changing someting in the screen, it is neccessary to update the display
    pygame.display.update()

