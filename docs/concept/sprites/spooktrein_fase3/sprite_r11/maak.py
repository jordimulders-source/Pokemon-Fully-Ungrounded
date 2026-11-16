# r11: alleen de koeienvanger (y45-61, x0-22) uit het model op treinschaal; rest = r10 (groen diff 0).
import sys; sys.path.insert(0,'sprite_r11')
from basis import B, soort
from PIL import Image; import numpy as np
from collections import Counter
im=Image.open('sprite_r10/sprite.png'); a=np.array(im); r10=a.copy()
G={2,3,4,5,6,13}; IJ={1,7,8,9,10,11,12}
def roestzone(x,y): # band/V + 3 vlekken waar het model het meeste roest heeft
    return y<=48 or (9<=x<=14 and y<=50) or (4<=x<=5 and 49<=y<=55) or (12<=x<=15 and 51<=y<=57) or (18<=x<=20 and 52<=y<=55)
Z=[(x,y) for y in range(45,62) for x in range(0,23)]
for x,y in Z:
    if a[y,x] in G: continue
    s=soort(B[y,x])
    if s in ('.','g'): a[y,x]=0; continue
    k,L=s
    if k=='R' and roestzone(x,y): a[y,x]=8 if L>=62 else 9
    elif k=='R': a[y,x]=12  # roestspikkel buiten de vlekken: donkergrijs
    else: a[y,x]=1 if L<45 else 12 if L<85 else 11 if L<120 else 10 if L<150 else 7
# y45-47 hoort bij de band onder de grijns: daar r10 houden, behalve het silhouet links
for y in (45,46,47):
    for x in range(5 if y<47 else 11,23):
        if r10[y,x] in IJ: a[y,x]=r10[y,x]
# 1-px-ruis: losse grijs/roesttint neemt de meest voorkomende buurtint (zelfde groep) aan; 2 rondes
grijs={7,10,11,12}; roest={8,9}
for _ in range(2):
    b=a.copy()
    for x,y in Z:
        v=a[y,x]
        if v not in grijs|roest: continue
        nb=[a[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0)) if 0<=y+dy<64 and 0<=x+dx<64]
        if v in nb: continue
        grp=grijs if v in grijs else roest
        c=Counter(n for n in nb if n in grp)
        if c: b[y,x]=c.most_common(1)[0][0]
    a=b
# buitenlijn: ijzer naast transparant (of naast groen onderaan) wordt zwart
b=a.copy()
for x,y in Z:
    if a[y,x] in IJ and a[y,x]!=1:
        for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
            Y,X=y+dy,x+dx
            if not(0<=Y<64 and 0<=X<64) or a[Y,X]==0 or (a[Y,X] in G and Y>y): b[y,x]=1; break
a=b
# losse zwarte binnenpixels (geen zwarte 4-buur, geheel omringd door ijzer) -> donkergrijs; spleten blijven
b=a.copy()
for x,y in Z:
    if a[y,x]==1 and 0<x<63 and y<63:
        nb=[a[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0))]
        dg=[a[y+dy,x+dx] for dy,dx in((1,1),(1,-1),(-1,1),(-1,-1))]
        if 1 not in nb and all(n in IJ for n in nb) and 1 not in dg: b[y,x]=12
a=b
# losse tintpixels na de buitenlijn samenvoegen (zelfde groep, buurkleur)
for (x,y),v in {(12,51):8,(20,52):11,(19,53):8,(20,54):12,(22,48):11,(19,48):9}.items(): a[y,x]=v
a[53,11]=1  # gat (model wit tussen bladen) dicht
assert all(a[y,x]==r10[y,x] for y in range(64) for x in range(64) if r10[y,x] in G or a[y,x] in G)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('sprite_r11/sprite.png',transparency=0)
print('   '+''.join(str(x%10) for x in range(26)))
for y in range(42,62): print('%2d '%y+''.join('g' if v in G else '.' if v==0 else '%X'%v for v in a[y,:26]))
print('gewijzigd t.o.v. r10',int((a!=r10).sum()))
