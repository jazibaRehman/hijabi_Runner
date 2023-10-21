import pygame, sys
from random import randint


def displayScore():
    currTime = int(pygame.time.get_ticks()/ 1000) - startTime
    scoreSurf = testFont.render(f"Score: {currTime}", False, (64, 64, 64))
    scoreRect = scoreSurf.get_rect(center = (400, 50))
    screen.blit(scoreSurf, scoreRect)
    return currTime

def obstacleMovement(obstacleList):
    if obstacleList:
        for obstacleRect in obstacleList:
            obstacleRect.x -= 5
            
            if obstacleRect.bottom == 300:               
                screen.blit(snailSurface, obstacleRect)
            else:
                screen.blit(flySurface, obstacleRect)
                
            
        obstacleList = [obstacle for obstacle in obstacleList if obstacle.x > -100]
            
        return obstacleList
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstaclesRect in obstacles:
            if player.colliderect(obstaclesRect):
                return False
            
    return True
                

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Hijabi Runner")
clock = pygame.time.Clock()
testFont = pygame.font.Font("font/Pixeltype.ttf", 50)
gameActive = False
startTime = 0
score = 0

#sky
skySurface = pygame.image.load("graphics/Sky.png").convert()
skyXPosition = 0

#ground and text
groundSurface = pygame.image.load("graphics/ground.png").convert()
    #scoreSurface = testFont.render("My Game", False, (64,64,64)).convert()
    #scoreRect = scoreSurface.get_rect(center = (400, 50))

#snail the obstacle
snailSurface = pygame.image.load("graphics/snail1.png").convert_alpha()
snailRect = snailSurface.get_rect(bottomright = (600, 300))

flySurface = pygame.image.load("graphics/fly1.png").convert_alpha()

obstacleRectList = []



#player
playerSurface = pygame.image.load("graphics/player_walk_1.png").convert_alpha()
playerRect = playerSurface.get_rect(midbottom = (80, 300))
playerGravity = 0

#intro screen
playerStand = pygame.image.load("graphics/player_stand.png").convert_alpha()
playerStand = pygame.transform.scale2x(playerStand)
playerStandRect = playerStand.get_rect(center = (400, 200))

introText = testFont.render("Hijabi Runner", False, (64, 64, 64))
introText = pygame.transform.scale2x(introText)
introTextRect = introText.get_rect(midbottom = (400, 100))

#Timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1500)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if gameActive:    
            if event.type == pygame.MOUSEBUTTONDOWN and playerRect.bottom == 300:
                if playerRect.collidepoint(event.pos):
                    playerGravity = -20
                
            if event.type == pygame.KEYDOWN and playerRect.bottom == 300:
                if event.key == pygame.K_SPACE :
                    playerGravity = -20
                    
                    
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                startTime = int(pygame.time.get_ticks()/ 1000)
                
        if event.type == obstacleTimer and gameActive:
            if randint(0,2):
                obstacleRectList.append(snailSurface.get_rect(bottomright = (randint(900, 1100), 300)))
            else:
                obstacleRectList.append(flySurface.get_rect(bottomright = (randint(900, 1100), 200)))

    #game
    if gameActive:
        screen.blit(skySurface, (skyXPosition,0))  
        screen.blit(groundSurface, (0,300))
        #pygame.draw.rect(screen, "#c0e8ec", scoreRect)
        #pygame.draw.rect(screen, "#c0e8ec", scoreRect, 10)
        #screen.blit(scoreSurface, scoreRect)
        score = displayScore()
        
        #snailRect.x -= 4
        #if snailRect.right <= 0:
        #    snailRect.left = 800
        #screen.blit(snailSurface, snailRect)
        #playerRect.left += 1
        #player
        playerGravity += 1
        playerRect.y += playerGravity
        if playerRect.bottom >= 300:
            playerRect.bottom = 300
            
        #if playerRect.top <= 0:
        #    playerRect.top = 0
        screen.blit(playerSurface, playerRect)
        
        #obstacle Movement
        obstacleRectList = obstacleMovement(obstacleRectList)
        
        #keys = pygame.key.get_pressed()
        
        #print(playerRect.colliderect(snailRect))#
        #if playerRect.colliderect(snailRect):
        #    print("Collision") 
        
        
       # mousePosition = pygame.mouse.get_pos()
       # if playerRect.collidepoint((mousePosition)):
       #     print(pygame.mouse.get_pressed())
        
        
        #collision
        #if snailRect.colliderect(playerRect):
         #   gameActive = False
        
        gameActive = collisions(playerRect, obstacleRectList)
    
    #menu
    else:
        screen.fill((245, 191, 217))
        obstacleRectList.clear()
        playerRect.midbottom = (80, 300)
        playerGravity = 0
        scoreMessage = testFont.render(f"Your Score: {score}", False, (64, 64, 64))
        scoreMessageRect = scoreMessage.get_rect(midbottom = (400, 350))
        screen.blit(playerStand, playerStandRect)
        screen.blit(introText, introTextRect)
        screen.blit(scoreMessage, scoreMessageRect)
        

    
    pygame.display.update()
    clock.tick(60)

    