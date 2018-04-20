# SPRITES
import time
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        #image = pg.transform.scale(image, (50,50))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.load_images()
        self.image = self.standing_frames[0]
        #self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH * 1/10
        self.rect.bottom = HEIGHT - 15
        self.pos = vec(self.rect.left, self.rect.bottom)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        # images for STANDING animations
        self.standing_frames = [self.game.spritesheet.get_image(0, 0, 50, 50),
                                self.game.spritesheet.get_image(50, 0, 50, 50)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        # images for WALKING animations
        self.walking_frames_r = [self.game.spritesheet.get_image(0, 50, 50, 50),
                                self.game.spritesheet.get_image(50, 50, 50, 50)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))
        for frame in self.walking_frames_l:
            frame.set_colorkey(BLACK)

        # images for FIGHTING animations
        self.attack_frames = [self.game.spritesheet.get_image(0, 100, 50, 50),
                            #self.game.spritesheet.get_image(0, 150, 70, 70),
                            self.game.spritesheet.get_image(0, 220, 70, 50)]
        for frame in self.attack_frames:
            frame.set_colorkey(BLACK)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP # Jump power

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0 
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # WALKING animation
        if self.walking:
            if now -  self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # STANDING animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 450:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # FIGHTHING animation
        keys = pg.key.get_pressed()
        if keys[pg.K_x]:
            if now - self.last_update > 200:
                for i in range(1):
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                    self.image = self.attack_frames[self.current_frame]
                    bottom = self.rect.bottom
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    #time.sleep(1)
                #self.current_frame = (self.current_frame+1), i


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.set_alpha(1)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
