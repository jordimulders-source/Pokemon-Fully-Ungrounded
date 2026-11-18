# r17 = r16 + Jordi (17 nov) over r16: "hij mag de hand gewoon overlappen he, dit ziet er echt raar uit"
# Muts ligt nu VOOR het kruis: linkerrand = een bolle boog van de koepel (11,11) naar het oor (9,25),
# over de rechterarm/het midden van het kruis heen. Geen S-curve, geen inham.
#   rand-x per rij: y11 11 | y12-14 10 | y15-19 9 | y20-23 8 | y24-25 9   (looplengtes 1,3,5,4,2)
#   buitenlijn: selout 4 waar links transparant is (y12-16), zwart 1 vanaf het kruis (y17-25)
#   binnen de nieuwe boog: middentint 3 zoals de mutsflap van r15 (x11), donkere sikkel x12-14 ongewijzigd
#   kruis links van de rand = r15-pixels (r16-verschuiving y21-24 teruggedraaid); (7,24) blijft 4 zoals r16
# Draaien vanuit deze map: python3 build.py
from PIL import Image; import numpy as np
src=Image.open('../r16/banette_evo.png'); pal=src.getpalette(); R16=np.array(src); a=R16.copy()
R15=np.array(Image.open('../r15/banette_evo.png'))
E={11:11,12:10,13:10,14:10,15:9,16:9,17:9,18:9,19:9,20:8,21:8,22:8,23:8,24:9,25:9}
for y,e in E.items():
    a[y,2:13]=R15[y,2:13]                       # r15 als basis (kruis + mutsflap)
    for x in range(e+1,11): a[y,x]=R15[y,11]    # nieuw mutsvlak = eerste flaptint van r15
    a[y,e]=4 if (a[y,e-1]==0 and y<=16) else 1  # selout lichtkant, zwart over het kruis
a[24,7]=4                                       # r16-fix blijft
a[25,10]=3                                      # aansluiting oor: x10 houdt r15-tint (geen 4-strook)
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
# --- bewijs
d=np.argwhere(a!=R16)
buiten=[(x,y) for y,x in d if not (2<=x<=15 and 8<=y<=28)]
print('pixeldiff t.o.v. r16:',len(d),'| buiten zone x2-15 y8-28:',len(buiten))
for y,x in d: print('  (%d,%d) %d -> %d'%(x,y,R16[y,x],a[y,x]))
print('rand-x per rij:',' '.join('y%d:%d(%d)'%(y,e,a[y,e]) for y,e in E.items()))
for y in range(8,30): print('  %2d'%y,''.join('.' if v==0 else '%x'%v for v in a[y,0:18]))
z=np.pad(a,1); N=((0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1))
los=[(x,y) for y in range(64) for x in range(64) if a[y,x] and not any(z[y+1+dy,x+1+dx] for dy,dx in N)]
# gesloten buitenlijn: geen grijs (2/3) direct naast transparant in de zone
open_=[(x,y) for y in range(8,29) for x in range(2,16) if a[y,x] in (2,3) and any(z[y+1+dy,x+1+dx]==0 for dy,dx in N[:4])]
# tintclusters <3 px (4-buren, zelfde index) in de zone x2-15 y8-28
from collections import deque
seen=set(); klein=[]
for y in range(8,29):
    for x in range(2,16):
        if (x,y) in seen or a[y,x]==0: continue
        q=deque([(x,y)]); seen.add((x,y)); c=[]
        while q:
            px,py=q.popleft(); c.append((px,py))
            for dy,dx in N[:4]:
                nx,ny=px+dx,py+dy
                if 0<=nx<64 and 0<=ny<64 and (nx,ny) not in seen and a[ny,nx]==a[py,px]: seen.add((nx,ny)); q.append((nx,ny))
        if len(c)<3: klein.append((a[y,x],c))
print('geheel losse pixels:',los,'| open buitenrand in zone:',open_,'| kleuren:',len(np.unique(a)))
print('tintclusters <3 px in zone:',klein)
