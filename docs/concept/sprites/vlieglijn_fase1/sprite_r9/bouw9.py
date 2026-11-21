# r9: vanaf r8. Alleen poot 4 (nieuwe poot langs rood) komt hoger uit het lijf: zijn kabelpatroon (lijn, 9 glans, 7, lijn)
# van rij 46 recht omhoog doorgetrokken t/m rij 42 over de grijze plaat onder de dij; rij 41 = lijn onder de dij.
# r9-strookje (33,44-46) en alles verder bevroren.
import numpy as np; from PIL import Image
PAL=[(255,0,255),(16,16,20),(32,32,36),(60,60,66),(104,104,110),(156,156,160),(188,188,192),
     (50,60,74),(86,100,118),(132,148,162),(234,248,252),(208,232,240),(116,146,162),(160,72,214),(224,116,52),(146,64,34)]
f=np.loadtxt('../sprite_r8/vlieg_r8.txt',dtype=int); r8=f.copy()
rij46=[f[46,x] for x in (34,35,36)]            # bestaande kabelpixels van poot 4: 9 7 1
assert rij46==[9,7,1], rij46
for y in (42,43,44,45):
    for x,v in zip((34,35,36),rij46): f[y,x]=v
for y in (42,43): f[y,33]=1                     # linkerlijn waar geen r9-strookje is
f[41,34]=1; f[41,35]=1                          # bovenlijn = verlengde onderlijn van de dij
# Jordi: r9-restant blijft staan maar moet als eigen verre poot lezen (alleen kleur/schaduw/lijn, vorm en plek gelijk)
R9={(33,45):7,(33,46):7}          # strookje onder het lijf: verre tint (8 glans op (32,44), rest 7) -> donker naast de 9-glans van poot 4
R9.update({(38,53):1,(39,54):1,(40,55):1})   # scheidingslijn: rechter 7-pixel van poot 4 naast het voetje wordt omlijning
for (x,y),v in R9.items(): f[y,x]=v
assert all(f[y,x]==15 for x,y in ((39,53),(40,53),(40,54)))   # klauwtjes al donker koper
np.savetxt('vlieg_r9.txt',f,fmt='%2d')
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save('vlieg_r9.png',transparency=0)
Image.fromarray(np.array(PAL)[f].astype('uint8')).resize((512,512),Image.NEAREST).save('vlieg_r9_8x.png')
d=[(x,y,r8[y,x],f[y,x]) for y,x in zip(*np.where(f!=r8))]
zone={(x,y) for x in range(33,37) for y in range(41,46)}
print('anders dan r8:',len(d),d); print('buiten poot-4-aanzet (x33-36,y41-45) en r9-restant:',[p for p in d if (p[0],p[1]) not in zone|set(R9)])
N=((1,0),(-1,0),(0,1),(0,-1))
print('losse px:',[(x,y) for y in range(1,63) for x in range(1,63) if f[y,x] and not any(f[y+a,x+b] for a,b in N)])
from collections import deque
# kleine restvlakjes (<3 px) van lijfkleur rond de aanzet
for col in (3,4,5):
    seen=set()
    for y in range(39,47):
        for x in range(30,40):
            if f[y,x]==col and (x,y) not in seen:
                q=deque([(x,y)]); seen.add((x,y)); c=[]
                while q:
                    p=q.popleft(); c.append(p)
                    for a,b in N:
                        n=(p[0]+b,p[1]+a)
                        if n not in seen and f[n[1],n[0]]==col: seen.add(n); q.append(n)
                if len(c)<3: print('klein vlakje kleur',col,c)
