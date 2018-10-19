import time
size = 61

for i in range(0,100):
    num = round(size*(i+1)/100)
    print('\rInstalling [{0}] {1}%'.format(('*' * num).ljust(size),i+1),end='')
    time.sleep(0.025)
print('...DONE')