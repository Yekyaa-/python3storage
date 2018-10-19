for i in range(1,256):
    x = chr(i)
    if (i == 0):
        x = '()'
    elif (i == 7):
        x = '\\a'
    elif (i == 8):
        x = '\\b'
    elif (i == 9):
        x = '\\t'
    elif (i == 10):
        x = '\\n'
    elif (i == 13):
        x = '\\r'
    print('{0:8X}{0:5d}{1}'.format(i,x.rjust(5,' ')),end='')
    if (i % 5 == 0):
        print()
