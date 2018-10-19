# Display Post Arrays Based on Move Number
def printPost(disks,m):
    # Create Locals
    thisList=[list(),list(),list()]
    x = f'{m:#b}'.zfill(disks)
    ln = disks

    if ('b' in x) :
        x = f'{m:b}'.zfill(disks)

    # Show bit value
    print('#{m}({x})'.format(m=m,x=x),end='')
    
    
    previousBit = 0
    stackCounter = 0
    calcMax = 0
    bit0 = 0
    prevPost = 0
    thisList[0].clear()
    thisList[1].clear()
    thisList[2].clear()
    
    for i,c in enumerate(x):
        # Convert character to 1 or 0
        currBit = 1 if c == '1' else 0
        # Handle largest disk first
        if (i == 0):
            stackCounter = 0
            bit0 = currBit
            previousBit = currBit
            # Largest Disk is either Initial position or Final Position
            prevPost = bit0 if bit0 == 0 else 2
            thisList[prevPost].append(ln-i)
            print('{dsk}({p})'.format(dsk=ln-i,p='I' if bit0 == 0 else 'F'),end='')
        elif (previousBit == currBit):
            thisList[prevPost].append(ln - i)
            stackCounter = stackCounter + 1
            print('>{dsk}({p})'.format(dsk=ln-i,p='S'),end='')
        else:
            calcMax = stackCounter + bit0
            # i != 0 && previousBit != currBit
            prevPost = (prevPost + 1 + (calcMax % 2)) % 3
            #else:
             #   prevPost = (prevPost + 1) % 3
            thisList[prevPost].append(ln-i)
            print('>{dsk}({p},{M},{dir})'.format(dsk=ln-i,p='D',M=calcMax,dir='L' if (calcMax % 2) == 1 else 'R'),end='')
            previousBit = currBit
            
    print('  ',end='')
    thisList[0].sort()
    thisList[1].sort()
    thisList[2].sort()
    print(thisList)
    return
#printPost(10,1000)