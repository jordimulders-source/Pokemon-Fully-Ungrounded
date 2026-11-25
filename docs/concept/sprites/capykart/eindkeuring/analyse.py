# Analyse buitencontour r6: huidige lijnkleur vs. gids-regel (boven/links = outline base, onder/rechts = zwart)
from PIL import Image
import sys
im=Image.open(sys.argv[1] if len(sys.argv)>1 else 'capykart/sprite/r6/capykart.png');px=im.load()
W=H=64
ch='.123456789ABCDEF'
def op(x,y): return 0<=x<W and 0<=y<H and px[x,y]!=0
GROUP={2:'bruin',3:'bruin',5:'bruin',6:'bruin',7:'metaal',15:'groen',11:'groen',12:'rood',13:'rood',10:'blauw',14:'geel',9:'wit'}
BASE={'bruin':4,'metaal':8,'groen':11,'rood':13,'blauw':8,'geel':None,'wit':7}
def group(x,y):
    from collections import Counter
    c=Counter()
    for r in (1,2):
        for dx in range(-r,r+1):
            for dy in range(-r,r+1):
                X,Y=x+dx,y+dy
                if op(X,Y) and px[X,Y] in GROUP: c[GROUP[px[X,Y]]]+=1.0/r
        if c: return c.most_common(1)[0][0]
    return '?'
out=[]
for y in range(H):
    for x in range(W):
        if not op(x,y): continue
        up=not op(x,y-1); dn=not op(x,y+1); lf=not op(x-1,y); rt=not op(x+1,y)
        if not(up or dn or lf or rt): continue
        g=group(x,y)
        side='schaduw' if (dn or (rt and not up)) else 'licht'
        want=1 if side=='schaduw' else BASE.get(g)
        cur=px[x,y]
        if cur!=want: out.append((x,y,ch[cur],g,side,ch[want] if want is not None else '?'))
for o in out: print(*o)
print(len(out))
