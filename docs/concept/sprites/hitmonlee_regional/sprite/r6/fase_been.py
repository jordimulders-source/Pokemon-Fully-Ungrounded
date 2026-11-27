# Proef: trapbeen (spriterijen 9-26) opnieuw bemonsteren met natieve fase-verschuiving (dy,dx in 0/1) en lijnregel md.
# Zelfde rij/kolomtoewijzing (keepr/keepc), alleen de 2x2-blokken schuiven 1 natieve pixel. Laat 8 opties naast het model zien.
from PIL import Image, ImageDraw; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import lab
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']'); PL=lab(np.array(PAL[1:],float))
RD=[4,8,13,17,22,28,45,55,64,70]; CD=[1,5,16,37,42,50,56,60,65]
keepr=[r for r in range(74) if r not in RD]; keepc=[c for c in range(68) if c not in CD]
nat=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float); nl=nat.mean(2)
def bouw(dy,dx,md,y0=9,y1=27,x0=33,x1=49):
    out=np.zeros((y1-y0,x1-x0),int)
    for y in range(y0,y1):
        for x in range(x0,x1):
            r=2*keepr[y]+dy; c=2*keepc[x]+dx
            blk=nat[r:r+2,c:c+2].reshape(-1,3); l=nl[r:r+2,c:c+2].ravel()
            if (blk.min(1)>=226).sum()>=3: continue
            fg=blk.min(1)<226; dk=(l<80)&fg
            col=blk[dk][l[dk].argmin()] if dk.sum()>=md else np.median(blk[fg&~dk],0)
            out[y-y0,x-x0]=int(((PL-lab(col))**2).sum(1).argmin())+1
    return out
opts=[(dy,dx,md) for md in (1,2) for dy in (0,1) for dx in (0,1)]
S=10; tiles=[]
for o in opts:
    a=bouw(*o); h,w=a.shape; im=Image.new('RGB',(w*S,h*S+14),'white'); d=ImageDraw.Draw(im)
    for y in range(h):
        for x in range(w):
            if a[y,x]: d.rectangle([x*S,y*S,x*S+S-1,y*S+S-1],fill=tuple(PAL[a[y,x]]))
    d.text((2,h*S+2),str(o),fill=(0,0,0)); tiles.append(im)
c=Image.new('RGB',(sum(t.width+6 for t in tiles),tiles[0].height),(150,150,150)); x=0
for t in tiles: c.paste(t,(x,0)); x+=t.width+6
c.save(sys.argv[1])
