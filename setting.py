import pygame,os

width, height = 800,500
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("** Defend Padlock **")
FPS=40 
fpsClock=pygame.time.Clock()

current_path = os.path.dirname(__file__) 
image_path = os.path.join(current_path, 'images') 
soil = pygame.image.load(os.path.join(image_path, 'soil.png'))
key = pygame.image.load(os.path.join(image_path,'key.png'))
heart = pygame.image.load(os.path.join(image_path,'heart.png'))
star = pygame.image.load(os.path.join(image_path,'star.png'))
sad = pygame.image.load(os.path.join(image_path,'sad.png'))