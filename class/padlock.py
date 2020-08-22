import pygame 
from setting import *

class Padlock:
    padlock_info = dict(id0=94,id1=94,id2=94,id3=94,id4=94) 
   
    def __init__(self,y):
        self.image = pygame.image.load(os.path.join(image_path, 'padlock.png'))
        self.small_health = pygame.image.load(os.path.join(image_path,'small_health.png'))
        self.small_healthbar = pygame.image.load(os.path.join(image_path,'small_healthbar.png'))
        self.bang = pygame.image.load(os.path.join(image_path,'bang.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        self.y = y
        self.count = 5
        
    def draw(self):
        screen.blit(self.image,(16,self.y))
    
    def collision(self,badguy,badguys,bangy,enemy,enemyindex):
        tmpId = None
        self.badguy = badguy 
        self.bangy = bangy
        enemy.rect.left = badguy[0]
        enemy.rect.top = badguy[1]

        section = [0,100,200,300,400,500]
        sectionId = ['id0','id1','id2','id3','id4']

        for i in range(0,5):
            if badguy[1]>section[i] and badguy[1]<=section[i+1]:
                tmpId = sectionId[i]
                break

        if enemy.rect.left<64:
            self.padlock_info[str(tmpId)] -= 40
            screen.blit(self.bang,(64,bangy))
            badguys.pop(enemyindex)
            
    def ifPadlockHp0(self):
        check=[0,0,0,0,0]
        sum = 0
        for index,(key,value) in enumerate(self.padlock_info.items()):
            if value<=0: 
                check[index]= 1
                self.count-=1 
            else: check[index]= 0
        for i in check:
            sum += i 
        if sum==5: return True 
        else: return False
