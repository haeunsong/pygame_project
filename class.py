import pygame,os,math,random,sys
from pygame.locals import *

pygame.init()
pygame.font.init()

width, height = 800,500
screen=pygame.display.set_mode((width,height))
FPS=30 # 속도
fpsClock=pygame.time.Clock()
# arrows=[] # 화살각도, 화살 x좌표, 화살 y좌표 

# keys=[False,False] 

current_path = os.path.dirname(__file__) 
image_path = os.path.join(current_path, 'images') 
# healthbar = pygame.image.load(os.path.join(image_path, 'healthbar.png'))
# health = pygame.image.load(os.path.join(image_path, 'health.png'))
soil = pygame.image.load(os.path.join(image_path, 'soil.png'))
key = pygame.image.load(os.path.join(image_path,'key.png'))
bang = pygame.image.load(os.path.join(image_path,'bang.png'))
heart = pygame.image.load(os.path.join(image_path,'heart.png'))

# running = 1 # 게임 실행
# exitcode = 0 # 1이 되면 게임 종료

class Player:
    playerpos = [154,155]

    def __init__(self):
        self.image = pygame.image.load(os.path.join(image_path, 'alien.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        self.hp = 2

    def draw(self):
        self.mousepos = pygame.mouse.get_pos()
        self.angle = math.atan2(self.mousepos[1]-self.playerpos[1],self.mousepos[0]-self.playerpos[0])
        self.playerrot = pygame.transform.rotate(self.image,360-self.angle*57.29) 
        self.playerpos1 = (self.playerpos[0]-self.playerrot.get_rect().width/2, self.playerpos[1]-self.playerrot.get_rect().height/2)
        screen.blit(self.playerrot, self.playerpos1) # playerrot를 좌표 playerpos1에 표시
        
class Shot:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,20,5)

    def draw(self):
        pygame.draw.rect(screen,(255,255,0),self.rect)
        
class Enemy:
    badtimer1 = 0

    def __init__(self):
        self.image = pygame.image.load(os.path.join(image_path, 'badguy.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        
    def draw(self):
        pass 


class Padlock:
    padlock_info = dict(id0=94,id1=94,id2=94,id3=94,id4=94) 
   
    def __init__(self,y):
        self.image = pygame.image.load(os.path.join(image_path, 'padlock.png'))
        self.small_health = pygame.image.load(os.path.join(image_path,'small_health.png'))
        self.small_healthbar = pygame.image.load(os.path.join(image_path,'small_healthbar.png'))
        self.rect = pygame.Rect(self.image.get_rect())
        self.y = y
        


    def draw(self):
        screen.blit(self.image,(16,self.y))
    
    def collision(self):
        pass 

def ifPadlockHp0(padlock):
    for value in padlock.padlock_info.values():
        if value<=0: return True 
        else: return False 

# def afterGameOver(running,gameOver):
#     exitKey = [False]
#     while True:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 pygame.quit()
#                 exit(0)
#             elif event.type==pygame.KEYDOWN:
#                 if event.key==pygame.K_c:
#                     exitKey[0]=True 
#                     running=1
#                     gameOver=0
#                     break
#             elif event.type==pygame.KEYUP:
#                 if event.key==pygame.K_c:
#                     exitKey[0]=False 

#         sysfont = pygame.font.SysFont(None,80)
#         text = sysfont.render("GAME OVER!!",True,(0,255,255))
#         text_rect = text.get_rect()
#         text_rect.center = (400,250)
#         screen.blit(text,text_rect.topleft)
#         pygame.display.flip()
#         fpsClock.tick(FPS)
    
#     return running,gameOver
    
def continueGame():
    main()

def main():
    # 메인루틴
    running = 1
    badtimer = 50
    badguys = [[800,random.randint(50,450)]] # 적 처음 위치
    enemy = Enemy()
    player = Player()
    padlockToKey = False 
    gameOver = 0
    # exitcode = 0
    again = 0
    exitKey = [False]
    padlock_y = [13,113,213,313,413]
    arrows=[] # 화살각도, 화살 x좌표, 화살 y좌표 
    keys=[False,False] 
    

    while running :
        # if again:
        #     enemy = Enemy()
        #     player = Player()
            
        #     for y in padlock_y:
        #         padlock = Padlock(y)
        #         if ifPadlockHp0(padlock):
        #             screen.blit(pygame.image.load(os.path.join(image_path,'key.png')),(10,y+10))              
        #             padlockToKey = True 
        #         else: 
        #             padlock.draw() 
        #             screen.blit(padlock.small_healthbar,(0,y+72)) # 각각 자물쇠 hp 틀 그리기(빨간색)

        if not gameOver:
            again = 0
            badtimer -= 2
            screen.fill((102,62,37)) # 갈색 배경으로 초기화

            # 화면 구성
            for x in range(int(width/soil.get_width()+1)):
                for y in range(int(height/soil.get_width()+1)): 
                    screen.blit(soil,(x*100,y*100)) # 이미지의 왼쪽 위 좌표

            # padlock_y = [13,113,213,313,413]

            for y in padlock_y:
                padlock = Padlock(y)
                if ifPadlockHp0(padlock):
                    screen.blit(pygame.image.load(os.path.join(image_path,'key.png')),(10,y+10))              
                    padlockToKey = True 
                else: 
                    padlock.draw() 
                    screen.blit(padlock.small_healthbar,(0,y+72)) # 각각 자물쇠 hp 틀 그리기(빨간색)
            player.draw()
            
            # 총알 그리기

            for bullet in arrows:
                index=0
                velx=math.cos(bullet[0])*20
                vely=math.sin(bullet[0])*20
                bullet[1]+=velx
                bullet[2]+=vely 
                # 범위 벗어나면 화살 삭제
                if bullet[1]>1000 or bullet[2]>500 or bullet[1]<-64 or bullet[2]<-64 :
                    arrows.pop(index)
                index+=1
                shot = Shot(bullet[1],bullet[2])
                shot.draw()


            # 적 그리기 
            enemy_y = random.randint(50,450)
            if badtimer==0:
                badguys.append([800,enemy_y])
                badtimer=100-(enemy.badtimer1*2) # 지금까지 badtimer가 몇 번 실행되었는지에 따라 badtimer 재설정.
                # 시간 지날수록 적 생성 속도 빨라짐
                if enemy.badtimer1>=35:
                    enemy.badtimer1=35
                else:
                    enemy.badtimer1+=5

            index = 0

            for badguy in badguys:
                # if badguy[0]<-64: # 적의 x위치 업데이트 후 화면 벗어나면 제거
                #     badguys.pop(index)

                badguy[0]-=9 # 적의 x좌표를 조정하여 이동속도 조절 가능

                # 적과 자물쇠의 충돌처리
                enemy.rect.top = badguy[1] # 적의 y좌표
                enemy.rect.left = badguy[0] # 적의 x좌표

                # 좌표를 벗어나면 hp감소하는 걸로 함.
                bangy = badguy[1]+5
                if enemy.rect.left < 64 and 0<badguy[1]<=100 :
                    padlock.padlock_info['id0'] -= 20
                    screen.blit(bang,(64,bangy))
                    badguys.pop(index)
                elif enemy.rect.left < 64 and 100<badguy[1]<=200 :
                    padlock.padlock_info['id1'] -= 20
                    screen.blit(bang,(64,bangy))
                    badguys.pop(index)
                elif enemy.rect.left < 64 and 200<badguy[1]<=300 :
                    padlock.padlock_info['id2'] -= 20
                    screen.blit(bang,(64,bangy))
                    badguys.pop(index)
                elif enemy.rect.left < 64 and 300<badguy[1]<=400 :
                    padlock.padlock_info['id3'] -= 20
                    screen.blit(bang,(64,bangy))
                    badguys.pop(index)
                elif enemy.rect.left < 64 and 400<enemy_y<=500 :
                    padlock.padlock_info['id4'] -= 20
                    screen.blit(bang,(64,bangy))
                    badguys.pop(index)   

                # 화살과 적의 충돌처리
                index1 = 0           
                for bullet in arrows:
                    shot.rect.left = bullet[1]
                    shot.rect.top = bullet[2] 
                    if enemy.rect.colliderect(shot.rect):
                        badguys.pop(index)
                        arrows.pop(index1)
                    index1 += 1
                    
                # 캐릭터와 적의 충돌처리
                player.rect.left = player.playerpos1[0]
                player.rect.top = player.playerpos1[1]
                if enemy.rect.colliderect(player.rect):
                    badguys.pop(index)
                    player.hp -= 1          

                # 다음 적 생성
                index += 1 

            # 모든 적을 그림
            for badguy in badguys:
                screen.blit(enemy.image,badguy)

            # 자물쇠 hp 처리
            hpy = 86
            for key,value in padlock.padlock_info.items():
                for smallHealth in range(value+3):
                    screen.blit(padlock.small_health,(smallHealth+1,hpy))
                hpy += 100
            
            # 캐릭터 hp 처리
            hpx = 750
            for hp in range(0,player.hp):
                screen.blit(heart,(hpx-hp,10))
                hpx -= 55

            # 화면 업데이트 
            # pygame.display.flip()
            # fpsClock.tick(FPS)

            # 키 이벤트 처리
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)
                # 키를 누를 때
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_w:
                        player.playerpos[1] -= 100
                    elif event.key==pygame.K_a:
                        keys[0]=True
                    elif event.key==pygame.K_s:
                        player.playerpos[1] +=100
                    elif event.key==pygame.K_d:
                        keys[1]=True 

                # 키를 뗄 때
                elif event.type==pygame.KEYUP:
                    if event.key==pygame.K_a:
                        keys[0]=False
                    elif event.key==pygame.K_d:
                        keys[1]=False

                    
            # 마우스 클릭하면
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mousepos=pygame.mouse.get_pos()
                # acc[1]+=1 # 화살 발사 횟수 증가
                    arrows.append([math.atan2(mousepos[1]-player.playerpos1[1],mousepos[0]-player.playerpos1[0]),player.playerpos1[0]+32,player.playerpos1[1]+32])
            
            if keys[0]:
                player.playerpos[0]-=10
            elif keys[1]:
                player.playerpos[0]+=10

            # 게임오버 / 게임승리 체크
            if player.hp==0 or padlockToKey:
                gameOver = 1 # 게임오버
                # running = 0

            # 게임오버시 
            # if gameOver :
            #     sysfont = pygame.font.SysFont(None,80)
            #     text = sysfont.render("GAME OVER!!",True,(0,255,255))
            #     text_rect = text.get_rect()
            #     text_rect.center = (400,250)
            #     screen.blit(text,text_rect.topleft)
            #     running = 0
            #     # exitcode = 1 
            
            pygame.display.flip()
            fpsClock.tick(FPS)
        
        if gameOver:
            # running,gameOver = afterGameOver(running,gameOver)
            # main()
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_c:
                            exitKey[0]=True 
                            again = 1
                            gameOver = 1
                            running = 0
                            continueGame()


                            break
                            # running=1
                            # gameOver=0
                            # again=1
                            # main()
                            # break
                    elif event.type==pygame.KEYUP:
                        if event.key==pygame.K_c:
                            exitKey[0]=False 

                sysfont = pygame.font.SysFont(None,80)
                text = sysfont.render("GAME OVER!!",True,(0,255,255))
                text_rect = text.get_rect()
                text_rect.center = (400,250)
                screen.blit(text,text_rect.topleft)
                pygame.display.flip()
                fpsClock.tick(FPS)

    if again:
        continueGame()


main()

