print('Hello, world')

fileread = open('bigtest.hgr')
filewrite = open('bigtest0.hgr', 'w')

print(fileread.readline(), end='', file=filewrite)

for i in fileread:
    line = list(map(int,i.rstrip().split(' ')))
    for j in line:
        print(j-1, end=' ', file=filewrite)
    print(file=filewrite)
