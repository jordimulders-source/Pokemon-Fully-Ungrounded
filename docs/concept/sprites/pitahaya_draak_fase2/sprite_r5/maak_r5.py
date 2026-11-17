# Pitahaya-draak fase 2, r5 op r4: bek als vier delen (bovenlip+kaaklijn, grijze wig, verre lip, onderkaak).
# Alles gemeten op het model (natief.png, 3x3-blok per spritepixel: X -> nx 2+3X..4+3X, Y -> ny 3(Y-13)..+2),
# banden als doorlopende contour (middenpad per spritekolom), opbouw (schaduw) naar Gen 3 (zie NOTITIES).
import numpy as np; from PIL import Image
from groepen import laad
R=Image.open('pitahaya2_r4.png'); r4=np.asarray(R).astype(int); pal=R.getpalette()
a,lum,g=laad(); o=r4.copy(); log=[]
N={0:'.',1:'K',2:'d',3:'r',4:'p',5:'P',6:'g',7:'G',8:'h',9:'H',10:'w',11:'W',12:'s',13:'v'}
I={v:k for k,v in N.items()}
GV=(155,154,159)   # donkergrijs, gemeten in het model (wig/pitrand, natief (36,93)); nieuwe index 13 'v'
pal[39:42]=list(GV)
def blk(X,Y): return slice(3*(Y-13),3*(Y-13)+3),slice(2+3*X,5+3*X)
def info(X,Y):
    gb=g[blk(X,Y)]; return f"model {(gb==2).sum()} roze/{(gb==1).sum()} zwart/{((gb==6)|(gb==7)).sum()} vlees/{(gb==0).sum()} bg"
def zet(X,Y,c,stap):
    v=I[c]
    if o[Y,X]!=v: log.append((stap,X,Y,N[o[Y,X]],c,info(X,Y))); o[Y,X]=v
# 1 BOVENLIP/KAAKLIJN: middenpad zwarte modellijn per spritekolom: X9-11 ny 88-89.5 -> Y42; X12-13 ny 90.5-91.5 -> Y43;
#   X14-16 ny 93.5 -> Y44; mondhoek X17-18 Y43 (lijn loopt omhoog naar de wang, r4 had die al). Tanden/tandvlees (4,8) = r4.
for X,Y in ((11,42),(12,43),(13,43),(14,44)): zet(X,Y,'K','1 kaaklijn (contour)')
# 2 WIG (vlees bovenkaak achter de tanden, boven de verre lip): Gen 3-schaduw onder de bovenkaak -> donkergrijs v
WIG=[(10,43),(11,43),(10,44),(11,44),(12,44),(13,44),(11,45)]
for X,Y in WIG: zet(X,Y,'v','2 wig donkergrijs (Gen 3-schaduw)')
# 3 VERRE LIP: middenpad roze band: nx32 ny100.5 -> (10,46); nx36 99.5 -> (11,46); nx38-40 98-97.5 -> (12,45); nx42 96 -> (13,45);
#   nx44 95.5 -> sluit op de kaaklijn (14,44). Links breder (X9-10, Y45-47 roze in het model). Toon = gemiddelde roze modelpx.
for X,Y,c in ((9,45,'r'),(10,45,'p'),(10,46,'r'),(11,46,'r'),(12,45,'r'),(13,45,'r'),(10,47,'r')): zet(X,Y,c,'3 verre lip (contour)')
# 4 ONDERKAAK: bovenkant tong in schaduw = w (model grijs 188-198), rest r4. Binnenrand lipband rechts/mondhoek (X17) uit het model.
for X,Y in ((14,45),(15,47)): zet(X,Y,'w','4 tongvlees grijs (pit eerst weg)')
# Gen 3-opbouw (Croconaw/Exploud/Gyarados: tong licht vooraan-links, schaduw achterin/rechtsboven; licht linksboven):
# voorste deel van de grijze tongtop -> wit, grijs blijft achterin (X14-16, Y45-48) waar het model ook grijs is.
for X,Y in ((12,46),(13,46),(11,47),(12,47),(13,47)): zet(X,Y,'W','4 tong vooraan licht (Gen 3-opbouw; model grijs 188-198)')
for X,Y,c in ((17,44,'r'),(17,46,'r'),(17,47,'r')): zet(X,Y,c,'4 mondhoek/binnenrand lipband (modeltoon)')
# PITJES: modelcomponenten (zwaartepunt -> spritepx), sterkste eerst; alleen op vlees, geen 8-buur pit,
#   hooguit 1 niet-vlees 4-buur, niet naast de verre lip/kaaklijn (4-buur).
for X,Y in zip(*np.where(o.T==12)): zet(X,Y,'W' if r4[Y,X]==12 and Y>=48 else 'w','pit opnieuw kiezen')
comps=[(913,10,48),(856,11,44),(798,10,43),(763,9,51),(705,14,49),(633,16,45),(594,11,51),(480,13,46),(477,12,50),(474,15,47),
 (464,14,47),(435,11,47),(374,8,45),(373,11,43),(326,12,48),(317,13,44),(310,9,50),(248,11,49),(247,12,43),(242,11,50),(236,13,46)]
VL={I['w'],I['W'],I['v']}; pits=[]
BAND={(9,45),(10,45),(10,46),(11,46),(12,45),(13,45),(10,47),(11,42),(12,43),(13,43),(14,44),(15,44),(16,44)}
for w,X,Y in comps:
    if o[Y,X] not in VL: continue
    if any(abs(X-x)<=1 and abs(Y-y)<=1 for x,y in pits): continue
    if any((abs(X-x)==2 and Y==y) or (abs(Y-y)==2 and X==x) for x,y in pits): continue
    nb=[o[Y+dy,X+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if sum(v not in VL for v in nb)>(2 if w>=900 else 1): continue   # sterkste modelpit (6 natieve px) mag in de hoek van de lipband
    if w<900 and any((X+dx,Y+dy) in BAND for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): continue
    pits.append((X,Y)); zet(X,Y,'s','pit (modelcomponent %d)'%w)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save('pitahaya2_r5.png',transparency=0)
diff=list(zip(*np.where(o!=r4)))
ZONE=lambda y,x: 2<=x<=22 and 40<=y<=56
buiten=[d for d in diff if not ZONE(*d)]; assert not buiten, buiten
sil=[(x,y) for y,x in zip(*np.where((o>0)!=(r4>0)))]; assert not sil, sil
print('r5: gewijzigd', len(diff), 'buiten zone 0, silhouet gelijk; pits', pits, 'kleuren', len(set(o.flatten())))
open('pitahaya2_r5_afwijkingen.txt','w').write('\n'.join('\t'.join(map(str,l)) for l in log)+'\n')
for l in log: print(l)
