# Bewijs: groen en zwarte gezichtslijnen bevroren; clusters < 3 px in het ijzer; kleuren.
from PIL import Image; import numpy as np
a=np.array(Image.open('sprite_r10/sprite.png')); b=np.array(Image.open('sprite_r9/sprite.png'))
G=[2,3,4,5,6,13]
gm=np.isin(b,G)|np.isin(a,G)
print('groen: pixels met groene index r9',int(np.isin(b,G).sum()),'r10',int(np.isin(a,G).sum()),'verschil op groene posities',int((a[gm]!=b[gm]).sum()))
# zwarte lijnen ogen + grijns groot gezicht: alle zwart in x2-23, y30-47 die aan groen grenzen (r9)
z=0;n=0
for y in range(30,48):
    for x in range(2,24):
        if b[y,x]==1 and any(b[y+dy,x+dx] in G for dy,dx in((0,1),(1,0),(0,-1),(-1,0))):
            n+=1; z+=int(a[y,x]!=1)
print('zwarte gezichtslijnen (zwart naast groen, x2-23 y30-47):',n,'gewijzigd',z)
d=np.argwhere(a!=b); print('totaal gewijzigd',len(d),'(alle op ijzer/transparant)')
print('kleuren gebruikt',len(set(a.flatten())-{0}))
# kleine clusters (4-buren, zelfde index) in ijzertinten 7-12 in de werkzones
from collections import deque
seen=np.zeros_like(a,bool); klein=[]
for y in range(64):
    for x in range(64):
        if seen[y,x] or a[y,x] not in (7,8,9,10,11,12): continue
        q=deque([(y,x)]); seen[y,x]=1; c=[]
        while q:
            p=q.popleft(); c.append(p)
            for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                Y,X=p[0]+dy,p[1]+dx
                if 0<=Y<64 and 0<=X<64 and not seen[Y,X] and a[Y,X]==a[y,x]: seen[Y,X]=1; q.append((Y,X))
        if len(c)<3: klein.append((a[y,x],[(p[1],p[0]) for p in c]))
print('clusters <3 px:',len(klein)); 
for k in klein: print(' ',k)
