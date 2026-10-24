# Controle: open randen (vulkleur naast transparant) en rechte omtreklijnen >= 4 px.
import sys
r=[l.rstrip('\n').ljust(64,'.') for l in open(sys.argv[1])][:64]
g=lambda x,y: r[y][x] if 0<=x<64 and 0<=y<64 else '.'
open_=[(x,y) for y in range(64) for x in range(64) if g(x,y) not in '.12' and any(g(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen:',open_)
edge=lambda x,y: g(x,y)!='.' and any(g(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
# verticale runs van omtrekpixels in dezelfde kolom met transparant aan dezelfde kant
for side,(dx,dy) in (('links',(-1,0)),('rechts',(1,0))):
    for x in range(64):
        y=0
        while y<64:
            n=0
            while y+n<64 and g(x,y+n)!='.' and g(x+dx,y+n)=='.': n+=1
            if n>=4: print('verticaal',side,'x=%d y=%d-%d (%d)'%(x,y,y+n-1,n))
            y+=max(n,1)
for side,(dx,dy) in (('boven',(0,-1)),('onder',(0,1))):
    for y in range(64):
        x=0
        while x<64:
            n=0
            while x+n<64 and g(x+n,y)!='.' and g(x+n,y+dy)=='.': n+=1
            if n>=4: print('horizontaal',side,'y=%d x=%d-%d (%d)'%(y,x,x+n-1,n))
            x+=max(n,1)
