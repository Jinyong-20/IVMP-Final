import pygame
import numpy as np
import random
from os import path

FPS = 60   # frames per second

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = WINDOW_WIDTH/12*9

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
font_dir = path.join(path.dirname(__file__), 'font')


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Boss Challenger")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

def show_clear_screen():
    screen.blit(clearScreen, clearScreen_rect)
    draw_text(screen, "Congratulation!", 48, WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100, WHITE)
    draw_text(screen, "Press any key to Title", 24, WINDOW_WIDTH / 2, WINDOW_HEIGHT/2 + 315, BLACK)
    clear_sound.play()
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_gameover_screen():
    screen.blit(gameoverScreen, gameoverScreen_rect)
    draw_text(screen, "You Died.", 48, WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100, RED)
    draw_text(screen, "Press any key to Title", 24, WINDOW_WIDTH / 2, WINDOW_HEIGHT/2 + 315, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_go_screen():
    screen.blit(startScreen, startScreen_rect)
    draw_text(screen, "< How to Play >", 22, 200, 275, BLACK)
    draw_text(screen, ": move", 18, 185, 340, BLACK)
    draw_text(screen, ": tumble", 18, 190, 390, BLACK)
    draw_text(screen, ": shoot bullet", 18, 210, 430, BLACK)
    draw_text(screen, ": knife attack", 18, 205, 470, BLACK)
    draw_text(screen, ": need bullet for shoot", 18, 240, 520, BLACK)
    draw_text(screen, ": box to refill bullet", 18, 230, 560, BLACK)
    draw_text(screen, "Press Any Key to Start", 24, WINDOW_WIDTH / 2, WINDOW_HEIGHT/2 + 315, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(path.join(font_dir, 'goudyo.ttf'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class BulletBox(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(box_img, (50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class FixIcon(pygame.sprite.Sprite) :
    def __init__(self, x,y, time, staytime):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fix_img, (30,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.createtime = time
        self.staytime = staytime
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.createtime > self.staytime:
            print("이미지 삭제!")
            self.kill()

class gunIcon(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gun_img, (24,16))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class Boss(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Boss_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WINDOW_WIDTH/2#random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.centery = WINDOW_HEIGHT/2 #random.randrange(WINDOW_HEIGHT - self.rect.height)
        self.shootPosx = self.rect.centerx-45
        self.shootPosy = self.rect.centery-95
        self.atk1_delay = 1000
        self.atk2_delay = 1000
        self.attack_delay = 1000
        self.skill_delay = 3000
        self.overheat_delay = 30000
        self.last_atk1 = pygame.time.get_ticks()
        self.last_skill = pygame.time.get_ticks()
        self.last_atk2 = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.last_overheat = pygame.time.get_ticks()
        self.atkCount = 0
        self.atk1cond = False
        self.atk2cond = False
        self.skillcond = False
        self.atk2targetPos = (0,0)
        self.atk1targetPos = (0,0)
        self.box_delay = 7000
        self.last_box = pygame.time.get_ticks()
        self.hp = 100
        self.overheat = False
        self.overheat_term = 5000

    def update(self):
        if boss.hp <= 0 :
            print("보스 컷")
            self.kill()
            
        availableatk = []
        now = pygame.time.get_ticks()
        if now - self.last_box > self.box_delay :
            print("빡스")
            self.box()
        if now - self.last_overheat > self.overheat_delay :
            self.overheat = True 
            self.broken()
            print("과열")

        if self.overheat :
            if now - self.last_overheat > self.overheat_term :
                self.overheat = False
                print("수리완료")

        if self.overheat == False :
            if self.atk1cond:
                if now - self.last_atk1 > self.atk1_delay :
                    print("패퉌")
                    self.attack1()
            elif self.atk2cond:
                if now - self.last_atk2 > self.atk2_delay :
                    self.attack2()
            elif self.skillcond :
                if now - self.last_skill > self.skill_delay :
                    self.skill()
            else : #patterns are not going on
                if now - self.last_attack > self.attack_delay :
                    if now - self.last_atk1 > self.atk1_delay : #atkavailable
                        availableatk.append(0)
                    if now - self.last_atk2 > self.atk2_delay : #atkavailable
                        availableatk.append(1)
                if now - self.last_skill > self.skill_delay : #skillavailable
                    availableatk.append(2)
                if len(availableatk) > 0 : 
                    cond = availableatk[random.randrange(0,len(availableatk))]
                    print(cond)
                    if cond == 0 :
                        self.atk1targetPos = (playerPos[0], playerPos[1])
                        self.attack1()
                        self.atk1cond = True
                    elif cond == 1 :
                        self.atk2targetPos = (playerPos[0], playerPos[1])
                        self.attack2()
                        print("위치지정")
                        self.atk2cond = True
                    elif cond == 2 :
                        self.skill()
                        self.skillcond = True

    def box(self):     
        targetPointx = random.randrange(self.rect.width + 50, WINDOW_WIDTH - self.rect.width -50)
        targetPointy = random.randrange(self.rect.height + 50, WINDOW_HEIGHT - self.rect.height -50)
        now = pygame.time.get_ticks()
        self.last_box = now
        box = BulletBox(targetPointx, targetPointy)
        all_sprites.add(box)
        boxes.add(box)
        boxcreate_sound.play()

    def broken(self):
        now = pygame.time.get_ticks()
        self.last_overheat = now
        fix = FixIcon(self.rect.x+50, self.rect.y-30, self.last_overheat, self.overheat_term)
        all_sprites.add(fix)
        broken_sound.play()


    def skill(self):
        targetPoint = (random.randrange(self.rect.width + 50, WINDOW_WIDTH - self.rect.width -50),
                              random.randrange(self.rect.height + 50, WINDOW_HEIGHT - self.rect.height -50))
        now = pygame.time.get_ticks()
        self.skill_delay = 500
        if now - self.last_skill > self.skill_delay:
            self.last_skill = now
            expl = Bomb(targetPoint, 'sm')
            all_sprites.add(expl)
            self.atkCount +=1
            if(self.atkCount >= 5):
                self.atkCount = 0
                self.skill_delay = 3000
                self.skillcond = False
                print("skill")


    def attack1(self):
        now = pygame.time.get_ticks()
        self.atk1_delay = 300
        if now - self.last_atk1 > self.atk1_delay:
            self.last_atk1 = now
            self.last_attack = now
            atk1 = Atk(self.shootPosx, self.shootPosy, self.atk1targetPos)
            all_sprites.add(atk1)
            atks.add(atk1)
            atk2 = Atk(self.shootPosx, self.shootPosy, (self.atk1targetPos[0]+100,self.atk1targetPos[1]))
            all_sprites.add(atk2)
            atks.add(atk2)
            atk3 = Atk(self.shootPosx, self.shootPosy, (self.atk1targetPos[0]-100,self.atk1targetPos[1]))
            all_sprites.add(atk3)
            atks.add(atk3)
            bossshoot_sound.play()
            self.atkCount +=1
            if(self.atkCount >= 2):
                self.atkCount = 0
                self.atk1_delay = 1000
                self.atk1cond = False
                print("attack1")

    def attack2(self):
        now = pygame.time.get_ticks()
        self.atk2_delay = 300
        if now - self.last_atk2 > self.atk2_delay:
            self.last_atk2 = now
            self.last_attack = now
            atk1 = Atk(self.shootPosx, self.shootPosy, self.atk2targetPos)
            all_sprites.add(atk1)
            atks.add(atk1)
            bossshoot_sound.play()
            self.atkCount +=1
            if(self.atkCount >= 3):
                self.atkCount = 0
                self.atk2_delay = 1000
                self.atk2cond = False
                print("atk222")


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosionRange_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosionRange_anim[self.size]):
                expl = Explosion(self.rect.center, 'sm') 
                random.choice(expl_sounds).play()
                all_sprites.add(expl)
                bombs.add(expl)
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionRange_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def draw_playerHp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_bossHp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 700
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

class Atk(pygame.sprite.Sprite):
    def __init__(self,x,y, targetPos):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(atk_img, (27, 26))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rot = np.arctan2(targetPos[1]-y, targetPos[0]-x) * 180 / np.pi
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        self.image = new_image
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = x
        self.rect.y = y
        self.rect.bottom = y+100
        self.speedy =  (targetPos[1] - self.rect.y) * 10/(abs(targetPos[1]-self.rect.y) + abs(targetPos[0]-self.rect.x))
        self.speedx = (targetPos[0] - self.rect.x) * 10/(abs(targetPos[1]-self.rect.y) + abs(targetPos[0]-self.rect.x))
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        #self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        """
        if self.rect.top > WINDOW_HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WINDOW_WIDTH + 100:
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            """

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.transform.scale(player_img, (40, 60))
        self.image = self.orig_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = random.randrange(self.rect.width,WINDOW_WIDTH-self.rect.width)
        self.rect.y = random.randrange(self.rect.height, WINDOW_HEIGHT-self.rect.height)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = self.rect.x+self.rect.width/2
        self.rect.centery = self.rect.y+self.rect.height/2
        self.rect.bottom = self.rect.y+self.rect.height

        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.tumble_delay = 1000
        self.knife_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.last_knife = pygame.time.get_ticks()
        self.last_tumble = pygame.time.get_ticks()
        self.hp = 100
        self.bulletcount = 10
        self.rot = 0

    def update(self):
        self.rot = -90 + ( np.arctan2(mousePos[0]-playerPos[0], mousePos[1]-playerPos[1]) * 180 / np.pi )
        new_image = pygame.transform.rotate(self.orig_image, self.rot)
        self.image = new_image
        self.speedx = 0
        self.speedy = 0
        mouseState = pygame.mouse.get_pressed()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        if keystate[pygame.K_SPACE]:
            self.tumble(self.speedx, self.speedy)
        if mouseState == (1,0,0) :
            if self.bulletcount > 0  :
                self.shoot()
        if mouseState == (0,0,1) :
            self.knife()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        self.rect.centerx = self.rect.x+self.rect.width/2
        self.rect.centery = self.rect.y+self.rect.height/2
        self.rect.bottom = self.rect.y+self.rect.height

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.bulletcount -= 1
            shoot_sound.play()
    def tumble(self, spx, spy):
        now = pygame.time.get_ticks()
        if now - self.last_tumble > self.tumble_delay:
            self.last_tumble = now
            self.rect.y += spy*10
            self.rect.x += spx*10
            tumble_sound.play()
            #self.rect.y += (mousePos[1] - self.rect.y) * 100/(abs(mousePos[1]-self.rect.y) + abs(mousePos[0]-self.rect.x))
            #self.rect.x += (mousePos[0] - self.rect.x) * 100/(abs(mousePos[1]-self.rect.y) + abs(mousePos[0]-self.rect.x))
    def knife(self):
        now = pygame.time.get_ticks()
        if now - self.last_knife > self.knife_delay:
            self.last_knife = now
            atkposy = self.rect.centery + ((mousePos[1] - self.rect.y) * 50/(abs(mousePos[1]-self.rect.y) + abs(mousePos[0]-self.rect.x)))
            atkposx = self.rect.centerx + ((mousePos[0] - self.rect.x) * 50/(abs(mousePos[1]-self.rect.y) + abs(mousePos[0]-self.rect.x)))
            katk = KnifeAtk((atkposx, atkposy), 'sm')
            knifes.add(katk)
            all_sprites.add(katk)
            knife_sound.play()

class KnifeAtk(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = slash_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(slash_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = slash_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.transform.scale(bullet_img, (5,20))
        self.image = self.orig_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.rot =  np.arctan2(mousePos[0]-playerPos[0], mousePos[1]-playerPos[1]) * 180 / np.pi
        new_image = pygame.transform.rotate(self.orig_image, self.rot)
        self.image = new_image
        self.speedy = (mousePos[1] - y) * 10/(abs(mousePos[1]-y) + abs(mousePos[0]-x))
        self.speedx = (mousePos[0] - x) * 10/(abs(mousePos[1]-y) + abs(mousePos[0]-x))

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 :
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class PlayerHit(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = hit_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(hit_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = hit_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class BossHit(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = bossHit_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(bossHit_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = bossHit_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



# Load all game graphics
background = pygame.image.load(path.join(img_dir, "Background.png")).convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH,WINDOW_HEIGHT))
background_rect = background.get_rect()
startScreen = pygame.image.load(path.join(img_dir, "startscreen.png")).convert()
startScreen = pygame.transform.scale(startScreen, (WINDOW_WIDTH,WINDOW_HEIGHT))
startScreen_rect = startScreen.get_rect()
gameoverScreen = pygame.image.load(path.join(img_dir, "gameoverscreen.png")).convert()
gameoverScreen = pygame.transform.scale(gameoverScreen, (WINDOW_WIDTH,WINDOW_HEIGHT))
gameoverScreen_rect = gameoverScreen.get_rect()
clearScreen = pygame.image.load(path.join(img_dir, "clearScreen.png")).convert()
clearScreen = pygame.transform.scale(clearScreen, (WINDOW_WIDTH,WINDOW_HEIGHT))
clearScreen_rect = startScreen.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Player.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
Boss_img = pygame.image.load(path.join(img_dir, "Boss.png")).convert()
box_img = pygame.image.load(path.join(img_dir, "box.png")).convert()
fix_img = pygame.image.load(path.join(img_dir, "fix.png")).convert()
gun_img = pygame.image.load(path.join(img_dir, "gun.png")).convert()
cursor_img = pygame.image.load(path.join(img_dir, "cursor.png"))
cursor_img = pygame.transform.scale(cursor_img, (48,40))
slash_anim = {}
slash_anim['lg'] = []
slash_anim['sm'] = []
for i in range(1,11):
    filename = 'knife{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (40, 40))
    slash_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (40, 40))
    slash_anim['sm'].append(img_sm)
atk_img = pygame.image.load(path.join(img_dir, "atk.png")).convert()
explosionRange_anim = {}
explosionRange_anim['lg'] = []
explosionRange_anim['sm'] = []
for i in range(1,14):
    filename = 'bomb{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosionRange_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (75, 75))
    explosionRange_anim['sm'].append(img_sm)
atk_img = pygame.image.load(path.join(img_dir, "atk.png")).convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(0,9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (100, 100))
    explosion_anim['sm'].append(img_sm)
hit_anim = {}
hit_anim['lg'] = []
hit_anim['sm'] = []
for i in range(1,10):
    filename = 'regularHit0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    hit_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (75, 75))
    hit_anim['sm'].append(img_sm)
bossHit_anim = {}
bossHit_anim['lg'] = []
bossHit_anim['sm'] = []
for i in range(0,9):
    filename = 'SonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (35, 35))
    bossHit_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (35, 35))
    bossHit_anim['sm'].append(img_sm)

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.mp3'))
knife_sound = pygame.mixer.Sound(path.join(snd_dir, 'knife_atk.mp3'))
knifehit_sound = pygame.mixer.Sound(path.join(snd_dir, 'knife.mp3'))
player_hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit.mp3'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'die.mp3'))
tumble_sound = pygame.mixer.Sound(path.join(snd_dir, 'tumble.mp3'))
broken_sound = pygame.mixer.Sound(path.join(snd_dir, 'broken.mp3'))
bosshit_sound = pygame.mixer.Sound(path.join(snd_dir, 'boss_hit.mp3'))
boxcreate_sound = pygame.mixer.Sound(path.join(snd_dir, 'box_appear.mp3'))
box_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun_refill.mp3'))
bossshoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'boss_shoot.mp3'))
clear_sound = pygame.mixer.Sound(path.join(snd_dir, 'congratulation.mp3'))
expl_sounds = []
for snd in ['explosion2.mp3', 'explosion3.mp3', 'explosion4.mp3', 'explosion5.mp3']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'makai-symphony-dragon-slayer(chosic.com).mp3'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)

all_sprites = pygame.sprite.Group()
atks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boxes = pygame.sprite.Group()
knifes = pygame.sprite.Group()
bombs = pygame.sprite.Group()
player = Player()
boss = Boss()
all_sprites.add(player)
all_sprites.add(boss)

# Game loop
game_over = True
game_clear = False
running = True
while running:
    if game_over or game_clear :
        print("초기화")
        if game_clear :
            show_clear_screen()
        elif player.hp < 1:
            show_gameover_screen()
        show_go_screen()
        game_over = False 
        game_clear = False       
        all_sprites = pygame.sprite.Group()
        atks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        boxes = pygame.sprite.Group()
        knifes = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        player = Player()
        boss = Boss()
        all_sprites.add(player)
        all_sprites.add(boss)
        
    mousePos = pygame.mouse.get_pos()
    playerPos = (player.rect.centerx, player.rect.centery)
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    


    #bomb collide
    hits = pygame.sprite.spritecollide(player, bombs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player_hit_sound.play()
        player.hp -= 30
        print("폭탄 피격!")
        if player.hp < 1 :
            death_explosion = Explosion(player.rect.center, 'sm')
            all_sprites.add(death_explosion)

    # check to see if a knife hit boss
    hits = pygame.sprite.spritecollide(boss, knifes, True, pygame.sprite.collide_rect)
    for hit in hits:
        knifehit_sound.play()
        expl = KnifeAtk(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if boss.hp > 0 :
            boss.hp -= 5
            print("나이프 공격")
        #newmob()

    # check to see if  bullet hit  boss
    hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_rect)
    for hit in hits:
        bosshit_sound.play()
        expl = BossHit(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if boss.hp > 0 :
                boss.hp -= 1
    
    # check to see if  box hit  player
    hits = pygame.sprite.spritecollide(player, boxes, True, pygame.sprite.collide_circle)
    for hit in hits:
        box_sound.play()
        player.bulletcount += 10

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, atks, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = PlayerHit(hit.rect.center, 'sm')
        all_sprites.add(expl)
        player.hp -= 10
        player_hit_sound.play()
        print("피격!")
        if player.hp < 1 :
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'sm')
            all_sprites.add(death_explosion)


    
    left_icon = gunIcon(20,WINDOW_HEIGHT-35)
    all_sprites.add(left_icon)

    if player.hp < 1 : #and not death_explosion.alive():
        game_over = True
        print("GG")
        
    if boss.hp < 1 : #and not death_explosion.alive():
        game_clear = True
        print("Clear")

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    screen.blit(cursor_img, mousePos)

    
    #UI
    #pygame.draw.circle(screen, RED, playerPos, 5)
    #pygame.draw.rect(screen, RED, [boss.rect.x, boss.rect.y, boss.rect.width, boss.rect.height])
    draw_text(screen, "BOSS", 32, WINDOW_WIDTH/2-400, 7, BLACK)
    draw_text(screen, "HP", 16, 20, WINDOW_HEIGHT-25, WHITE)
    draw_text(screen, "LEFT BULLETS : ", 16, 100, WINDOW_HEIGHT-45, WHITE)
    draw_text(screen, str(player.bulletcount), 16, 170, WINDOW_HEIGHT-45, WHITE)
    draw_playerHp_bar(screen, 35, WINDOW_HEIGHT-20, player.hp)
    draw_bossHp_bar(screen, WINDOW_WIDTH/2-350, 15, boss.hp)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
