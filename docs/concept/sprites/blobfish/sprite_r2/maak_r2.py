# Blobfish r2: r1 + alleen herstel van wat de 4x4-reductie kapotmaakte, elke pixel gemeten op het model.
# Silhouet bevroren (alpha-diff 0 met r1, wordt gecontroleerd). Elke wijziging -> afwijkingen_r2.txt.
# Stappen (benoemde reparaties van Claude, in volgorde):
#  L lippen/mond   O ogen   S vinstralen   V kopvinnetje (scheidingslijn)   G glans
import numpy as np; from PIL import Image; from collections import Counter
R1=Image.open('r1.png'); r1=np.asarray(R1).astype(int); pal=R1.getpalette()[:3*13]
GL=12+1                                   # nieuwe index 13: glanswit (gemeten, zie G)
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]
def blok(x,y):
    ny=OY+4*(y-y0+ymin); nx=OX+4*(x-x0+xmin); return n[ny:ny+4,nx:nx+4].reshape(-1,3), L[ny:ny+4,nx:nx+4].ravel()
PALA=np.array(pal).reshape(-1,3)
def dichtst(c,idx): return min(idx,key=lambda i:((PALA[i]-c)**2).sum())
o=r1.copy(); log=[]
def zet(x,y,v,stap):
    if o[y,x]!=v: log.append((stap,x,y,o[y,x],v)); o[y,x]=v
m=r1>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
OOG={(19,45),(20,45),(19,46),(20,46),(9,41),(10,41),(9,42),(10,42)}

# ---- L lippen: per blok tellen; donker = helderheid < 62, licht = >= 105 (lipkleur)
#  mondlijn  : >=4 donker EN >=5 licht  (dunne zwarte lijn door de lichte lip)          -> zwart (1)
#  onderliplijn: >=4 donker, < 5 licht (bredere donkere lijn, blokgemiddelde ~65)        -> lijnrood (2)
#  lip       : >=8 licht                                                                 -> dichtstbijzijnde liptoon (9/10/11) van de niet-donkere modelpixels
#  rest      : r1 blijft
for y in range(44,53):
    for x in range(7,22):
        if not m[y,x] or rand[y,x] or (x,y) in OOG: continue
        b,l=blok(x,y); d=(l<62).sum(); li=(l>=105).sum()
        if d>=4 and li>=5: zet(x,y,1,'L')
        elif d>=4: zet(x,y,2,'L')
        elif li>=8: zet(x,y,dichtst(b[l>=62].mean(0),(9,10,11)),'L')
# onderlip rechts (x15-19, y50): modelgemiddelde (182-188,62-64,67), helderheid 98-101, ligt even ver van tint 8 als
# van liptint 9 (RGB-afstand 19/20) -> liptint 9, zodat de onderlip als lip leest (opdracht: onderlip licht)
for x in range(15,20): zet(x,50,9,'L')
# onderliplijn links smelt samen met de buitenlijn (x10-11 y50 boven randpixels x10-11 y51): daar neemt de buitenlijn
# het over en krijgen deze pixels de lipkleur van hun blok (opdracht: niet samengesmolten met de buitenlijn)
for x,y in ((10,50),(11,50)):
    b,l=blok(x,y); zet(x,y,dichtst(b[l>=62].mean(0),(9,10)),'L')
# mondlijn doorlopend en 1 px: (9,47) 3 donkere modelpx op de lijn van (8,46) naar (10,48) -> zwart;
# (19,49) eind van de mondlijn, 6 donkere modelpx (de lijn loopt hier omhoog naar het bovenste deel van het blok) -> zwart
for x,y in ((9,47),(19,49)): zet(x,y,1,'L')
# onderliplijn = lijnrood, ook waar de regel hem zwart gaf (12,50); lipeind-lijn sluiten: (20,47) 3 donkere modelpx
for x,y in ((12,50),(20,47)): zet(x,y,2,'L')
# onderliplijn tegen de buitenlijn links ((8,48) naast rand (7,48); (9,49) naast rand (8,49)/(9,50)): buitenlijn neemt over,
# pixel krijgt de lipkleur van zijn niet-donkere modelpixels
for x,y in ((8,48),(9,49)):
    b,l=blok(x,y); zet(x,y,dichtst(b[l>=62].mean(0),(9,10)),'L')

# ---- O ogen (2x2 op de modelplek; model: donkere ring/pupil boven met glanspuntje, wit sikkeltje onder)
#  nabij (19-20,45-46): bovenrij 4 en 7 donkere modelpx -> pupil; (20,46) 12 witte px -> wit; (19,46) 2 donker/5 licht/rest lijf -> r1 (lijf)
#  ver (9-10,41-42): (10,41) 3 donkere px -> pupil; (9,41) ring + glanspuntje, meest lijf -> pupil (anders leest het oog
#  als witte vlek; opdracht: "donkere ring/pupil met witte glans"); (9,42) en (10,42) 3-4 witte px -> wit (sikkeltje)
#  Pupilkleur: model meet (77-92,38-44,37-44) = lijnrood; zwart gekozen voor leesbaarheid op 1x (opdracht), zie NOTITIES.
for x,y in ((19,45),(20,45),(9,41),(10,41)): zet(x,y,1,'O')
for x,y in ((20,46),(9,42),(10,42)): zet(x,y,12,'O')

# ---- V kopvinnetje: ondercontour tussen vinnetje en kop (model: dunne donkere lijn (13,34)-(17,32); 3-4 donkere px per blok)
#  (14,33) 4 donker, (15,33) 3 donker -> lijnrood (binnenlijn); (17,32) is al zwart (rand)
for x,y in ((14,33),(15,33)): zet(x,y,2,'V')

# ---- S vinstralen: natieve pixel >= 22 helderder dan de 7x7-mediaan = straal (stralen.py); spritepixel met >= 5 straalpx
#  in een vinzone (niet op de rand, niet op de kopvinlijn, niet los: >= 1 straalbuur) -> straaltint 11 (222,144,150); gemeten straalkleur per vin
#  (211-223,130-149,133-152), helderheid p50 155-172 -> 11 is de dichtstbijzijnde
T=np.load('stralen.npy')
VIN={'kopvin':(10,29,17,33),'rugvin':(24,26,42,34),'borstvin':(26,38,42,54),'staart':(42,24,58,38)}
kand=set()
for nm,(a,b,c,d) in VIN.items():
    for y in range(b,d):
        for x in range(a,c):
            if m[y,x] and not rand[y,x] and T[y,x]>=5 and (x,y) not in ((14,33),(15,33)): kand.add((x,y))
# alleen lijnen: een straalpixel blijft als hij een 8-buur straalpixel heeft (losse stippen = raster, weg)
for x,y in sorted(kand):
    if any((x+dx,y+dy) in kand for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy): zet(x,y,11,'S')

# ---- G glans: modelhelderheid per blok (p90) overnemen, alleen lichter maken, nooit donkerder.
#  glanswit = mediaan van de natieve glanspixels op de kop (helderheid >= 200) -> nieuwe index 13
#  p90 >= 200 -> 13 (glanswit); 160-199 -> 11; 140-159 -> 10, als dat lichter is dan r1. Niet op rand, ogen, lipzone.
kop=n[OY+4*(30-y0+ymin):OY+4*(40-y0+ymin), OX+4*(7-x0+xmin):OX+4*(22-x0+xmin)].reshape(-1,3)
kl=kop@[0.299,0.587,0.114]; GLANS=tuple(int(v) for v in np.median(kop[kl>=200],0))
PALA=np.vstack([PALA,GLANS]); LUM=PALA@[0.299,0.587,0.114]
for y in range(24,56):
    for x in range(64):
        if not m[y,x] or rand[y,x] or (x,y) in OOG or (7<=x<=21 and 44<=y<=52): continue
        b,l=blok(x,y); p=np.percentile(l,90)
        v=13 if p>=200 else (11 if p>=160 else (10 if p>=140 else 0))
        if v and LUM[v]>LUM[o[y,x]]: zet(x,y,v,'G')
# losse G-pixels (geen lichte 8-buur 10-13) = ruis, terug naar r1
for st,x,y,a,b in [e for e in log if e[0]=='G']:
    if not any(o[y+dy,x+dx] in (10,11,12,13) for dy in (-1,0,1) for dx in (-1,0,1) if dx or dy):
        o[y,x]=a; log.remove((st,x,y,a,b))
assert ((o>0)==(r1>0)).all(), 'silhouet gewijzigd'

# ---- uitvoer
def opslaan(naam):
    P=list(pal)+list(GLANS)
    p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(P+[0]*(768-len(P))); p.save(naam,transparency=0)
if __name__=='__main__':
    opslaan('blobfish_r2.png')
    print(Counter(s for s,*_ in log)); print('alpha-diff met r1:',int(((o>0)!=(r1>0)).sum()),'kleuren',len(set(o.ravel()))-1)
    Z={'gezicht (ogen+lippen)':(6,40,23,55),'kop':(6,28,23,40),'rugvin':(23,26,42,34),'borstvin':(26,38,42,56),'staart':(42,24,58,40)}
    def zone(x,y):
        for nm,(a,b,c,d) in Z.items():
            if a<=x<c and b<=y<d: return nm
        return 'lijf'
    print(Counter((s,zone(x,y)) for s,x,y,_,_ in log))
    open('afwijkingen_r2.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a}->{b}\t{zone(x,y)}' for s,x,y,a,b in log)+'\n')
    for y in range(40,55): print('%2d'%y, ''.join(('%x'%o[y,x] if o[y,x] else '.') for x in range(6,24)), '  ', ''.join(('%x'%r1[y,x] if r1[y,x] else '.') for x in range(6,24)))
