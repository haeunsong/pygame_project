import pygame 
from setting import *

def startScreen():
    keyC = False
    while True:
        screen.fill((0,0,0))
        font = pygame.font.Font(None,100)
        title = font.render("Defend Padlock",True,(0,198,255))
        title_rect = title.get_rect()
        title_rect.center = (400,80)
        screen.blit(title,title_rect.topleft)

        font = pygame.font.Font(None,40)
        winText = font.render("WIN --> ",True,(0,255,0))
        loseText = font.render("LOSE --> ",True,(255,0,0))
        secondText = font.render("Defend for 90 seconds",True,(255,255,255))
        thirdText = font.render("All padlocks -> keys or Player dies",True,(255,255,255))
        pressText = font.render("Press c to continue...",True,(255,255,0))
        screen.blit(winText,(90,200))
        screen.blit(loseText,(90,260))
        screen.blit(secondText,(250,200))
        screen.blit(thirdText,(250,260))
        screen.blit(pressText,(250,380))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    keyC = True 
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_c:
                    keyC=False 
        if keyC:
            break

def drawStar(padlock):
    starx=[]
    plus=30
    for index in range(padlock.count):
        starx.insert(index,140+plus)
        plus += 100
    for x in starx:
        screen.blit(star,(x,130))

def handleGameOver(padlock,gameWin,gameLose):
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pass

            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    pass

        font = pygame.font.Font(None,80)

        if gameWin:
            text = font.render("!!CONGRATULATION!!",True,(51,255,0),(0,0,0))
            drawStar(padlock)
                
        elif gameLose:
            text = font.render("!!GAME OVER!!",True,(255,0,0),(0,0,0))
            screen.blit(sad,(290,135))
            screen.blit(sad,(410,135))

        text_rect = text.get_rect()
        text_rect.center = (400,250)
        screen.blit(text,text_rect.topleft)

        pygame.display.flip()
        fpsClock.tick(FPS)