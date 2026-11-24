# Kleurronde k2 tempel: vanaf k1, alleen tinten op bestaande posities.
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k1'))
from gereedschap import *
HIER2=os.path.dirname(os.path.abspath(__file__))
a0,pal0=laad()                                  # af (voor bewijs)
k1,pal=laad(os.path.join(HIER2,'..','k1','tempel.png'))
a=k1.copy()
STEEN=(5,6,15)

# 1. Ruïneblok: voetlijn in 'o' (7), zoals de voet van de gevel (rij 16, x25-36).
for x in range(38,47): a[14,x]=7

# 4. Ruispixel
a[37,50]=14

# 3b. Bergwand: rechts van de p-vouw (EE-paar, rij 22-36) tot de zwarte lijn -> 14
for y in range(22,37):
    xs=[x for x in range(44,63) if a[y,x]==14]
    zw=min(x for x in range(44,64) if a[y,x]==1)
    if not xs: continue
    for x in range(max(xs)+1,zw):
        if a[y,x]==15: a[y,x]=14

# 2 + 3a. Stenen naar de steenindeling van het model; elke steen één tint.
def rand_M(x):   # onderrand middelste terras (bestaande p-lijn)
    return {40:40,41:40,42:39,43:39,44:39,45:39,46:39,47:38,48:38,49:38,50:38,51:37,52:37,53:37}[x]
S1={44:52,45:51,46:51,47:50,48:50,49:49,50:48,51:47,52:47,53:47,54:46,55:46,56:45,57:45,58:44,59:44,60:44}
def steen(x,y):
    # middelste terras, rechterzijvlak (x40-53, y28-38): 3 lagen; voegen uit het model
    if 40<=x<=53 and y<rand_M(x) and y>=29:
        A = 32 if x<=44 else (31 if x<=49 else 30)      # voeg A (stijgt naar rechts)
        B = 36 if x<=43 else (35 if x<=49 else 34)      # voeg B
        if y<=A:   return ('M1', 0 if x<=44 else (1 if x<=49 else 2))
        if y<=B:   return ('M2', 0 if x<=46 else (1 if x<=51 else 2))
        return ('M3', 0 if x<=43 else (1 if x<=49 else 2))
    # onderste terras, rechterzijvlak (x42-60, y37-60): boven en onder voeg S1
    if 42<=x<=60 and y>=37 and not (40<=x<=53 and y<rand_M(x)):
        if x in S1 and y>S1[x]:
            return ('D', 0 if x<=49 else (1 if x<=54 else 2))
        return ('U', 0 if x<=51 else 1)
    return None
groep={}
for y in range(64):
    for x in range(64):
        if a[y,x] in STEEN:
            s=steen(x,y)
            if s: groep.setdefault(s,[]).append((x,y))
stenen=sorted(groep)
# buren: stenen die aan elkaar grenzen (4-buren), ook over één voegpixel heen
pos={p:s for s,ps in groep.items() for p in ps}
buur=set()
for p,s in pos.items():
    x,y=p
    for dx,dy in ((1,0),(0,1),(-1,0),(0,-1),(2,0),(0,2)):
        t=pos.get((x+dx,y+dy))
        if t and t!=s and (s[0][0]=='M')==(t[0][0]=='M'): buur.add(tuple(sorted((s,t))))
# voorkeur: licht van linksboven (laag x+y = lichter), onderste laag donkerder
LUM={5:0,6:1,15:2}
def doel(s):
    ps=groep[s]; m=sum(x+y for x,y in ps)/len(ps)
    return 0 if m<80 else (1 if m<95 else 2)
best=None
for keus in itertools.product(STEEN,repeat=len(stenen)):
    k=dict(zip(stenen,keus))
    if any(k[u]==k[v] for u,v in buur): continue
    c=sum(abs(LUM[k[s]]-doel(s))*len(groep[s]) for s in stenen)
    if best is None or c<best[0]: best=(c,k)
# met de hand gekozen (middelste terras: licht linksboven, mozaïek van stenen; (licht onder het mos linksboven, donkere middensteen onder S1)
best[1].update({('M1',0):5,('M1',1):15,('M1',2):6,('M2',0):6,('M2',1):5,('M2',2):15,('M3',0):5,('M3',1):15,('M3',2):6,
                ('U',0):5,('U',1):6,('D',0):6,('D',1):15,('D',2):5})
assert not any(best[1][u]==best[1][v] for u,v in buur)
for s in stenen:
    for x,y in groep[s]: a[y,x]=best[1][s]
    print(s,len(groep[s]),'->',best[1][s])

if __name__=='__main__':
    bewaar(a,pal,os.path.join(HIER2,'tempel.png'))
    print(bewijs(a,pal,a0,pal0))
    d=(a!=k1).sum(); print('pixels veranderd t.o.v. k1: %d'%d)
    vel(a,pal,k1,pal,os.path.join(TEMPEL,'referenties','model.webp'),os.path.join(HIER2,'vel.png'))
    from PIL import ImageDraw
    V=Image.open(os.path.join(HIER2,'vel.png')); d=ImageDraw.Draw(V)
    d.rectangle((760,686,1000,700),fill=(236,236,236)); d.text((760,690),'boven: k2 1x, onder: k1 1x  |  8x: k2 | k1 | model',fill=(0,0,0)); V.save(os.path.join(HIER2,'vel.png'))
    big=Image.open(os.path.join(HIER2,'tempel.png')).convert('RGBA').resize((512,512),Image.NEAREST)
    bg=Image.new('RGB',(512,512),(255,255,255)); bg.paste(big,(0,0),big); bg.save(os.path.join(HIER2,'tempel_8x.png'))
