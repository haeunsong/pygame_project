import pygame,os,math,random,time
from pygame.locals import *
from setting import *
from MyDef import *
from player import *
from enemy import *
from padlock import *
from timer import *
from shot import *

pygame.init()
pygame.font.init()

def main():
    running = 1
    badtimer = 50
    badguys = [[800,random.randint(50,450)]] # 적 처음 위치
    enemy = Enemy()
    player = Player()
    padlockToKey = False 
    gameOver = 0
    gameWin = 0
    gameLose = 0
    padlock_y = [13,113,213,313,413]
    arrows=[] # 총알각도, 총알 x좌표, 총알 y좌표 
    keys=[False,False] 

    timer = Timer()
    timer.start()
    
    while running :
        if not gameOver:
            timerResult = round(timer.get_elapsed())

            badtimer -= 2
            screen.fill((102,62,37)) # 갈색 배경으로 초기화

            # 화면 구성
            for x in range(int(width/soil.get_width()+1)):
                for y in range(int(height/soil.get_width()+1)): 
                    screen.blit(soil,(x*100,y*100)) # 이미지의 왼쪽 위 좌표

            for y in padlock_y:
                padlock = Padlock(y)
                if padlock.ifPadlockHp0():
                    screen.blit(pygame.image.load(os.path.join(image_path,'key.png')),(10,y+10))              
                    padlockToKey = True 
                else: 
                    padlock.draw() 
                    screen.blit(padlock.small_healthbar,(0,y+72)) # 각각 자물쇠 hp 틀 그리기(빨간색)
            
            player.draw() 
            
            # 총알 그리기
            for bullet in arrows:
                index=0
                velx=math.cos(bullet[0])*30
                vely=math.sin(bullet[0])*30
                bullet[1]+=velx
                bullet[2]+=vely 
                # 범위 벗어나면 총알 삭제
                if bullet[1]>1000 or bullet[2]>500 :
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
                badguy[0]-=9 # 적의 x좌표를 조정하여 이동속도 조절 가능

                # 자물쇠와 적의 충돌처리
                # 좌표를 벗어나면 hp감소하는 걸로 함.
                bangy = badguy[1]+5
                padlock.collision(badguy,badguys,bangy,enemy,index)
                
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
                enemy.draw(badguy)

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

            # 시계 표시
            font = pygame.font.Font(None,80)
            timeValue = 90-timerResult # 90초 카운트다운
            if timeValue<=10:
                timerText = font.render(str(timeValue),True,(255,255,62))
            else:
                timerText = font.render(str(timeValue),True,(0,0,0))
            screen.blit(timerText,(720,420))
            

            # 키 이벤트 처리
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)
                # 키를 누를 때
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_w:
                        if player.playerpos[1]<=100:
                            player.playerpos[1]=455
                        else: player.playerpos[1] -= 100
                    elif event.key==pygame.K_a:
                        keys[0]=True
                    elif event.key==pygame.K_s:
                        if player.playerpos[1]>=400:
                            player.playerpos[1]=55
                        else: player.playerpos[1] +=100
                    elif event.key==pygame.K_d:
                        keys[1]=True 

                # 키를 뗄 때
                elif event.type==pygame.KEYUP:
                    if event.key==pygame.K_a:
                        keys[0]=False
                    elif event.key==pygame.K_d:
                        keys[1]=False
                # 마우스 클릭시
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mousepos=pygame.mouse.get_pos()
                    arrows.append([math.atan2(mousepos[1]-player.playerpos1[1],mousepos[0]-player.playerpos1[0]),player.playerpos1[0]+32,player.playerpos1[1]+32])
            
            if keys[0]:
                player.playerpos[0]-=10
            elif keys[1]:
                player.playerpos[0]+=10

            # 게임오버 / 게임승리 체크
            if player.hp<=0 or padlockToKey:
                gameOver = 1 # 게임종료
                gameLose=1
            if timeValue<=0:
                gameOver = 1
                gameWin=1

            pygame.display.flip()
            fpsClock.tick(FPS)

        if gameOver:
            handleGameOver(padlock,gameWin,gameLose)
        
startScreen()  
main()
