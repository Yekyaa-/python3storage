import pygame
import time
import pygame.event
from pygame.locals import *
import random
#import drawAnalog

class Disk:
    
    pass
    
SPACE_PER_PEG = 200

def drawButton(screen, x, y, xc, yc):
    ''' Draw Analog Control Stick at (x,y) with offset (xc,yc) '''
    pygame.draw.circle(screen, Color(128,128,128), (x,y),50,0)
    pygame.draw.circle(screen, Color(0,0,0), (round(x+(xc*25)),round(y+(yc*25))),45,0)
    return

def display_footer(screen,position,base_width):
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h    
    myfontN = pygame.font.SysFont('monospace', 20)
    myfontS = pygame.font.SysFont('monospace', 14)
    Print1 = '{0}'.format(position[0])
    Print2 = '{0}'.format(position[1])
    Print3 = '{0}'.format(position[2])
    #Print1 = '{0}'.format(sorted([round(x/base_width) for x in position[0]]))
    #Print2 = '{0}'.format(sorted([round(x/base_width) for x in position[1]]))
    #Print3 = '{0}'.format(sorted([round(x/base_width) for x in position[2]]))
    if (len(Print3) > 20):
        ts3 = myfontS.render(Print3, False, (0,0,0))
    else:
        ts3 = myfontN.render(Print3,False,(0,0,0))
        
    if (len(Print2) > 20):
        ts2 = myfontS.render(Print2, False, (0,0,0))
    else:
        ts2 = myfontN.render(Print2,False,(0,0,0))
    if (len(Print1) > 20):
        ts1 = myfontS.render(Print1, False, (0,0,0))
    else:
        ts1 = myfontN.render(Print1,False,(0,0,0))
    # Center Text within Block
    # Start of Block = (if 1, 0+offset, if 2, offset + Width per Block, if 3, offset + Width per Block * 2)
    # This may require more additions of variables if we account for "space/padding between blocks, etc"
    Start1 = 50
    Start2 = 50 + SPACE_PER_PEG
    Start3 = 50 + SPACE_PER_PEG*2
    # Start of Block + (Width per Block - Width of Text) / 2
    x_1 = Start1 + (SPACE_PER_PEG - ts1.get_width()) / 2
    x_2 = Start2 + (SPACE_PER_PEG - ts2.get_width()) / 2
    x_3 = Start3 + (SPACE_PER_PEG - ts3.get_width()) / 2
    screen.blit(ts1,(x_1,550))
    screen.blit(ts2,(x_2,550))
    screen.blit(ts3,(x_3,550))
    return

def display_pile(pegs, width, start_x, start_y, peg_height, screen):
    for c, peg in enumerate(pegs):
        for i, diskNum in enumerate(peg):
            drawDisk(diskNum, width, start_x, start_y, c, peg_height, screen, len(peg)-i)
    return

def drawDisk(num, width, start_x, start_y, peg_num, peg_height, screen, height_mod):
    dw = num*width
    rect = (
            start_x+SPACE_PER_PEG*peg_num + (SPACE_PER_PEG - dw)/2 ,
            start_y - peg_height * height_mod,
            dw,
            peg_height
           )
 
    pygame.draw.rect(
        screen,
        Color(((num+1)%3*width)%255,((num-1)%5*width)%255,(num%3*width)%255,255),
        rect
    )
    
    return
    
def animate(prev, next, d, m):
    disk, source, dest = calcData(d, m)
    
    
    if (prev != next):
        pass
    #else:
        #print("EQUAL")
    return
    
def calcData(d,m):
    '''Return tuple containing Disk, Source Peg, Destination Peg for Move m for Disks d'''
    # Determine source and destination posts (within range 0->2 +1 = 1->3)
    sourcePost = (m - (m & (-m))) % 3 + 1
    destPost   = (m + (m & (-m))) % 3 + 1

    # if Disk count is even, swap Post #2 and #3
    # since "final" post is #3 no matter disk count
    if (d % 2 == 0) :
        if (sourcePost == 3):
            sourcePost = 2
        elif (sourcePost == 2):
            sourcePost = 3
        if (destPost == 3):
            destPost = 2
        elif (destPost == 2):
            destPost = 3

    # Create bitstring for move, padded with zeroes to fill 'd' length
    x = f'{m:b}'.zfill(d)

    # Initialize counter to 1 (determines Disk Number that's moving on this move)
    diskNum = 1
    for c in reversed(x):
        if (c == '0'):
            diskNum = diskNum + 1
        elif (c == '1'):
            break
    
    return diskNum,sourcePost,destPost
    
def visual_toh_sim(number_of_pegs, base_width, peg_height, sleeping_interval):
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) )
    pygame.display.set_caption('BETTER Towers of Hanoi ({0} Disks)'.format(number_of_pegs))
    pygame.font.init()
    done = False
    origVal = sleeping_interval
    optMoves = 2 ** number_of_pegs - 1
    prevpile = getLayout(number_of_pegs, 0)
    for i in range(0,optMoves+1):
        done = inputLoop()
        if (done == K_DOWN):
            sleeping_interval=0
        elif (done == K_UP):
            sleeping_interval = origVal
        elif (done == QUIT):
            pygame.quit()
            return QUIT
        screen.fill((255, 255, 255)) 
        pegs = getLayout(number_of_pegs, i)
        animate(prevpile, pegs, number_of_pegs, i)
        prevpile = pegs
        display_pile(pegs, base_width, 50,500,peg_height,screen)
        display_footer(screen,pegs,base_width)
        drawButton(screen, 100, 100, (random.random() * 2) - 1, (random.random() * 2) - 1)
        pygame.display.update()
        #time.sleep(sleeping_interval)
        pygame.time.delay(round(sleeping_interval))

    while (inputLoop() != QUIT):
        # do nothing
        pass
    pygame.quit()
    return QUIT
    
def inputLoop():
    done = None
    for event in pygame.event.get():
        if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
            done = QUIT
            pygame.quit()
            break
        elif (event.type == KEYUP and event.key == K_UP):
            return K_UP
        elif event.type == KEYUP and event.key == K_DOWN:
            return K_DOWN
    return done

def functionT(time, src, dst):

    return
    
def getLayout(disks, m):
    ln = disks
    x = f'{m:b}'.zfill(ln)
    stackCounter = 0
    bit0 = 0
    currBit = 0
    previousBit = 0
    prevPost = 0
    thePlay = ""
    theList = [list(),list(),list()]
    # For each character in the bitstring
    for i,c in enumerate(x):
        # Convert character to 1 or 0
        currBit = 1 if c == '1' else 0
        
        # if this is the first bit (largest disk)
        if (i == 0):
            # Establish opening values
            stackCounter = 0
            bit0 = currBit
            previousBit = currBit
            
            # Establish start of string
            thePlay = '{dsk}({p})'.format(dsk=ln-i,p='I' if bit0 == 0 else 'F')

            # Establish post for largest disk as either initial (I) or final post (F)
            prevPost = bit0 * 2            
        # if previous disk is in same location as current disk (Second disk in stack)
        elif (previousBit == currBit):
            # prevPost stays the same here

            # Add 1 to stack counter
            stackCounter = stackCounter + 1
            
            # Show that current disk is stacked
            thePlay = thePlay + ' >>{dsk}(S)'.format(dsk=ln-i)
        # if not largest disk, and new disk is not stacked on previous
        else:
            # Add 1 to stacked disk counter if largest disk is on final post.
            calcMax = stackCounter + bit0
            
            # If calcMax is odd, move left of previous post (with wraparound)
            # If calcMax is even, move right of previous post (with wraparound)
            prevPost = (prevPost + (-1 if (calcMax % 2 == 1) else 1)) % 3
            
            # Show that current disk is not stacked, but on a different post
            thePlay = thePlay + ' >>{dsk}(D,{Z}+{M},{dir}{to})'.format(dsk=ln-i,p='x',
                        Z=bit0,M=calcMax-bit0,dir='L' if (calcMax % 2) == 1 else 'R',to=prevPost+1)
                        
            # Establish values for next iteration
            previousBit = currBit
        theList[prevPost].append(disks-i)
    theList[0].sort()
    theList[1].sort()
    theList[2].sort()
    # Return the created string
    return theList
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    visual_toh_sim(
        number_of_pegs = 7,
        base_width = 30,
        peg_height = 40,
        sleeping_interval = 500
    )
    visual_toh_sim(
        number_of_pegs = 8,
        base_width = 20,
        peg_height = 30,
        sleeping_interval = 200
    )
#    visual_toh_sim(
#        number_of_pegs = 11,
#        base_width = 20,
#        peg_height = 30,
#        sleeping_interval = 0.001
#    )
exit()