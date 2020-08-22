import pygame 
from setting import *

class Enemy:
    badtimer1 = 0

    def __init__(self):
        self.image = pygame.image.load(os.path.join(image_path, 'badguy.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        
    def draw(self,badguy):
        screen.blit(self.image,badguy)