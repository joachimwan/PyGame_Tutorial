# change the score to something else

# make a list of enemies in class Enemy, append all instances of Enemy class
# change all the codes to first check if there's enemy using len(Enemy.enemies)==0
# then loop using for enemy in Enemy.enemies:
# change enemy movement to be based on enemy.controls eg left right jump shoot to code AI

# make MP bar and charge bar
# code shoot animation

# create menu page: use mouse to make obstructions
# show timer
# create volume button

# create you win or you lose page, restart game or terminate

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
    
    def __init__(self, x=50, y=0, width=64, height=64):
        # define the Player character
        self.x = x  # starting point x-coordinate
        self.y = y  # starting point y-coordinate
        self.width = width
        self.height = height
        self.vel = 5
        self.bounding_box = (self.x+12, self.y+12, 40, 55)
        self.color = (0, 0, 255)
        self.hit = False
        self.delayCount = 0
        self.HP0 = 100
        self.HP = self.HP0
        
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
        
    def draw(self, window):
        # use same image for 3 frames, then reset to first image
        if self.walkCount >= np.size(self.walkRight)*3:
            self.walkCount = 0
        
        # define which image to draw at which count
        if self.left:
            window.blit(self.walkLeft[self.walkCount//3], [self.x, self.y])
            if keys[pygame.K_LEFT]:
                self.walkCount += 1
        elif self.right:
            window.blit(self.walkRight[self.walkCount//3], [self.x, self.y])
            if keys[pygame.K_RIGHT]:
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
            
        self.bounding_box = (self.x+12, self.y+12, 40, 55)
        pygame.draw.rect(window, self.color, self.bounding_box, 2)
        
        # draw HP bar above player
        pygame.draw.rect(window, (255, 255, 0),
                         (int(self.x-0.5*(self.HP0-self.width)), int(self.bounding_box[1])-10, max(0, self.HP), 8), 0)
        pygame.draw.rect(window, (0, 0, 0),
                         (int(self.x-0.5*(self.HP0-self.width)), int(self.bounding_box[1])-10, self.HP0, 8), 2)
        
    def hit_action(self):
        self.hit = True
        self.delayCount = 1
        self.HP -= 10
        hit_sound.play()
    
    def check_collision(self, box):
        if box.bounding_box[0] < self.bounding_box[0] + self.bounding_box[2] and self.bounding_box[0] < box.bounding_box[0] + box.bounding_box[2]:
            if box.bounding_box[1] < self.bounding_box[1] + self.bounding_box[3] and self.bounding_box[1] < box.bounding_box[1] + box.bounding_box[3]:
                if box.bounding_box[1] < self.y + 12 + 55:  # solves tuple assignment bug
                    return True


class Enemy:
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
    
    def __init__(self, x=100, y=355, width=64, height=64, x_range=500):
        # define the Player character
        self.x = x  # starting point x-coordinate
        self.y = y  # starting point y-coordinate
        self.width = width
        self.height = height
        self.vel = 3
        self.bounding_box = (self.x+10, self.y, 50, 60)
        self.color = (0, 0, 255)
        self.hit = False
        self.delayCount = 0
        self.HP0 = 100
        self.HP = self.HP0
        
        # to code animation
        self.left = False
        self.right = True
        self.walkCount = 0
        self.path = [x, x+x_range]
        
    def draw(self, window):
        # automatically move the enemy
        self.move()
        
        # use same image for 3 frames, then reset to first image
        if self.walkCount >= np.size(self.walkRight)*3:
            self.walkCount = 0
        
        # define which image to draw at which count
        if self.left:
            window.blit(self.walkLeft[self.walkCount//3], [self.x, self.y])
            # self.walkCount += 1
        elif self.right:
            window.blit(self.walkRight[self.walkCount//3], [self.x, self.y])
            # self.walkCount += 1
        
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
        
        self.bounding_box = (self.x+10, self.y, 50, 60)
        pygame.draw.rect(window, self.color, self.bounding_box, 2)
        
        # draw HP bar above enemy
        pygame.draw.rect(window, (255, 0, 0),
                         (int(self.x-0.5*(self.HP0-self.width)), int(self.bounding_box[1])-10, max(0, self.HP), 8), 0)
        pygame.draw.rect(window, (0, 0, 0),
                         (int(self.x-0.5*(self.HP0-self.width)), int(self.bounding_box[1])-10, self.HP0, 8), 2)
        
    def move(self):
        self.walkCount += 1
        if self.left:
            if self.x - self.vel >= self.path[0]:
                self.x -= self.vel
            else:
                self.left = False
                self.right = True
        elif self.right:
            if self.x + self.width + self.vel <= self.path[1]:
                self.x += self.vel
            else:
                self.right = False
                self.left = True
    
    def hit_action(self):
        if self.hit is False:
            self.HP -= 10
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
        self.vel = 8*self.facing
        bullet_sound.play()
    
    # check bullet collision with any bounding box
    def check_collision(self, box):
        if box[0] < self.x + self.radius and self.x - self.radius < box[0] + box[2]:
            if box[1] < self.y + self.radius and self.y - self.radius < box[1] + box[3]:
                return True
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, [int(self.x), int(self.y)], self.radius)


class Obstruction:
    boxes = []
    
    def __init__(self, x, y, width, height, color=(255, 180, 0), transparent=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounding_box = (self.x, self.y, self.width, self.height)
        self.color = color
        self.boxes.append(self)
        self.rel_pos = 0  # relative position
        self.transparent = transparent
    
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


def redraw_game_window():
    window.blit(bg, [0, 0])  # set background to image from [0, 0] position
    for box in Obstruction.boxes[1:]:  # draw boxes except ground
        if not box.transparent:
            box.draw(window)
    player.draw(window)  # draw player
    enemy.draw(window)  # draw enemy
    pygame.draw.circle(window, (255, 0, 0), mouse_position, 2)  # draw mouse position
    for bullet in Projectile.bullets:  # draw bullets
        bullet.draw(window)
    text = font.render(str(mouse_position) + " You win = " + str(player.check_collision(target)) + ". Reach the red dot!!", True, (0, 0, 0))  # todo change to show something else later
    window.blit(text, [surf_width - text.get_width() - 5, 5])  # draw scoreboard
    pygame.display.update()


# main loop
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)  # create object with font style and font size
player = Player()  # initialize player
enemy = Enemy()  # initialize enemy
ground = Obstruction(0, 415, surf_width, 30, (0, 0, 0), True)

box1 = Obstruction(380, 350, 70, 65, (255, 255, 0))

Obstruction(280, 285, 100, 20, (100, 255, 100))
Obstruction(280, 210, 80, 20, (255, 50, 50))
Obstruction(170, 135, 60, 10, (0, 0, 0), True)
Obstruction(280, 80, 500, 5, (255, 180, 180))

Obstruction(460, 285, 100, 5, (255, 0, 255))
Obstruction(610, 285, 30, 5, (255, 0, 255))

Obstruction(460, 220, 60, 20, (180, 125, 255))
Obstruction(520, 210, 60, 20, (125, 0, 255))
Obstruction(580, 200, 60, 20, (0, 180, 255))
Obstruction(640, 190, 60, 20, (180, 125, 255))

target = Obstruction(750, 35, 10, 10, (255, 0, 0))

run = True
while run:
    clock.tick(27)  # set frame per second to max 27 (9 images * 3 frame/image)
    
    # define state of keyboard buttons
    keys = pygame.key.get_pressed()
    
    # define state of mouse buttons and position
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()

    # define when to terminate loop, i.e. when click on CLOSE button (QUIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
    
    # update relative position of all obstructions
    for box in Obstruction.boxes:
        box.check_position(player)

    # define what key-presses do, e.g. change x and y starting point
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
            rel_pos.append(box.rel_pos)
        if min(rel_pos) > 0:
            player.jumpCount = -3  # set to falling
            player.isJump = True
        
        if (keys[pygame.K_UP]) & (player.y + player.height + player.vel <= surf_height):
            player.isJump = True
    else:
        if player.jumpCount >= 0:  # jumpCount is num of frames jumping
            up = 1
        else:  # player.jumpCount < 0
            up = -1
        
        distance = 0.20 * player.jumpCount ** 2 * up  # constant is jump height / num of frames
        player.y -= distance
        player.bounding_box = (player.x+12, player.y+12, 40, 55)
        if player.jumpCount < 0:
            box_distance = []
            for box in Obstruction.boxes:
                box.check_position(player)
                if box.rel_pos == 4:
                    box_distance.append(box.bounding_box[1] - (player.bounding_box[1] + player.bounding_box[3] + distance))
            box_distance2 = []
            for dist in box_distance:
                if dist >= 0:
                    box_distance2.append(dist)
            if len(box_distance2) != 0:
                player.y += distance
                player.y += min(box_distance2)
                player.isJump = False
                player.jumpCount = player.jumpCount0
        player.jumpCount -= 1

    # define what key-presses do to bullets, i.e. change x and y starting point
    if keys[pygame.K_SPACE] and (player.left or player.right) and player.shootCount == 0:
        Projectile.bullets.append(Projectile(player.x + (0.5 + (player.right - player.left)/5)*player.width,
                                  player.y + player.height/2,
                                  [player.left, player.right]))
        player.shootCount += 1

    for bullet in Projectile.bullets:
        # check if bullet hits enemy
        if bullet.check_collision(enemy.bounding_box):
            Projectile.bullets.pop(Projectile.bullets.index(bullet))
            if enemy.hit is False:
                enemy.hit_action()
        
        elif 0 < bullet.x < surf_width:
            bullet.x += bullet.vel
        else:
            Projectile.bullets.pop(Projectile.bullets.index(bullet))
    
    # check if player collides with enemy
    if player.check_collision(enemy) and player.hit is False:
        player.hit_action()
    
    # define shooting delay
    if 0 < player.shootCount <= 10:
        player.shootCount += 1
    else:
        player.shootCount = 0
    
    redraw_game_window()
pygame.quit()
