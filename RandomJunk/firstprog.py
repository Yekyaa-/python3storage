# for simple command-line arguments
from sys import argv
import time
from printpost import printPost
from TOH import TOHStart
MoveNumber = 0
OrigDiskCnt = 0

def parseBits(x):
    # Initialize counter to 1 (determines Disk Number that's moving on this move)
    diskNum = 1
    for c in reversed(x):
        if (c == '0'):
            diskNum = diskNum + 1
        elif (c == '1'):
            break
    print('move #',int(x,2),'disk #',diskNum,'/',len(x))
    d,s,t = calcData(len(x),int(x,2))
    print(d,':',s,'->',t)
    print(showPos(len(x),int(x,2)))
    print(getInDepthMove(len(x),int(x,2)))
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
    
# Given the number of disks and the requested move in range 0 -> (2 ** n) - 1 {2^n - 1}
# Explain the bit setting breakdown of each move.
def showPos(disks,m):
    # Initialize Variables
    ln = disks
    x = f'{m:b}'.zfill(ln)
    stackCounter = 0
    bit0 = 0
    currBit = 0
    previousBit = 0
    prevPost = 0
    thePlay = ""
    
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
            
    # Return the created string
    return thePlay
    
def getInDepthMove(disks,m):
    # Basic Error Checks
    # -- No Move Required @ Initial Position
    result = createPegArray(disks,m)

    if (m == 0):
        return 'No Move {0}'.format(result)

    # -- No Move Possible if m is larger than optimal move count
    if ((2 ** disks - 1) < m):
        return "Invalid move #{m} for {disks} disks (Range: 0 - {z}).".format(disks=disks,m=m,z=(2**disks)-1)
        
    # Determine source and destination posts (within range 0->2 +1 = 1->3)
    sourcePost = (m - (m & (-m))) % 3 + 1
    destPost   = (m + (m & (-m))) % 3 + 1
    
    # if Disk count is even, swap Post #2 and #3
    # since "final" post is #3 no matter disk count
    if (disks % 2 == 0) :
        if (sourcePost == 3):
            sourcePost = 2
        elif (sourcePost == 2):
            sourcePost = 3
        if (destPost == 3):
            destPost = 2
        elif (destPost == 2):
            destPost = 3

    # Create bitstring for move, padded with zeroes to fill 'disks' length
    x = f'{m:b}'.zfill(disks)
    
    resultMinus1 = createPegArray(disks,m-1)
    diskNum = 0

    for c in reversed(x):
        if (c == '0'):
            diskNum = diskNum + 1
        elif (c == '1'):
            break
    
    # Build and Return String
    return '({M}) disk {d} >{s}:{t} {x}-->{z}'.format(M=f'{m:b}'.zfill(disks),
                d=diskNum+1,s=sourcePost,t=destPost,x=resultMinus1,z=result)
    
def createPegArray(disks,m):
    x = f'{m:b}'.zfill(disks)
    thisList=[list(),list(),list()]
    thisList[0].clear()
    thisList[1].clear()
    thisList[2].clear()

    stackCounter = 0
    bit0 = 0
    currBit = 0
    previousBit = 0
    prevPost = 0
    for i,c in enumerate(x):
        # Convert character to 1 or 0
        currBit = 1 if c == '1' else 0
        # Handle largest disk first
        if (i == 0):
            stackCounter = 0
            bit0 = currBit
            previousBit = currBit
            # Largest Disk is either Initial position or Final Position
            prevPost = bit0 * 2
            thisList[prevPost].append(disks-i)
        elif (previousBit == currBit):
            thisList[prevPost].append(disks - i)
            stackCounter = stackCounter + 1
            # prevPost stays the same here
        else:
            calcMax = stackCounter + bit0
            prevPost = (prevPost + (-1 if (calcMax % 2 == 1) else 1)) % 3
            thisList[prevPost].append(disks-i)
            previousBit = currBit
    thisList[0].sort()
    thisList[1].sort()
    thisList[2].sort()
    return thisList
    
print("*" * 50)
value = argv[len(argv) - 1]
Disks = 5
try:
    Disks = int(value)
    print("Using Disks value of " + value)
except ValueError:
    print("Using Disks value of 5 (default)")
    
OrigDiskCnt = Disks    
if (Disks <= 15):
    s = time.perf_counter()
    t = time.process_time()
    #TOHStart(Disks)
    perf_elapsed = time.perf_counter() - s
    elapsed_time = time.process_time() - t
    print("*" * 50)
    print("Calculated :", (2 ** Disks) - 1, "moves to complete", Disks, "disks.")
    print("Process Time Required :",elapsed_time,"seconds.")
    print("System Time Required  :",perf_elapsed,"seconds.")
    #print("Wrong Counter         :",wrongCnt)
s = time.perf_counter()
t = time.process_time()
expD = 2**Disks
modD = Disks * Disks
for i in range(0,expD):
    #print(getInDepthMove(Disks,i))
    #print('{0[0]} : {0[1]} -> {0[2]}'.format(calcData(Disks,i)))
    print(getLayout(Disks,i))
    #if ((i % modD) == 0):
    #    print('.',end='',flush=True)
    #gz,hz,iz=calcData(Disks,i)

perf_elapsed = time.perf_counter() - s
elapsed_time = time.process_time() - t
#print(flush=True)
print()
print("*" * 50)
print("Process Time Required :",elapsed_time,"seconds.")
print("System Time Required  :",perf_elapsed,"seconds.")
#printPost(10,1022)
#printPost(10,1000)

d,s,t = calcData(10,1000)
#print(d,':',s,'->',t)
d,s,t = calcData(200,1)
#print(d,':',s,'->',t)
#parseBits(f'{10 ** 3 ** 2 ** 2:b}')
#help(calcData)
#CSI="\x1B["
#print (CSI+"31;40m" + u"\u2588" + CSI + "0m")