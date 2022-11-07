import pygame
import math
import random

pygame.init()

# Game Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Background
background = pygame.image.load("./media/stars.png")

# Sound
pygame.mixer.music.load("./media/background.wav")
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound("./media/laser.wav")
bullet_sound_4 = pygame.mixer.Sound('./media/level_4/laser.mp3')
explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
explosion_sound_4 = pygame.mixer.Sound('./media/level_4/explosion.wav')
victory_sound = pygame.mixer.Sound('./media/victory_sound.mp3')

# Player
playerImg = pygame.image.load("./media/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5
num_enemies_lvl2 = 8
num_enemies_lvl3 = 12
num_enemies_lvl4 = 15

level2_start = True
level3_start = True
level4_start = True
end_game_bonus = True

# Bullet
bulletImg = pygame.image.load("./media/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score Board
score_value = 0
font = pygame.font.Font("./fonts/Square.ttf", 24)
textX = 10
textY = 10

# Game Over Text
# create the font for game over
game_over_font = pygame.font.Font("./fonts/Square.ttf", 128)
game_start_font = pygame.font.Font('./fonts/Square.ttf', 50)
game_end_font = pygame.font.Font('./fonts/Square.ttf', 50)
game_end_score = pygame.font.Font('./fonts/Square.ttf', 40)


def show_score(x, y):
    score = font.render("Score: "+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def isCollision_lvl2(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow((enemyX - 10)-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def isCollision_lvl3(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow((enemyX)-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def isCollision_lvl4(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow((enemyX - 30)-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def game_over():  # display the game over text
    over_font = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_font, (100, 250))


class GameState():

    def __init__(self):
        self.state = 'intro'

    def intro(self):
        global running
        global game_start_font
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'base_level'

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # start font
        start_font = game_start_font.render("START", True, (0, 255, 0))
        screen.blit(start_font, (330, 270))

        pygame.display.update()

    def base_level(self):
        global score_value
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global bullet_state
        global running
        global num_enemies

        for i in range(5):
            enemyImg.append(pygame.image.load("./media/ufo.png"))
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(2)
            enemyY_change.append(40)

       # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3

                if event.key == pygame.K_RIGHT:
                    playerX_change = 3

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = pygame.mixer.Sound("./media/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_enemies):

            # Game Over
            if enemyY[i] > 440:  # trigger the end of the game
                for j in range(num_enemies):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                #enemyX[i] = random.randint(0, 736)
                #enemyY[i] = random.randint(50, 150)
                del enemyX[i]
                del enemyY[i]
                num_enemies -= 1

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Animation
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    def level_2(self):
        global score_value
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global bullet_state
        global running
        global num_enemies_lvl2
        bulletX_lvl2 = bulletX+10

        for i in range(num_enemies_lvl2):
            enemyImg.append(pygame.image.load("./media/level_2/pinkufo.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(3)
            enemyY_change.append(40)

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3

                if event.key == pygame.K_RIGHT:
                    playerX_change = 3

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = pygame.mixer.Sound(
                            "./media/level_2/bulletshot.mp3")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_enemies_lvl2):

            # Game Over
            if enemyY[i] > 440:  # trigger the end of the game
                for j in range(num_enemies_lvl2):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            collision = isCollision_lvl2(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = pygame.mixer.Sound(
                    "./media/level_2/explosionsound.mp3")
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 2
                #enemyX[i] = random.randint(0, 736)
                #enemyY[i] = random.randint(50, 150)
                del enemyX[i]
                del enemyY[i]
                num_enemies_lvl2 -= 1

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Animation
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX_lvl2, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    def level_3(self):
        global score_value
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global bullet_state
        global running
        global num_enemies_lvl3
        bulletX_lvl3 = bulletX-45

        for i in range(num_enemies_lvl3):
            enemyImg.append(pygame.image.load(
                "./media/level_3/shipGreen_manned.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(4)
            enemyY_change.append(40)

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3

                if event.key == pygame.K_RIGHT:
                    playerX_change = 3

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = pygame.mixer.Sound(
                            "./media/level_3/shooting.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_enemies_lvl3):

            # Game Over
            if enemyY[i] > 440:  # trigger the end of the game
                for j in range(num_enemies_lvl3):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 8
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -8
                enemyY[i] += enemyY_change[i]

            collision = isCollision_lvl3(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = pygame.mixer.Sound(
                    "./media/level_3/explosion.wav")
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 3
                del enemyX[i]
                del enemyY[i]
                num_enemies_lvl3 -= 1

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Animation
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX_lvl3, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    def level_4(self):
        global score_value
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global bullet_state
        global running
        global num_enemies_lvl4
        global bullet_sound_4
        global explosion_sound_4

        for i in range(num_enemies_lvl4):
            enemyImg.append(pygame.image.load("./media/level_4/ufo.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(4)
            enemyY_change.append(40)

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3

                if event.key == pygame.K_RIGHT:
                    playerX_change = 3

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound_4.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_enemies_lvl4):

            # Game Over
            if enemyY[i] > 440:  # trigger the end of the game
                for j in range(num_enemies_lvl4):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 11
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -11
                enemyY[i] += enemyY_change[i]

            collision = isCollision_lvl4(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound_4.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 5
                del enemyX[i]
                del enemyY[i]
                num_enemies_lvl4 -= 1

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Animation
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    def win(self):
        global running
        global game_end_font
        global game_end_score
        global level2_start
        global level3_start
        global level4_start

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # end font
        end_font = game_end_font.render(
            "Congratulations, you win!!!", True, (0, 255, 0))
        screen.blit(end_font, (80, 270))
        end_score = game_end_score.render(
            'Your score: ' + str(score_value), True, (0, 255, 0))
        screen.blit(end_score, (250, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                level2_start = True
                level3_start = True
                level4_start = True
                self.state = 'intro'

    def state_manager(self):
        global score_value
        global background
        global playerImg
        global bulletImg
        global bullet_sound
        global explosion_sound
        global level2_start
        global level3_start
        global level4_start
        global victory_sound
        global bullet_sound_4
        global end_game_bonus

        if self.state == 'intro':
            self.intro()
        if self.state == 'base_level':
            self.base_level()
        if score_value >= 5 and score_value < 31:
            if score_value == 5:
                victory_sound.play()

            self.state = 'level_2'

            background = pygame.image.load("./media/level_2/background.jpg")
            playerImg = pygame.image.load("./media/level_2/spaceship.png")
            bulletImg = pygame.image.load("./media/level_2/bullet.png")

            if level2_start:
                score_value += 10
                pygame.mixer.Sound.stop(bullet_sound)
                pygame.mixer.Sound.stop(explosion_sound)
                pygame.mixer.music.stop()
                pygame.mixer.music.load("./media/level_2/backgroundmusic.mp3")
                pygame.mixer.music.play(-1)
                level2_start = False

            enemyImg.clear()
            self.level_2()
        if score_value >= 31 and score_value < 87:
            if score_value == 31:
                victory_sound.play()

            background = pygame.image.load("./media/level_3/background.jpg")
            playerImg = pygame.image.load("./media/level_3/spaceship.png")
            bulletImg = pygame.image.load("./media/level_3/bullet.png")

            if level3_start:
                score_value += 20
                pygame.mixer.Sound.stop(bullet_sound)
                pygame.mixer.Sound.stop(explosion_sound)
                pygame.mixer.music.stop()
                pygame.mixer.music.load("./media/level_3/background-music.wav")
                pygame.mixer.music.play(-1)
                level3_start = False

            self.state = 'level_3'
            enemyImg.clear()
            self.level_3()
        if score_value >= 87 and score_value < 192:
            if score_value == 87:
                victory_sound.play()

            playerImg = pygame.image.load("./media/level_4/spaceship.png")
            background = pygame.image.load("./media/level_4/stars.png")
            bulletImg = pygame.image.load("./media/level_4/bullet.png")
            #bullet_sound_4 = pygame.mixer.Sound("./media/level_4/laser.mp3")

            if level4_start:
                score_value += 30
                pygame.mixer.Sound.stop(bullet_sound)
                pygame.mixer.Sound.stop(explosion_sound)
                pygame.mixer.music.stop()
                pygame.mixer.music.load("./media/level_4/background_music.mp3")
                pygame.mixer.music.play(-1)
                level4_start = False

            self.state = 'level_4'
            enemyImg.clear()

            self.level_4()
        if score_value >= 192:
            if end_game_bonus == True:
                score_value += 58
                end_game_bonus = False

            pygame.mixer.Sound.stop(bullet_sound)
            pygame.mixer.Sound.stop(explosion_sound)
            self.win()


game_state = GameState()

# Game Loop
running = True
while running:
    game_state.state_manager()
    pygame.display.update()
    clock.tick(60)
