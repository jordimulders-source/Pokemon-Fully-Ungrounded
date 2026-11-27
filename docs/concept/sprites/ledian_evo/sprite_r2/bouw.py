# Ledian-evolutie r2 (kleurronde): vorm en kleurverdeling = r1 (bevroren); alleen tinten naar de Gen 3-Ledian
# (graphics/pokemon/ledian/normal_gba.pal), rood "net iets roder" (Jordi). Vanuit de repo-root draaien.
# Stappen:
#  1. Per r1-index de Ledian-tint (1-op-1: het model bepaalt per pixel licht/midden/schaduw, wij kiezen alleen de tint).
#  2. Donkergrijze BINNENLIJNEN (1 px dik, minstens 2 rode buren, geen 2x2-blok donker = geen vlek/band) -> donkerste rode tint (selout).
#  3. Buitenlijn aan de lichtkant (zwart met transparant boven/links en niet onder/rechts, grenst aan rood) -> rode selout.
#  Rode ramp: Ledians ramp met de hue een paar graden lager (zelfde S en V), varianten a/b/c; b = hoofdversie.
import numpy as np, colorsys, sys
from PIL import Image
R1='docs/concept/sprites/ledian_evo/sprite_r1/ledian_evo_r1.png'
D='docs/concept/sprites/ledian_evo/sprite_r2/'
a=np.array(Image.open(R1)); H=W=64
RED={7,8,9,10}; DK={1,2,3}
def g(y,x): return a[y,x] if 0<=y<H and 0<=x<W else 0
N4=((1,0),(-1,0),(0,1),(0,-1))

s=a.copy(); log=[]
# 2. binnenlijnen donkergrijs -> rode selout (7)
for y in range(H):
    for x in range(W):
        if a[y,x]!=2: continue
        nr=sum(g(y+dy,x+dx) in RED for dy,dx in N4)
        blok=any(all(g(y+i,x+j) in DK for i in(0,oy) for j in(0,ox)) for oy in(-1,1) for ox in(-1,1))
        if nr>=2 and not blok: s[y,x]=7; log.append((y,x,'binnenlijn d->rode selout'))
# 3. buitenlijn lichtkant
for y in range(H):
    for x in range(W):
        if a[y,x]!=1: continue
        up_l=g(y-1,x)==0 or g(y,x-1)==0
        dn_r=g(y+1,x)==0 or g(y,x+1)==0
        if not up_l or dn_r: continue
        nb=[g(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy,dx)!=(0,0)]
        nb=[v for v in nb if v not in(0,1)]
        if nb and sum(v in RED for v in nb)*2>len(nb): s[y,x]=7; log.append((y,x,'buitenlijn lichtkant K->rode selout'))

def shift(rgb,deg):
    h,sat,v=colorsys.rgb_to_hsv(*[c/255 for c in rgb]); h=(h-deg/360)%1
    return tuple(int(round(c*255)) for c in colorsys.hsv_to_rgb(h,sat,v))
LEDIAN_ROOD=[(131,49,16),(197,57,16),(255,90,32),(255,197,131)]   # selout, schaduw, basis, licht
VARIANTEN={'a':5,'b':8,'c':11}   # graden roder dan Ledian
def palet(deg):
    r=[shift(c,deg) for c in LEDIAN_ROOD]
    return [(0,0,0),            # 0 transparant
     (16,16,16),                # 1 zwart (Ledian)
     (57,57,57),                # 2 donkergrijs (sprieten, gewrichten, stippen, vleugelband); Ledian heeft geen tussentint, 2a->39
     (106,106,106),             # 3 grijs (Ledian)
     (180,180,180),(213,213,213),(255,255,255),   # 4-6 vuist schaduw/midden/wit (Ledian)
     r[0],r[1],r[2],r[3],       # 7-10 rood selout/schaduw/basis/licht
     (246,230,115),(205,180,57)]  # 11 geel licht, 12 goud (Ledian)
def save(arr,pal,fn):
    im=Image.fromarray(arr.astype('uint8'),'P'); flat=[c for p in pal for c in p]; flat+=[0]*(768-len(flat))
    im.putpalette(flat); im.save(D+fn,transparency=0)
for k,deg in VARIANTEN.items():
    save(s,palet(deg),f'rood_{k}.png')
    print(k,['%02x%02x%02x'%c for c in palet(deg)[7:11]])
save(s,palet(VARIANTEN['b']),'ledian_evo_r2.png')
# bewijs
assert ((a==0)==(s==0)).all(), 'silhouet gewijzigd'
print('silhouetdiff',int(((a==0)!=(s==0)).sum()),'kleuren',len(set(s.flatten())),'indexwijzigingen',int((a!=s).sum()))
from collections import Counter
print(Counter(w for _,_,w in log))
