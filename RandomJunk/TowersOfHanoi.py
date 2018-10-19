# for simple command-line arguments
from sys import argv
import time

# Lists (Towers of Hanoi)
def init(cnt):
    theList=[list(range(1,cnt+1)),list(),list()]
    print('   START         :',theList)
    return theList

def update(Post, dsk,src,dst):
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
    print('Disk {dsk} to Post {dst} : {Post}'.format(dsk=dsk,dst=dst,Post=Post))
    return

def TOH(PostList, dsk,src,dst):
    if (dsk == 0):
        return
    # Assuming src + dst + spare = 6 (1+2+3=6)
    TOH(PostList, dsk-1,src,6-src-dst)
    #print('Disk {dsk} to {dst}'.format(dsk=dsk,src=src,dst=dst))
    update(PostList, dsk,src,dst)
    TOH(PostList, dsk-1,6-src-dst,dst)
    return
def TOHStart(dsk):
    PostList = init(dsk)
    TOH(PostList, dsk,1,3)
    return
def header():
	print("*" * 79)
	return

# Start	
value = argv[len(argv) - 1]
Disks = 5
try:
    Disks = int(value)
    print("Using Disks value of " + value)
except ValueError:
    print("Using Disks value of 5 (default)")
header()
s = time.perf_counter()
t = time.process_time()
TOHStart(Disks)
perf_elapsed = time.perf_counter() - s
elapsed_time = time.process_time() - t
header()
print("Calculated :", (2 ** Disks) - 1, "moves to complete", Disks, "disks.")
print("Process Time Required :",elapsed_time,"seconds.")
print("System Time Required  :",perf_elapsed,"seconds.")
