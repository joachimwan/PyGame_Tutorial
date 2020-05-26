# change all the codes to first check if there's enemy using len(Enemy.enemies)==0
# code AI to control enemies

# make MP bar and charge bar
# code shoot animation

# code drop item and item interaction

# create stage selection page
# create volume button
# fix restart button

# code staircase steps <-------------

import pygame
import numpy as np

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()

# check if current working directory contains required images
try:
    # %matplotlib inline
    import matplotlib.pyplot as plt
    import os

    print("current working directory: ", os.getcwd())
    img = plt.imread('R1.png')
    # plt.imshow(img)
    # plt.imshow(img[15:40, 15:45, 0:4])
    # print(img)
except OSError:
    # change current working directory to folder containing all images
    if os.path.exists("/Users/JoachimWHY/PycharmProjects/TestProjects/PyGame Tutorial"):
        os.chdir("/Users/JoachimWHY/PycharmProjects/TestProjects/PyGame Tutorial")
    print("current working directory: ", os.getcwd())
    img = plt.imread('R1.png')
    # else use ('PyGame Tutorial/R1.png') or (os.path.join('PyGame Tutorial', 'R1.png'))
finally:
    del img

# load music file and play
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# load sound effect files, must be .wav
bullet_sound = pygame.mixer.Sound('bullet.wav')
bullet_sound.set_volume(0.1)
hit_sound = pygame.mixer.Sound('hit.wav')
hit_sound.set_volume(0.1)

# load background image from current working directory
bg = pygame.image.load('bg.jpg')

# define the surface
surf_width = 850
surf_height = 480
window = pygame.display.set_mode(size=(surf_width, surf_height))  # width x height of surface
pygame.display.set_caption("First Game")


class Player:
    # load images for animation from current working directory
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'),
                 pygame.image.load('R3.png'), pygame.image.load('R4.png'),
                 pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'),
                 pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'),
                pygame.image.load('L3.png'), pygame.image.load('L4.png'),
                pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'),
                pygame.image.load('L9.png')]
    standing = pygame.image.load('standing.png')

    def __init__(self, x=50, y=200, width=64, height=64):
        # define the Player character
        self.x = x  # starting point x-coordinate
        self.y = y  # starting point y-coordinate
        self.width = width
        self.height = height
        self.vel = 6
        self.bounding_box = (self.x + 12, self.y + 12, 40, 55)
        self.color = (0, 0, 255)
        self.hit = False
        self.delayCount = 0
        self.HP0 = 100
        self.HP = self.HP0
        self.score = 0

        # to code shooting delay
        self.shootCount = 0

        # to code jumping action
        self.isJump = False
        self.jumpCount0 = 11
        self.jumpCount = self.jumpCount0

        # to code animation
        self.left = False
        self.right = False
        self.walkCount = 0
    
    def update_bounding_box(self):
        self.bounding_box = (self.x + 12, self.y + 12, 40, 55)

    def draw(self, window):
        # use same image for 3 frames, then reset to first image
        if self.walkCount >= np.size(self.walkRight) * 3:
            self.walkCount = 0

        # define which image to draw at which count
        if self.left:
            window.blit(self.walkLeft[self.walkCount // 3], [self.x, self.y])
            if keys[pygame.K_LEFT] and not game_over:
                self.walkCount += 1
        elif self.right:
            window.blit(self.walkRight[self.walkCount // 3], [self.x, self.y])
            if keys[pygame.K_RIGHT] and not game_over:
                self.walkCount += 1
        else:
            window.blit(self.standing, [self.x, self.y])

        # define delay for hit
        if 0 < self.delayCount <= 10:
            self.delayCount += 1
        else:
            self.hit = False
            self.delayCount = 0

        # change color of bounding box
        if self.hit:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 255)

        self.update_bounding_box()
        pygame.draw.rect(window, self.color, self.bounding_box, 2)

        # draw HP bar above player
        pygame.draw.rect(window, (255, 255, 0),
                         (int(self.x - 0.5 * (self.HP0 - self.width)), int(self.bounding_box[1]) - 10, max(0, self.HP),
                          8), 0)
        pygame.draw.rect(window, (0, 0, 0),
                         (int(self.x - 0.5 * (self.HP0 - self.width)), int(self.bounding_box[1]) - 10, self.HP0, 8), 2)

    def hit_action(self):
        if self.hit is False:
            self.HP -= 10
            hit_sound.play()
            self.hit = True
            self.delayCount = 1

    def check_collision(self, box):
        if box.bounding_box[0] < self.bounding_box[0] + self.bounding_box[2] and self.bounding_box[0] < \
                box.bounding_box[0] + box.bounding_box[2]:
            if box.bounding_box[1] < self.bounding_box[1] + self.bounding_box[3] and self.bounding_box[1] < \
                    box.bounding_box[1] + box.bounding_box[3]:
                return True


class Enemy:
    enemies = []

    # load images for animation from current working directory
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),
                 pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
                 pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
                 pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),
                 pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),
                pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
                pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),
                pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),
                pygame.image.load('L11E.png')]

    def __init__(self, x=100, y=355, width=64, height=64):
        # define the Player character
        self.x = x  # starting point x-coordinate
        self.y = y  # starting point y-coordinate
        self.width = width
        self.height = height
        self.vel = 3
        self.bounding_box = (self.x + 10, self.y, 50, 60)
        self.color = (0, 0, 255)
        self.hit = False
        self.delayCount = 0
        self.HP0 = 100
        self.HP = self.HP0
        self.enemies.append(self)

        # to code jumping action
        self.isJump = False
        self.jumpCount0 = 11
        self.jumpCount = self.jumpCount0

        # to code animation
        self.ctrl = {"up": False, "down": False, "left": False, "right": False, "A": False, "B": False}
        self.left = False
        self.right = True
        self.walkCount = 0
        
    def update_bounding_box(self):
        self.bounding_box = (self.x + 10, self.y, 50, 60)

    def draw(self, window):
        # automatically move the enemy
        self.move()

        # use same image for 3 frames, then reset to first image
        if self.walkCount >= np.size(self.walkRight) * 3:
            self.walkCount = 0

        # define which image to draw at which count
        if self.left:
            window.blit(self.walkLeft[self.walkCount // 3], [self.x, self.y])
            if self.ctrl["left"]:
                self.walkCount += 1
        elif self.right:
            window.blit(self.walkRight[self.walkCount // 3], [self.x, self.y])
            if self.ctrl["right"]:
                self.walkCount += 1

        # define delay for hit
        if 0 < self.delayCount <= 6:
            self.delayCount += 1
        else:
            self.hit = False
            self.delayCount = 0

        # change color of bounding box
        if self.hit:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 255)

        self.update_bounding_box()
        pygame.draw.rect(window, self.color, self.bounding_box, 2)

        # draw HP bar above enemy
        pygame.draw.rect(window, (255, 0, 0),
                         (int(self.x - 0.5 * (self.HP0 - self.width)), int(self.bounding_box[1]) - 10, max(0, self.HP),
                          8), 0)
        pygame.draw.rect(window, (0, 0, 0),
                         (int(self.x - 0.5 * (self.HP0 - self.width)), int(self.bounding_box[1]) - 10, self.HP0, 8), 2)

    # program to control the enemy
    def move(self):
        # re-initialize all controls
        self.ctrl = {"up": False, "down": False, "left": False, "right": False, "A": False, "B": False}

        # to be replaced with AI that will decide enemy.ctrl
        if self.HP > 0:
            if self.walkCount//np.random.randint(1, 3) == 0:  # randomly jump
                self.ctrl["up"] = True
            if self.left:
                if self.x - self.vel >= 0:
                    self.ctrl["left"] = True
                else:
                    self.ctrl["right"] = True
            elif self.right:
                if self.x + self.width + self.vel <= surf_width:
                    self.ctrl["right"] = True
                else:
                    self.ctrl["left"] = True

        # define what happens when click left or click right
        if self.ctrl["left"] and self.x - self.vel >= 0:
            self.x -= self.vel
            self.left = True
            self.right = False
        elif self.ctrl["right"] & (self.x + self.width + self.vel <= surf_width):
            self.x += self.vel
            self.right = True
            self.left = False

        if not self.isJump:
            # check if player is on an obstruction
            rel_pos = []
            for box in Obstruction.boxes:
                box.check_position(self)
                rel_pos.append(box.rel_pos)
            if min(rel_pos) > 0:
                self.jumpCount = -3  # set to falling
                self.isJump = True

            if self.ctrl["up"] & (self.y + self.height + self.vel <= surf_height):
                self.isJump = True
        else:
            if self.jumpCount >= 0:  # jumpCount is num of frames jumping
                up = 1
            else:  # player.jumpCount < 0
                up = -1

            distance = int(0.20 * self.jumpCount ** 2 * up)  # constant is jump height / num of frames
            self.y -= distance
            self.update_bounding_box()
            if self.jumpCount < 0:
                box_distance = []
                for box in Obstruction.boxes:
                    box.check_position(self)
                    if box.rel_pos == 4:
                        box_distance.append(
                            box.bounding_box[1] - (self.bounding_box[1] + self.bounding_box[3] + distance))
                box_distance2 = []
                for dist in box_distance:
                    if dist >= 0:
                        box_distance2.append(dist)
                if len(box_distance2) != 0:
                    self.y += distance
                    self.y += min(box_distance2)
                    self.update_bounding_box()
                    self.isJump = False
                    self.jumpCount = self.jumpCount0
            self.jumpCount -= 1

    def hit_action(self):
        if self.hit is False and self.HP >= 0:
            self.HP -= 20
            hit_sound.play()
            self.hit = True
            self.delayCount = 1


class Projectile:
    bullets = []

    def __init__(self, x, y, facing, radius=5, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing[1] - facing[0]  # 1 for right or -1 for left
        self.vel = 12 * self.facing
        self.bullets.append(self)

    # check bullet collision with any bounding box
    def check_collision(self, box):
        if box[0] < self.x + self.radius and self.x - self.radius < box[0] + box[2]:
            if box[1] < self.y + self.radius and self.y - self.radius < box[1] + box[3]:
                return True

    def draw(self, window):
        pygame.draw.circle(window, self.color, [int(self.x), int(self.y)], self.radius)


class Obstruction:
    boxes = []

    def __init__(self, x, y, width, height=10, color=(193, 154, 107), transparent=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounding_box = (self.x, self.y, self.width, self.height)
        self.color = color
        self.boxes.append(self)
        self.rel_pos = 0  # relative position
        self.transparent = transparent
        
        # to code animation
        self.moveCount0 = 15
        self.moveCount = self.moveCount0
        
    def update_bounding_box(self):
        self.bounding_box = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.bounding_box, 0)

    def check_position(self, player):
        if self.bounding_box[0] + self.bounding_box[2] <= player.bounding_box[0]:
            self.rel_pos = 2  # box is left of player
        elif player.bounding_box[0] + player.bounding_box[2] <= self.bounding_box[0]:
            self.rel_pos = 1  # box is right of player
        elif self.bounding_box[1] < player.bounding_box[1] + player.bounding_box[3]:
            self.rel_pos = 4  # top of box is above bottom of player
        elif player.bounding_box[1] + player.bounding_box[3] < self.bounding_box[1]:
            self.rel_pos = 3  # top of box is below bottom of player
        else:
            self.rel_pos = 0  # player is standing on this box


class Target:
    targets = []
    
    def __init__(self, x, y, radius=5, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.bounding_box = (self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)
        self.color = color
        self.targets.append(self)
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, [int(self.x), int(self.y)], self.radius)


def redraw_game_window():
    window.blit(bg, [0, 0])  # set background to image from [0, 0] position
    
    for box in Obstruction.boxes[1:]:  # draw boxes except ground
        if not box.transparent:
            box.draw(window)
    
    player.draw(window)  # draw player
    
    for enemy in Enemy.enemies:
        enemy.draw(window)  # draw enemy
    
    for bullet in Projectile.bullets:  # draw bullets
        bullet.draw(window)
        
    for target in Target.targets:  # draw target
        target.draw(window)
    
    font = pygame.font.SysFont(None, 30)  # create object with font style and font size
    text = font.render(str(mouse_position), True, (0, 0, 0))
    window.blit(text, [surf_width - text.get_width() - 5, surf_height - text.get_height() - 5])
    text = font.render("Score = " + str(player.score), True, (0, 0, 0))
    window.blit(text, [5, 5])
    text = font.render(str(timer), True, (0, 0, 0))
    window.blit(text, [int(surf_width/2 - text.get_width()/2), 5])
    text = font.render("Restart", True, (180, 50, 0))
    pygame.draw.rect(window, (180, 50, 0), (restart_button.x - 2, restart_button.y - 2,
                                            restart_button.width + 4, restart_button.height + 4), 2)
    window.blit(text, [restart_button.x, restart_button.y])
    
    pygame.draw.circle(window, (255, 0, 0), mouse_position, 2)  # draw mouse position
    
    if game_over:  # print this if game over
        pygame.draw.rect(window, (255, 255, 255), (80, 80, surf_width - 160, surf_height - 160))
        pygame.draw.rect(window, (0, 0, 0), (80, 80, surf_width - 160, surf_height - 160), 10)
        font = pygame.font.SysFont(None, 30)
        instruction = ["Intruction:",
                       "1. You lose health if get hit by enemies.",
                       "2. You kill enemy by shooting them.",
                       "3. Killing enemies will spawn new ones, and you gain +1 score.",
                       "4. Grab the big red dot to earn score too.",
                       "5. Game ends when timer counts down to 0, or player dies.",
                       "6. Click on 'Restart' to start playing!"]
        text = []
        for line in instruction:
            text.append(font.render(line, True, (0, 0, 0)))
        for line in range(len(text)):
            window.blit(text[line], [90, 90 + line*int(text[line].get_height())])
        font = pygame.font.SysFont(None, 100)
        text = font.render("Score = " + str(player.score), True, (0, 0, 0))
        window.blit(text, [int(surf_width/2 - text.get_width()/2), int(surf_height/2) + 20])
    
    pygame.display.update()


def init_main():
    Projectile.bullets = []
    Enemy.enemies = []
    
    start_time = pygame.time.get_ticks()  # initialize start time
    
    player = Player()  # initialize player
    for i in range(n_enemies):  # initialize enemy
        Enemy(np.random.randint(200, surf_width - 64), np.random.randint(int(surf_height/2), ground.y - 64))
    
    return player, start_time


# define stage obstructions
field = 1
if field == 1:  # JW's field
    ground = Obstruction(0, 415, surf_width, 30, transparent=True)
    # Obstruction(160, 70, 150, 20, color=(215, 215, 230))  # cloud 1
    cloud = Obstruction(320, 140, 90, 20, color=(255, 0, 255))  # cloud 2
    Obstruction(170, 180, 20, 235, color=(255, 125, 40))  # big tree trunk 2
    Obstruction(100, 180, 150, 50, color=(110, 200, 60))  # big tree leaves 2
    Obstruction(355, 235, 20, 180, color=(255, 125, 40))  # small tree trunk 1
    Obstruction(330, 235, 80, 20, color=(0, 175, 0))  # small tree leaves 1
    Obstruction(290, 255, 140, 20, color=(0, 150, 50))  # small tree leaves 2
    Obstruction(270, 275, 180, 20, color=(0, 120, 40))  # small tree leaves 3
    Obstruction(210, 345, 20, 70, color=(255, 125, 40))  # small tree trunk 4
    Obstruction(160, 345, 130, 35, color=(90, 150, 0))  # small tree leaves 4
    Obstruction(0, 110, 75, 305, color=(250, 220, 185))  # rock 0 left
    Obstruction(770, 170, 80, 245, color=(250, 220, 185))  # rock 0 right
    Obstruction(550, 230, 240, 185, color=(230, 200, 165))  # rock 1
    Obstruction(490, 300, 130, 115, color=(185, 120, 90))  # rock 2
    Obstruction(660, 100, 20, 315, color=(255, 125, 40))  # big tree trunk 2
    Obstruction(600, 100, 150, 80, color=(144, 238, 144))  # big tree leaves 1
    Obstruction(570, 360, 200, 55, color=(70, 70, 50))  # rock 3

if field == 2:  # JunLi's field
    ground = Obstruction(0, 415, surf_width, 30, transparent=True)
    Obstruction(0, 350, 150, 10)  # level 1
    Obstruction(250, 350, 350, 10)  # level 1
    Obstruction(700, 350, 150, 10)  # level 1
    Obstruction(100, 290, 350, 10)  # level 2
    Obstruction(550, 290, 200, 10)  # level 2
    Obstruction(0, 230, 330, 10)  # level 3
    Obstruction(430, 230, 220, 10)  # level 3
    Obstruction(750, 230, 100, 10)  # level 3
    Obstruction(0, 170, 150, 10)  # level 4
    Obstruction(250, 170, 250, 10)  # level 4
    Obstruction(600, 170, 150, 10)  # level 4
    Obstruction(150, 110, 550, 10)  # level 5
    Obstruction(440, 180, 50, 50, (130, 0, 20))  # box 1
    Obstruction(380, 360, 55, 55, (130, 0, 20))  # box 2
    

# Obstruction(460, 35, 100, 5, (255, 255, 255))
# Obstruction(610, 35, 30, 5, (255, 255, 255))

target = Target(750, 35)

# draw restart button
font = pygame.font.SysFont(None, 30)  # create object with font style and font size
text = font.render("Restart", True, (0, 0, 0))
restart_button = Obstruction(5, surf_height-25, int(text.get_width()), int(text.get_height()), (0, 0, 0), True)

# initialize player, enemies, and start time
n_enemies = 1
player, start_time = init_main()

clock = pygame.time.Clock()
timer = 120
game_over = True
run = True
while run:
    clock.tick(27)  # set frame per second to max 27 (9 images * 3 frame/image)
    
    # define state of keyboard buttons
    keys = pygame.key.get_pressed()

    # define state of mouse buttons and position
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    
    if restart_button.x <= mouse_position[0] <= restart_button.x + restart_button.width:
        if restart_button.y <= mouse_position[1] <= restart_button.y + restart_button.height:
            if mouse_buttons[0]:
                game_over = False
                player, start_time = init_main()
    
    if not game_over:
        timer = 120 - round((pygame.time.get_ticks() - start_time)/1000)  # define time past since init_main
    
    # define when to terminate loop, i.e. when click on CLOSE button (QUIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
    
    if field == 1:
        if cloud.moveCount == cloud.moveCount0:
            delta = 1
        elif cloud.moveCount == -1 * cloud.moveCount0:
            delta = -1
        if cloud.moveCount >= 0:  # moveCount is num of frames moving
            up = 1
        else:
            up = -1
        distance = int(0.04 * cloud.moveCount ** 2 * up)  # constant is jump height / num of frames
        cloud.check_position(player)
        if cloud.rel_pos == 0:
            player.y -= distance
            player.update_bounding_box()
        cloud.y -= distance
        cloud.update_bounding_box()
        cloud.moveCount -= delta
        
    
    # define what key-presses do, e.g. change x and y starting point
    if not game_over:
        if keys[pygame.K_LEFT] and player.x - player.vel >= 0:
            player.x -= player.vel
            player.left = True
            player.right = False
        elif (keys[pygame.K_RIGHT]) & (player.x + player.width + player.vel <= surf_width):
            player.x += player.vel
            player.right = True
            player.left = False
        elif keys[pygame.K_DOWN]:
            player.left = False
            player.right = False
            player.walkCount = 0

    if not player.isJump:
        # check if player is on an obstruction
        rel_pos = []
        for box in Obstruction.boxes:
            box.check_position(player)
            rel_pos.append(box.rel_pos)
        if min(rel_pos) > 0:
            player.jumpCount = -3  # set to falling
            player.isJump = True

        if (keys[pygame.K_UP]) & (player.y + player.height + player.vel <= surf_height) and not game_over:
            player.isJump = True
    else:
        if player.jumpCount >= 0:  # jumpCount is num of frames jumping
            up = 1
        else:  # player.jumpCount < 0
            up = -1

        distance = int(0.20 * player.jumpCount ** 2 * up)  # constant is jump height / num of frames
        player.y -= distance
        player.update_bounding_box()
        if player.jumpCount < 0:
            box_distance = []
            for box in Obstruction.boxes:
                box.check_position(player)
                if box.rel_pos == 4:
                    box_distance.append(
                        box.bounding_box[1] - (player.bounding_box[1] + player.bounding_box[3] + distance))
            box_distance2 = []
            for dist in box_distance:
                if dist >= 0:
                    box_distance2.append(dist)
            if len(box_distance2) != 0:
                player.y += distance
                player.y += min(box_distance2)
                player.update_bounding_box()
                player.isJump = False
                player.jumpCount = player.jumpCount0
        player.jumpCount -= 1

    # define what key-presses do to bullets, i.e. change x and y starting point
    if keys[pygame.K_SPACE] and (player.left or player.right) and player.shootCount == 0 and not game_over:
        Projectile(player.x + (0.5 + (player.right - player.left) / 5) * player.width,
                   player.y + player.height / 2, [player.left, player.right])
        player.shootCount += 1
        bullet_sound.play()

    # define shooting delay
    if 0 < player.shootCount <= 10:
        player.shootCount += 1
    else:
        player.shootCount = 0

    # check if bullet hits enemy
    if len(Enemy.enemies) != 0:
        for enemy in Enemy.enemies:
            for bullet in Projectile.bullets:
                if bullet.check_collision(enemy.bounding_box):
                    Projectile.bullets.pop(Projectile.bullets.index(bullet))
                    enemy.hit_action()
                elif 0 < bullet.x < surf_width:
                    bullet.x += bullet.vel/len(Enemy.enemies)
                else:
                    Projectile.bullets.pop(Projectile.bullets.index(bullet))
    else:
        for bullet in Projectile.bullets:
            if 0 < bullet.x < surf_width:
                bullet.x += bullet.vel
            else:
                Projectile.bullets.pop(Projectile.bullets.index(bullet))

    # check if player collides with enemy
    for enemy in Enemy.enemies:
        if player.check_collision(enemy):
            player.hit_action()
    
    # remove dead enemies and create new enemies
    for enemy in Enemy.enemies:
        if enemy.HP <= 0 and enemy.delayCount == 0:
            Enemy.enemies.pop(Enemy.enemies.index(enemy))
            player.score += 1
            Enemy(np.random.randint(200, surf_width - 64), np.random.randint(int(surf_height / 3), ground.y - 64))
            Enemy(np.random.randint(200, surf_width - 64), np.random.randint(int(surf_height / 3), ground.y - 64))
    
    # condition to game over: player die, or time's up
    if player.HP <= 0 or timer <= 0:
        game_over = True
    
    for target in Target.targets:
        if player.check_collision(target):
            Target.targets.pop(Target.targets.index(target))
            player.score += 1
            target = Target(x=np.random.randint(100, surf_width-100), y=np.random.randint(100, surf_height-100))
    
    redraw_game_window()
    

pygame.display.quit()
pygame.quit()
