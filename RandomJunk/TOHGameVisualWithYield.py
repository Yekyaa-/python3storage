import pygame
import time
import pygame.event
from pygame.locals import *

SPACE_PER_PEG = 200

def hanoi(pegs, start, target, n):
    """
    From stackoverflow:
      http://stackoverflow.com/questions/23107610/towers-of-hanoi-python-understanding-recursion
      http://stackoverflow.com/questions/41418275/python-translating-a-printing-recursive-function-into-a-generator

    This function, given a starting position of an hanoi tower, yields
    the sequence of optimal steps that leads to the solution.

    >>> for position in hanoi([ [3, 2, 1], [], [] ], 0, 2, 3): print(position)
    [[3, 2], [], [1]]
    [[3], [2], [1]]
    [[3], [2, 1], []]
    [[], [2, 1], [3]]
    [[1], [2], [3]]
    [[1], [], [3, 2]]
    [[], [], [3, 2, 1]]

    """
    assert len(pegs[start]) >= n, 'not enough disks on peg'
    if n == 1:
        pegs[target].append(pegs[start].pop())
        yield pegs
    else:
        aux = 3 - start - target  # start + target + aux = 3
        for i in hanoi(pegs, start, aux, n-1): yield i
        for i in hanoi(pegs, start, target, 1): yield i
        for i in hanoi(pegs, aux, target, n-1): yield i

def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen):
    """
    Given a pile of pegs, displays them on the screen, nicely inpilated
    like in a piramid, the smaller in lighter color.
    """
    for i, pegwidth in enumerate(pegs):

        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            (255-pegwidth, 255-pegwidth, 255-pegwidth),
            (
              start_x + (SPACE_PER_PEG - pegwidth)/2 , # Handles alignment putting pegs in the middle, like a piramid
              start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration
              pegwidth,
              peg_height
            )

        )

def display_footer(screen,position,base_width):
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h    
    myfontN = pygame.font.SysFont('monospace', 20)
    myfontS = pygame.font.SysFont('monospace', 14)
    Print1 = '{0}'.format(sorted([round(x/base_width) for x in position[0]]))
    Print2 = '{0}'.format(sorted([round(x/base_width) for x in position[1]]))
    Print3 = '{0}'.format(sorted([round(x/base_width) for x in position[2]]))
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

def visual_hanoi_simulation(number_of_pegs, base_width, peg_height, sleeping_interval):
    """
    Visually shows the process of optimal solution of an hanoi tower problem.
    """
    pegs = [[i * base_width for i in reversed(range(1, number_of_pegs+1))], [], []]
    positions = hanoi(pegs, 0, 2, number_of_pegs)
    orig_val = sleeping_interval
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) )
    pygame.display.set_caption('Towers of Hanoi')
    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    for position in positions:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_DOWN):
                sleeping_interval = 0
            elif (event.type == KEYDOWN and event.key == K_UP):
                sleeping_interval = orig_val
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
        screen.fill((255, 255, 255)) 
        for i, pile in enumerate(position):
            display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen)
        display_footer(screen,position,base_width)
        pygame.display.update()
        pygame.time.delay(round(sleeping_interval*1000))

    while True:
        for event in pygame.event.get():
            if (event.type == KEYUP):
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    visual_hanoi_simulation(
        number_of_pegs = 7,
        base_width = 30,
        peg_height = 40,
        #sleeping_interval = 0.05                                 
        sleeping_interval = 1
    )
    visual_hanoi_simulation(
        number_of_pegs = 8,
        base_width = 20,
        peg_height = 30,
        sleeping_interval = .5
    )
    visual_hanoi_simulation(
        number_of_pegs = 11,
        base_width = 20,
        peg_height = 30,
        sleeping_interval = 0.0625
    )
exit()