"""Controle viscacha kleur_r2: alpha-diff met het r1-silhouet (alleen benoemde zones), pixeldiff r1->r2 per zone, open randen, losse pixels, clusters < 3 px, kleurtelling, png = raster."""
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
r=[l.rstrip('\n') for l in open(D+'kleur_r2/raster.txt')][:64]
sil=[l.rstrip('\n') for l in open(D+'silhouet/silhouet.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
LIJN=set('128BF')          # omlijning, selout, binnenlijnen (8 = geel selout, B = bruin selout staart / oorbinnen, F = creme selout)
VLAK=set('345679ACDE')     # vlaktinten (D/E = oog)
ad=[(x,y) for x,y in P if (r[y][x]!='.')!=(sil[y][x]=='#')]
import collections
sys.path.insert(0,D+'kleur_r2'); import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import reparaties_r2 as RP
o=[l.rstrip('\n') for l in open(D+'kleur_r1/raster.txt')][:64]
print('silhouetwijzigingen t.o.v. r1:',len(ad))
for x,y in ad: print('   (%d,%d) %s  zone %s'%(x,y,'erbij' if r[y][x]!='.' else 'weg',RP.ZONE.get((x,y),'NIET BENOEMD')))
d=[(x,y) for x,y in P if r[y][x]!=o[y][x]]
pz=collections.Counter(RP.ZONE.get(p,'NIET BENOEMD') for p in d)
print('pixeldiff r1->r2:',len(d),'px; per zone:',dict(sorted(pz.items())))
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
open_=[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in LIJN]
print('open randen (vlakkleur op de buitenrand):',len(open_),open_)
los=[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and all(c=='.' for c in nb4(x,y))]
print('losse pixels (geen 4-buren):',los)
seen=set(); small=[]
for x,y in P:
    c=r[y][x]
    if c not in VLAK or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
        a,b=st.pop(); comp.append((a,b))
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=(a+dx,b+dy)
            if 0<=p[0]<64 and 0<=p[1]<64 and p not in seen and r[p[1]][p[0]]==c: seen.add(p); st.append(p)
    if len(comp)<3: small.append((c,sorted(comp)))
print('tintclusters < 3 px (4-samenhangend):',len(small))
for c,comp in small: print('  ',c,comp,'(oog/glans)' if c in 'DEF' else '')
used=sorted(set(c for row in r for c in row)-{'.'})
print('gebruikte indexen:',''.join(used),'| kleuren incl. transparant:',len(used)+1)
im=Image.open(D+'kleur_r2/viscacha.png'); print('png:',im.size,im.mode,'paletlengte',len(im.getpalette())//3)
ok=all((im.getpixel((x,y))==(0 if r[y][x]=='.' else int(r[y][x],16))) for x,y in P); print('png == raster:',ok)
