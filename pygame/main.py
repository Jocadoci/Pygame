import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.alive = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # to scroll
        #if self.player.rect.right <= WIDTH / 10:
        #    self.player.pos.x -= abs(self.player.vel.x)
        #    for plat in self.platforms:
        #        plat.rect.x -= abs(self.player.vel.x)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.alive = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
    def draw(self):
        # Game Loop - draw
        self.screen.blit(pg.image.load(BACKGROUND), [0,0])
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 14, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(RED)
        self.draw_text(TITLE, 50, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("INSTRCUTONS", 20, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("INSTRCUTONS", 20, WHITE, WIDTH / 2, HEIGHT *3 / 4)
        self.draw_text("HSC: "+ str(self.highscore), 22, WHITE, WIDTH / 2 ,15)
        pg.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        # game over/continue
        if not self.alive:
            return
        self.screen.fill(BLACK)
        self.draw_text("DEAD", 50, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("INSTRCUTONS", 20, WHITE, WIDTH / 2, HEIGHT / 2)
        
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('', 20, WHITE, WIDTH / 2, HEIGHT - 15)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("HSC: "+ str(self.highscore), 22, WHITE, WIDTH / 2 ,50)

        self.draw_text("INSTRCUTONS", 20, WHITE, WIDTH / 2, HEIGHT *3 / 4)
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.alive = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
g = Game()
g.show_start_screen()
while g.alive:
    g.new()
    g.show_go_screen()

pg.quit()