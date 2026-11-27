# r16 = volume in de vachtvlakken (Jordi 27 nov op r15: "ik vind hem nog erg effen qua kleur").
# Alleen tintwissels binnen vachtvlakken: alleen M-pixels (en in B enkele M binnen een hooglicht) wisselen naar H/L/D.
# H = nieuwe tussentint in het vrije slot 15, tussen L en M (Stantler/Ponyta: 3 vachttinten + een extra lichte op de bolling).
# Opbouw per groot vlak (Gen 3-studie, r16/NOTITIES.md): hooglicht als ellips linksboven op de bolling (gebogen grens),
# sikkel = ellips min dezelfde ellips verschoven naar het licht (maansikkel aan de schaduwkant).
# Bestaande L/D (uit het model), randen, lijnen, strepen, oog, neus/mond: niet aangeraakt (zie bewijs in r16_check.py).
import numpy as np
from PIL import Image
im=Image.open('r15/kudu_r15.png'); idx0=np.array(im); g0=np.load('r15/grid.npy')
PAL=im.getpalette()[:48]; PAL[45:48]=[234,194,106]   # H
L2I={}
for y in range(64):
    for x in range(64): L2I.setdefault(g0[y,x],int(idx0[y,x]))
L2I['H']=15
def E(cx,cy,rx,ry): return lambda x,y: ((x-cx)/rx)**2+((y-cy)/ry)**2<1
def SIK(cx,cy,rx,ry,dx,dy): # sikkel: in ellips, niet in de naar linksboven verschoven ellips
    a=E(cx,cy,rx,ry); b=E(cx-dx,cy-dy,rx,ry); return lambda x,y: a(x,y) and not b(x,y)
def PX(*p):
    S=set(p); return lambda x,y:(x,y) in S
def RECT(x0,x1,y0,y1): return lambda x,y: x0<=x<=x1 and y0<=y<=y1
def AND(*f): return lambda x,y: all(h(x,y) for h in f)
# (vlak, zone-test, lagen [(vorm, tint)], laatste laag wint)
VLAKKEN={
'A':[
 ('kop voorhoofd', RECT(11,24,17,29), [(PX((14,19),(15,19),(13,20),(14,20)),'H')]),
 ('kop wang',      RECT(11,24,17,29), [(PX((14,25),(15,25),(16,25),(14,26),(15,26)),'H')]),
 ('hals',          RECT(19,19,30,32), [(lambda x,y:True,'H')]),
 ('borst',         RECT(16,23,38,46), [(PX((20,41),(20,42),(21,42),(19,43),(20,43)),'H')]),
 ('schouder',      RECT(21,34,38,47), [(PX((29,44),(30,45),(30,46),(30,47),(30,48)),'H'), (PX((27,46),(28,46),(34,44),(34,45),(33,46)),'D')]),
 ('romp',          RECT(35,49,31,43), [(E(41.5,33.0,4.2,4.2),'H')]),
 ('dij',           RECT(45,54,33,50), [(E(47.8,36.6,2.3,2.4),'H'), (PX((52,44),(51,45),(51,46)),'D')]),
 ('achterbeen',    RECT(48,53,48,52), [(PX((51,50),(52,51),(52,52)),'H')]),
],
'B':[
 ('kop voorhoofd', RECT(11,24,17,29), [(PX((15,18),(13,19),(14,19),(15,19),(16,19),(12,20),(13,20),(14,20)),'H'), (PX((14,19),),'L')]),
 ('kop wang',      RECT(11,24,17,29), [(PX((14,24),(15,24),(13,25),(14,25),(15,25),(16,25),(17,25),(14,26),(15,26),(16,26)),'H'), (PX((15,25),),'L'), (SIK(17.5,23.5,5.8,5.4,2.0,2.0),'D')]),
 ('hals',          RECT(19,19,30,32), [(lambda x,y:True,'H')]),
 ('borst',         RECT(16,23,38,46), [(PX((19,41),(20,41),(21,41),(21,42),(22,42),(19,43),(20,43),(21,43),(19,44),(20,44)),'H'), (PX((20,42),),'L'), (PX((21,45),(22,45)),'D')]),
 ('schouder',      RECT(21,34,38,47), [(PX((28,43),(29,43),(29,44),(29,45),(30,46),(30,47)),'H'), (PX((26,46),(27,46),(28,46),(34,43),(34,44),(34,45),(33,45),(33,46),(32,46)),'D')]),
 ('romp',          RECT(35,49,31,43), [(E(41.5,33.5,5.0,5.0),'H'), (E(41.0,33.0,3.0,2.4),'L')]),
 ('dij',           RECT(45,54,33,50), [(E(48.2,37.5,2.6,4.0),'H'), (E(48.0,36.5,1.2,1.8),'L'), (PX((52,43),(52,44),(51,45),(51,46),(52,47),(52,48)),'D')]),
 ('voorbeen',      RECT(30,30,48,49), [(lambda x,y:True,'H')]),
 ('achterbeen',    RECT(48,53,48,52), [(PX((49,48),(50,49),(51,50),(52,51),(52,52)),'H')]),
]}
OOG=RECT(15,19,21,24); NEUS=RECT(8,12,23,29)
def rand(g,x,y): return any(g[y+dy,x+dx] in '.0K' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
def maak(v):
    g=g0.copy(); log=[]
    for naam,zone,lagen in VLAKKEN[v]:
        for y in range(1,63):
            for x in range(1,63):
                if not zone(x,y) or OOG(x,y) or NEUS(x,y): continue
                c=g0[y,x]
                if c!='M' and not (c=='L' and naam=='romp'): continue  # alleen effen middenvacht (en modellicht in de romp blijft L)
                if rand(g0,x,y) and c=='M': 
                    # randpixels: alleen hooglicht naar binnen toe, geen sikkel op de rand (rand = lijnrol)
                    pass
                n=None
                for f,t in lagen:
                    if f(x,y): n=t
                if n is None or n==c: continue
                if c=='L': continue
                g[y,x]=n; log.append((x,y,c,n,naam))
    return g,log
HAND={'A':[],'B':[]}   # (x,y,oud,nieuw,reden) na het kijken
def bouw(v):
    g,log=maak(v)
    for x,y,o,n,r in HAND[v]:
        assert g[y,x]==o,(v,x,y,g[y,x],o); g[y,x]=n; log.append((x,y,o,n,'hand: '+r))
    return g,log
if __name__=='__main__':
    for v in 'AB':
        g,log=bouw(v)
        idx=np.vectorize(lambda c:L2I[c])(g).astype(np.uint8)
        o=Image.fromarray(idx,'P'); o.putpalette(PAL+[0]*(768-48)); o.save(f'r16/kudu_r16{v}.png',transparency=0)
        np.save(f'r16/grid{v}.npy',g)
        with open(f'r16/pixels{v}.txt','w') as f:
            for x,y,o,n,r in log: f.write(f'({x},{y}) {o}->{n}  {r}\n')
        print(v,len(log))
        for y in range(14,64): print('%2d '%y+''.join(g[y]))
