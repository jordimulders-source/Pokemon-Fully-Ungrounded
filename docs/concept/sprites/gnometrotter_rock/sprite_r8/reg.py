# reg.py x0 y0 x1 y1 : print region of grid.txt with header ; reg.py put x0 y0 file : write rows from file into grid
import sys
G=[list(l.rstrip('\n')) for l in open('grid.txt') if l.strip()]
if sys.argv[1]=='put':
    x0,y0=int(sys.argv[2]),int(sys.argv[3]); rows=[l.rstrip('\n') for l in open(sys.argv[4]) if l.strip()]
    for j,r in enumerate(rows):
        r=r.split()[-1]
        for i,c in enumerate(r):
            old=G[y0+j][x0+i]
            if (old=='.')!=(c=='.'): print('SILHOUET!',x0+i,y0+j,old,c)
            G[y0+j][x0+i]=c
    open('grid.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
else:
    x0,y0,x1,y1=map(int,sys.argv[1:5])
    print('    '+''.join(str(x//10) for x in range(x0,x1)));print('    '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d  '%y+''.join(G[y][x0:x1]))
