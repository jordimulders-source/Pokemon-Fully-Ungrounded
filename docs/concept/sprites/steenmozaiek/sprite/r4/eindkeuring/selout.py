# Voorstel selout (gekleurde buitenlijn aan de lichtkant) voor steenjaguar r4. Past de sprite NIET aan.
import sys
from PIL import Image
from collections import Counter
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/steenmozaiek/sprite/r4/'
im=Image.open(D+'steenjaguar_r4.png'); W,H=im.size; px=im.load()
g=lambda x,y: px[x,y] if 0<=x<W and 0<=y<H else 0
GROEP={7:2,8:2,10:3,11:3,13:12,14:12}   # licht/midden vlak -> selout; 2,6,3,9,4,5,12,15 -> blijft 1
def maak(cream=12):
    out=im.copy(); o=out.load(); voorstel={}
    for y in range(H):
        for x in range(W):
            if px[x,y]!=1: continue
            nb=[(dx,dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if g(x+dx,y+dy)==0]
            if not nb: continue
            if not any(d in((-1,0),(0,-1)) for d in nb): continue   # alleen lichtkant (boven/links)
            if 2<=x<=11 and 23<=y<=29: continue                       # muil/tanden: zwart
            binnen=[g(x+dx,y+dy) for dx,dy in((1,0),(0,1),(1,1),(-1,1),(1,-1),(-1,0),(0,-1)) if g(x+dx,y+dy) not in(0,1)]
            if not binnen: continue
            v=Counter(binnen).most_common(1)[0][0]
            if v in GROEP:
                c=GROEP[v]
                if c==12: c=cream
                voorstel[(x,y)]=c
    # geen om en om: losse gekleurde randpixels terug naar 1, zwarte gaatjes tussen gelijke kleur dichten
    for _ in range(2):
        for (x,y),c in list(voorstel.items()):
            buren=[voorstel.get((x+dx,y+dy)) for dx in(-1,0,1) for dy in(-1,0,1) if (dx,dy)!=(0,0)]
            if sum(1 for b in buren if b is not None)==0: del voorstel[(x,y)]
    for (x,y),c in voorstel.items():
        if c!=1: o[x,y]=c
    return out,voorstel
if __name__=='__main__':
    a,va=maak(12); a.save(D+'eindkeuring/selout_voorstel.png')
    a.resize((W*8,H*8),Image.NEAREST).save(D+'eindkeuring/selout_voorstel_8x.png')
    b,vb=maak(1); b.save(D+'eindkeuring/selout_voorstel_b.png')
    for naam,v in(('A',va),('B',vb)):
        per=Counter(v.values()); print(naam,dict(per),'van rand',sum(1 for y in range(H) for x in range(W) if px[x,y]==1 and any(g(x+dx,y+dy)==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))))
    for c in(2,3,12):
        print(c,sorted((y,x) for (x,y),k in va.items() if k==c))
