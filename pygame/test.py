import pygame
import random
import os

WIDTH = 1000
HEIGHT = 500
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

# assets folders
game_folder = os.path.dirname(__file__)
img_folder =  os.path.join(game_folder, "img")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FEARLESS')
clock = pygame.time.Clock()

# Font
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

# Attack's animations
attack_anim = {}
attack_anim['pala'] = []
for i in range(4):
	filename = 'palaAttack{}.png'.format(i)
	img = pygame.image.load(os.path.join(img_folder,filename)).convert()
	img.set_colorkey(BLACK)
	img_pala = pygame.transform.scale(img, (50,50))
	attack_anim['pala'].append(img_pala)


# Graphics
#background = pygame.image.load(path.join(img_folder, "name")).convert()
#background_rect = background.get_rect()
pala =  pygame.image.load(os.path.join(img_folder, "pala.png")).convert()


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pala, (50,50) )
		self.image.set_colorkey(BLACK) # To ignore a possible background color
		#self.image = pygame.Surface((50,20))
		#self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.left = WIDTH * 1/10
		self.rect.bottom = HEIGHT - 3
		self.speedx = 0
		self.shield = 5
	
	# Update section	
	def update(self):
		self.speedx = 0 # without pressing any key the speed is 0
		keystate = pygame.key.get_pressed() # function to identify key pressed
		if keystate[pygame.K_LEFT]:
			self.speedx = -3
		if keystate[pygame.K_RIGHT]:
			self.speedx = 3
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
			
	def punch(self):
		attack = Attack(self.centerx, self.left)
		all_sprites.add(attack)
		attacks.add(attack)

class Attack(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.transform.scale(pala, (50,50) )
		#self.image.set_colorkey(BLACK) # To ignore a possible background color
		self.image = pygame.Surface ((30,30))
		
		self.rect = self.image.get_rect()
		self.rect.bottom = HEIGHT - 3 
		self.rect.centerx = x + 50
		self.speedx = 0
		#self.frame = 0 
		#self.last_update = pygame.time.get_ticks()
		#self.frame_rate = 30
		
	def update(self):
		self.rect.x += self.speedx

		#now = pygame.time.get_ticks()
		#if now - self.last_update > self.frame_rate:
		#	self.last_update = now
		#	self.frame += 1
		#	if self.frame == len(attack_anim[self.size]):
		#		self.kill()
		#	else:
		#		center = self.rect.center
		#		self.image = attack_anim[self.size][self.frame]
		#		self.rect = self.image.get_rect()
		#		self.rect.center = center

		if self.rect.bottom < 0:
			self.kill()


class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30,30))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.right = WIDTH
		self.rect.bottom = HEIGHT - 3
		self.speedx = random.randrange(2 , 6)
		self.damage = 1
		
	def update(self):
		# update the position of the mobs with the speed values.
		self.rect.x += -self.speedx 
		# if the mob pass the left -500 pixels will spawn another mob
		if self.rect.right >  self.rect.left <  - 500:

			self.rect.right = WIDTH
			self.rect.bottom = HEIGHT - 3
			self.speedx = random.randrange(1,5)

	
# function for the mobs respawn
def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)
	
# adding sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
damage = Mob()

attacks = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range (4):
	newmob()
	
# Score game
score = 0

# Game Loop
alive = True
while alive:
	
	# keep loop running at the right speed
	clock.tick(FPS)
	
	# Process input (events)
	for event in pygame.event.get():
		
		# closing window
		if event.type == pygame.QUIT:
			alive = False	
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.punch()
			
	# Update
	all_sprites.update()
	
	# if the attacks hit the mobs
	hits = pygame.sprite.groupcollide(mobs, attacks, True, True)
	for hit in hits:
		score += 1
		newmob()
	
	# check a collision
	hits = pygame.sprite.spritecollide(player, mobs, True)
	for hit in hits:
		
		player.shield -= damage.damage
		newmob()

		if player.shield < 0:
			alive =  False
	
	# Draw / render
	screen.fill(BLACK)
	# screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 14, WIDTH / 2, 10)
	
	# after, flip
	pygame.display.flip()
	
pygame.quit()
	
