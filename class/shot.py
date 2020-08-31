import pygame 
from setting import *

class Shot:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,20,5)

    def draw(self):
        pygame.draw.rect(screen,(255,255,0),self.rect)
        
