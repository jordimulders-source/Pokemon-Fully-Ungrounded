# Nachtaap ronde 12, variant_spiraal: D1 oppervlak <= 950 met een kleinere spiraal.
# Basis: ../ (ronde 12 = ronde 11 + A6). Lijf, kop en armen pixel voor pixel gelijk; alleen de staart verandert.
# - Spiraal met de hand verkleind in dezelfde opbouw (bovenband 2/5/4/3/1, zijkanten 2-4-1, binnenpunt, onderband):
#   13x12 -> 10x9 px; de binnenpunt is 1 px breed (2) in plaats van 3.
# - Spiraal zakt 6 rijen en 7 kolommen langs de stam (stam 6 rijen korter); staat nu rechts naast de kop.
# - Stam 3 px dik (2-4-1) in plaats van 4 (2-4-3-1), passend bij de kleinere spiraal; aanzet bij de heup blijft.
import numpy as np
from fu import *
old,pal=load('nachtaap/ronde12'); a=old.copy()
OUT={1,2}
SPIRAAL=['..22222...',
         '.2555431..',
         '254111431.',
         '251...241.',
         '241.2.241.',
         '241.2.241.',
         '.14121241.',
         '..133241..',
         '...1241...']
X0,Y0,KEEP=43,32,41          # frame 1; frame 2 = staart 1 rij hoger (zoals ronde 10-12)
def staart(f1,seed):
    m=np.zeros_like(f1,bool); st=[seed]
    while st:
        x,y=st.pop()
        if m[y,x] or f1[y,x]==0 or x<36 or y>48: continue
        m[y,x]=True; st+= [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return m
for f,dy in ((0,0),(1,-1)):
    fr=a[64*f:64*f+64]                     # view
    m=staart(fr.copy(),(55,30+dy))
    tail=np.where(m,fr,0); fr[m]=0         # lijf zonder staart
    body=fr.copy()
    for y in range(KEEP+dy,64):            # aanzet + onderste stam blijven
        for x in range(64):
            if m[y,x]: fr[y,x]=tail[y,x]
    for y in range(KEEP+dy,KEEP+dy+5):     # stam 41-45 dunner: '3' eruit, '1' 1 px naar links
        xs=[x for x in range(64) if m[y,x]]
        assert ''.join('%x'%tail[y,x] for x in xs[-2:])=='31',(f,y)
        fr[y,xs[-1]]=0; fr[y,xs[-2]]=1
    for j,r in enumerate(SPIRAAL):
        for i,ch in enumerate(r):
            if ch=='.': continue
            y,x=Y0+dy+j,X0+i
            assert body[y,x]==0 and not any(body[y+v,x+u] for u in (-1,0,1) for v in (-1,0,1)),('raakt lijf',f,x,y)
            fr[y,x]=int(ch,16)
zones=[(f,36,21,60,48+dy) for f,dy in ((0,0),(1,-1))]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
# bewijs: alles links van x36 en alle niet-staartpixels gelijk
save(a,pal,'nachtaap/ronde12','nachtaap/ronde12/variant_spiraal')
