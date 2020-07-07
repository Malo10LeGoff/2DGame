# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:31:22 2020

@author: LENOVO
"""

import pygame
import time
import random
#from game import Game
pygame.init()
print(time.time())



def check_collisions(sprite, group): ### check if a sprite collides with a groupe of sprite
    return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask )  ### The parameter false says that if the player touches the monster he doesn't die right away
        ### collide_mask is the type of collision
### Class player

class Player(pygame.sprite.Sprite):  ### Sprite is the original class for graphic component
    def __init__(self):
        super(Player,self).__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.image = pygame.image.load("player3.png")
        self.rect = self.image.get_rect() ### Coordinates corresponding to rectangle framing the player
        self.rect.x = 400
        self.rect.y = 300
        self.jumph = 30
        self.all_fireball = pygame.sprite.Group() ### Each fireball has to be put in this group
        self.all_lightning = pygame.sprite.Group()

    def move_right(self,group_monster):
        if not check_collisions(self, group_monster):
            self.rect.x += self.velocity
        
    def move_left(self):
        self.rect.x -= self.velocity
        
    def jump(self):
        self.rect.y -= self.jumph
        print('b')
        time.sleep(2)
        print("a")
        self.rect.y += self.jumph
        
    def launch_fireball(self):
        p = Fireball(self)
        self.all_fireball.add(p)
        print("Fireball launched")
              
    def launch_lightning(self):
        e = Lightning(self)
        self.all_lightning.add(e)
        print("Lighining launched")
        
    def update_health_bar(self, surface):
        bar_color = (111, 210, 46)  ### color of the bar, green here
        background_color = (60, 63, 60)
        bar_pos = [self.rect.x + 60, self.rect.y - 5, self.health, 7]   ### position, width and thickness of the bar
        background_bar_pos = [self.rect.x + 60, self.rect.y - 5, self.max_health, 7]
        ### Drawing of the bar
        pygame.draw.rect(surface, background_color, background_bar_pos)
        pygame.draw.rect(surface, bar_color, bar_pos)
        
    def damage_player(self, amount):
        self.health -= amount
        if self.health < 0 :
            running = False
            pygame.quit()
        
        
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super(Monster,self).__init__()
        self.health = 100
        self.velocity = 3 + random.randint(0,4)
        self.attack = 0.3
        self.max_health = 100
        self.image = pygame.image.load("mummy.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1080 + random.randint(0,300)
        self.rect.y = 300
        self.image=pygame.transform.scale(self.image,(250,250))
        self.all_monsters = pygame.sprite.Group()
        #self.spawn_monster()
        
    def forward(self, all_players):
        if not check_collisions(self, all_players):
            self.rect.x -= self.velocity
            print("monster moving")
        if check_collisions(self, all_players):
            print("monster attacking")
            for player in all_players:
                player.damage_player(self.attack)
        
        
    def update_health_bar(self, surface):
        bar_color = (111, 210, 46)  ### color of the bar, green here
        background_color = (60, 63, 60)
        bar_pos = [self.rect.x + 60, self.rect.y - 5, self.health, 7]   ### position, width and thickness of the bar
        background_bar_pos = [self.rect.x + 60, self.rect.y - 5, self.max_health, 7]
        ### Drawing of the bar
        pygame.draw.rect(surface, background_color, background_bar_pos)
        pygame.draw.rect(surface, bar_color, bar_pos)
        
    def damage(self, amount):
        self.health -= amount
        
        if self.health <= 0: 
            self.all_monsters.remove(self)
        
        
        
def spawn_monster():
    m = Monster()
    m.all_monsters.add(m)
    return m


class Fireball(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Fireball,self).__init__()
        self.velocity = 5
        self.image = pygame.image.load("projectile.png")
        self.image=pygame.transform.scale(self.image,(75,75))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 90
        self.rect.y = player.rect.y + 50

    def move(self, all_monsters):
    
        self.rect.x += self.velocity
        for monster in check_collisions(self, all_monsters):
            player.all_fireball.remove(self)
            monster.damage(10)
        if self.rect.x > 1080:
            player.all_fireball.remove(self)
            
            
class Lightning(pygame.sprite.Sprite):
    def __init__(self,player):
        super(Lightning,self).__init__()
        self.velocity = 50
        self.image = pygame.image.load("light.png")
        self.image=pygame.transform.scale(self.image,(350,350))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 90
        self.rect.y = player.rect.y - 40
        
    def erase(self, all_monster):
        time.sleep(3)   ### casting time for lightning
        player.all_lightning.remove(self)
        for monster in all_monster:
            monster.damage(30)
    
### Generate game window

pygame.display.set_caption("Game")
screen = pygame.display.set_mode((1000,600))
running = True
background = pygame.image.load("vg2.jpg")

all_players = pygame.sprite.Group()

player = Player()
all_players.add(player)

monster = spawn_monster()
monster2 = spawn_monster()
monster3 = spawn_monster()

pressed = {'right_arrow' : False,
           'left_arrow' : False}

while(running):
    screen.blit(background,(0,0))
    screen.blit(player.image,player.rect)
    #screen.blit(monster.image,(800,325))
    
    player.update_health_bar(screen)
    ### Player motion
    if pressed['right_arrow'] == True and player.rect.x < screen.get_width():
        player.move_right(monster.all_monsters)
    if pressed['left_arrow'] == True and player.rect.x > 0:
        player.move_left()
        
        
    for fireball in player.all_fireball:
        fireball.move(monster.all_monsters)
        
        
    player.all_lightning.draw(screen)    
    player.all_fireball.draw(screen)
    
    
    for light in player.all_lightning:
        light.erase(monster.all_monsters)
        
    for monst in monster.all_monsters:
        #print("Loop entered")
        monst.forward(all_players)
        monst.update_health_bar(screen)
        
    monster.all_monsters.draw(screen)

        
    pygame.display.flip() ### update the display
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:  ### detect if the player press the keyboard
            if event.key == pygame.K_LEFT and player.rect.x > 0:
                
                pressed['left_arrow'] = True
                pressed['right_arrow'] = False
                
            if event.key == pygame.K_RIGHT and player.rect.x < screen.get_width():
                
                pressed['right_arrow'] = True
                pressed['left_arrow'] = False
                
            if event.key == pygame.K_UP:
                player.jump()
            
            if event.key == pygame.K_SPACE:
                player.launch_fireball()
                
            if event.key == pygame.K_DOWN:
                player.launch_lightning()
                
        if event.type == pygame.KEYUP:  ### unpressed keyboard
            pressed['right_arrow'] = False
            pressed['left_arrow'] = False
            