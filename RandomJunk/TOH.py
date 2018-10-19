MoveNumber = 0
OrigDiskCnt = 0
# Lists (Towers of Hanoi)
def init(cnt):
    theList=[list(range(1,cnt+1)),list(),list()]
    print('   START         :',theList)
    return theList

def TOHStart(dsk):
    global OrigDiskCnt
    OrigDiskCnt = dsk
    PostList = init(dsk)
    TOH(PostList, dsk,1,3)
    return 

def update(Post, dsk,src,dst):
    global MoveNumber
    global OrigDiskCnt

    # Lists are sequenced starting at 0
    if (dsk in Post[6-src-dst-1]):
        Post[6-src-dst].remove(dsk)
        Post[6-src-dst].sort()
    if (dsk in Post[src-1]):
        Post[src-1].remove(dsk)
        Post[src-1].sort()
    if (dsk not in Post[dst-1]):
        Post[dst-1].append(dsk)
        Post[dst-1].sort()

    MoveNumber = MoveNumber + 1
    m = MoveNumber
    
    sourcePost = (m - (m & (-m))) % 3 + 1
    destPost = (m + (m & (-m))) % 3 + 1
    if (OrigDiskCnt % 2 == 0) :
        if (sourcePost == 3):
            sourcePost = 2
        elif (sourcePost == 2):
            sourcePost = 3
        if (destPost == 3):
            destPost = 2
        elif (destPost == 2):
            destPost = 3
    print('Disk {dsk} to Post {dst} : {Post}'.format(dsk=dsk,dst=dst,Post=Post))
    #wrongCnt = wrongCnt + (0 if Post == createPegArray(OrigDiskCnt,m) else 1)
    return

def TOH(PostList, dsk,src,dst):
    if (dsk == 0):
        return
    # Assuming src + dst + spare = 6 (1+2+3=6)
    TOH(PostList, dsk-1,src,6-src-dst)

    update(PostList, dsk,src,dst)

    # Assuming src + dst + spare = 6 (1+2+3=6)
    TOH(PostList, dsk-1,6-src-dst,dst)
    return
    