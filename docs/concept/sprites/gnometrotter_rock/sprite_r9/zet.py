# zet.py file : lines 'y x0 string' -> overwrite grid (no silhouette change allowed)
import sys
G=[list(l.rstrip('\n')) for l in open('grid.txt') if l.strip()]
bad=0
for l in open(sys.argv[1]):
    l=l.split('#')[0].split()
    if len(l)<3: continue
    y,x0,s=int(l[0]),int(l[1]),l[2]
    for i,c in enumerate(s):
        old=G[y][x0+i]
        if (old=='.')!=(c=='.'): print('SILHOUET!',x0+i,y,old,c); bad=1
        G[y][x0+i]=c
if not bad: open('grid.txt','w').write('\n'.join(''.join(r) for r in G)+'\n'); print('ok')
