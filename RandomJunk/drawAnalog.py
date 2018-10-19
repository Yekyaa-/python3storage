import pygame
#from pygame import Color
from pygame.locals import *

def drawButton(screen, x, y, xc, yc):
    ''' Draw Analog Control Stick at (x,y) with offset (xc,yc) '''
    pygame.draw.circle(screen, Color(0,0,0), (x,y),50,0)
    pygame.draw.circle(screen, Color(128,128,128), (round(x+(xc*33)),round(y+(yc*33))),45,5)
    return

def clamp(n, min, max):
    if (n < min):
        return min
    elif (n > max):
        return max
    return n
    
def main():
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) )
    pygame.display.set_caption('Draw Demos')
    pygame.font.init()
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h    
    done = False
    deltaX = 0
    deltaY = 0
    d = 0.075
    pygame.event.set_grab(True)

    while not done:
        #pygame.time.Clock().tick(120)
        clock.tick_busy_loop(120)
        screen.fill((255, 255, 255)) 
        #pygame.draw.polygon(screen, (128,128,79), [(200,100),(100,300),(550,10),(250,250)],0)
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        done,modx,mody = inputLoop()
        dirPressed = 0
        if keys[pygame.K_UP]:
            mody += -d
            dirPressed += 1
        if keys[pygame.K_DOWN]:
            mody += d
            dirPressed += 1
        if keys[pygame.K_LEFT]:
            modx += -d
            dirPressed += 1
        if keys[pygame.K_RIGHT]:
            modx += d
            dirPressed += 1
        #print(delay, deltaX, deltaY, modx, mody)
        # if none of the 4 keys are pressed, simulate "neutral"
        if (dirPressed <= 0):
            deltaX = 0
            deltaY = 0
        else:
            deltaX = clamp(deltaX + modx, -1.0, 1)
            deltaY = clamp(deltaY + mody, -1.0, 1)
        drawButton(screen, width//2, height//2, deltaX, deltaY)
        myfontN = pygame.font.SysFont('monospace', 20)
        fps = round(clock.get_fps())
        txt = myfontN.render(f'{fps}', False, (0,0,0))
        screen.blit(txt,(0,0))
        pygame.display.update()
    pygame.event.set_grab(False)

    return
    
def inputLoop():
    for event in pygame.event.get():
        #print(event)
        if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
            done = QUIT
            pygame.quit()
            return True,0,0
        elif event.type == KEYDOWN:
            if (event.key == K_TAB and pygame.key.get_mods() & KMOD_ALT):
                print("ALT-TAB!!")
        # elif event.type == KEYUP or event.type == KEYDOWN:
            # if (event.key == K_UP):
                # return False,0,-0.05
            # elif event.key == K_DOWN:
                # return False,0,0.05
            # elif event.key == K_LEFT:
                # return False,-0.05,0
            # elif event.key == K_RIGHT:
                # return False,0.05,0
    return False,0,0
    
main()