import json,sys
ZONES={'onder de hoorns':(14,13,30,19),'oor links':(9,17,17,24),'oor rechts':(26,17,35,24),'rug':(22,29,48,37),'manen hals':(26,23,34,33),'poten':(9,44,52,63)}
def runs(RN):
    m=json.load(open(f'{RN}/grid.json')); g=m['grid']; OX,OY=m['OX'],m['OY']; H=len(g); W=len(g[0])
    op=lambda x,y: 0<=x<W and 0<=y<H and g[y][x]!='.'
    # rand = opake pixel met transparante 4-buur; ook tintgrens binnen (pixel met andere niet-lijn buurtint)
    best={z:[0,0] for z in ZONES}
    def zone(X,Y): return [z for z,(a,b,c,d) in ZONES.items() if a<=X<=c and b<=Y<=d]
    for kind in ('rand','tint'):
        for side in ((1,0),(-1,0),(0,1),(0,-1)):
            dx,dy=side
            def edge(x,y):
                if not op(x,y): return False
                if kind=='rand': return not op(x+dx,y+dy)
                return op(x+dx,y+dy) and g[y][x] not in '0A1' and g[y+dy][x+dx] not in '0A1' and g[y][x]!=g[y+dy][x+dx]
            if dx:   # verticale runs
                for x in range(W):
                    y=0
                    while y<H:
                        if edge(x,y):
                            y2=y
                            while y2+1<H and edge(x,y2+1) and (kind=='rand' or g[y2+1][x]==g[y][x]): y2+=1
                            for z in zone(x+OX,(y+y2)//2+OY): best[z][kind=='tint']=max(best[z][kind=='tint'],y2-y+1)
                            y=y2+1
                        else: y+=1
            else:
                for y in range(H):
                    x=0
                    while x<W:
                        if edge(x,y):
                            x2=x
                            while x2+1<W and edge(x2+1,y) and (kind=='rand' or g[y][x2+1]==g[y][x]): x2+=1
                            for z in zone((x+x2)//2+OX,y+OY): best[z][kind=='tint']=max(best[z][kind=='tint'],x2-x+1)
                            x=x2+1
                        else: x+=1
    return best
a=runs(sys.argv[1]); b=runs(sys.argv[2])
for z in ZONES: print(f'{z:16s} langste rechte run buitenrand {a[z][0]:2d} -> {b[z][0]:2d} | tintgrens {a[z][1]:2d} -> {b[z][1]:2d}')
