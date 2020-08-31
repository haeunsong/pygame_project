import pygame,os,math
from setting import *

class Player:
    playerpos = [154,155]

    def __init__(self):
        self.image = pygame.image.load(os.path.join(image_path, 'alien.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        self.hp = 3

    def draw(self):
        self.mousepos = pygame.mouse.get_pos()
        self.angle = math.atan2(self.mousepos[1]-self.playerpos[1],self.mousepos[0]-self.playerpos[0])
        self.playerrot = pygame.transform.rotate(self.image,360-self.angle*57.29) 
        self.playerpos1 = (self.playerpos[0]-self.playerrot.get_rect().width/2, self.playerpos[1]-self.playerrot.get_rect().height/2)
        screen.blit(self.playerrot, self.playerpos1) # playerrot를 좌표 playerpos1에 표시
