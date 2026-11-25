# r5 = r4B + reparaties na keuring r4B. Lokaal = absoluut - (10,6). Diff 0 buiten de zones (bewezen).
import json, numpy as np
from collections import Counter
from PIL import Image
src=json.load(open('r4/grid_B.json')); OX,OY=src['OX'],src['OY']; R=src['grid']
g=[list(r) for r in R]; H=len(g); W=len(g[0])
ZONES={'oog':(12,19,19,26),'veroog':(5,17,6,22),'kammetje':(5,15,13,17),'contour':(3,11,7,19),'borst':(18,38,24,41)}
log=[]
def put(z,x,y,c,why):
    a,b,cc,d=ZONES[z]; assert a<=x<=cc and b<=y<=d,(z,x,y)
    if g[y][x]!=c: log.append((z,x,y,g[y][x],c,why)); g[y][x]=c
# 1 nabij oog: ring 1 px (rechts alleen x18, onder alleen y25), iris ~4x4 (y24 x14-17 donker, donkerst midden-onder)
OOG={19:'--CCCC--',20:'-C000CC-',21:'C000DDCM',22:'C00C0DCM',23:'C0000DCM',24:'DDD00DCM',25:'DCCCCCMM',26:'LLLLLLSS'}
for y,row in OOG.items():
    for i,c in enumerate(row):
        if c!='-': put('oog',12+i,y,c,'oog: dunne ring 1 px / grote iris (model); vacht/traanvlek naar model')
# 2 ver oog: zwart ovaal op x5-6 y17-22 (model zwart x4.6-6.3, y17.3-22), 1 glimlicht binnen de rand; creme (6,18) -> kopkleur
put('veroog',5,17,'0','ver oog: zwart ovaal (model 0)')
put('veroog',6,18,'L','ver oog: creme weg, kopkleur (model L)')
put('veroog',6,19,'C','ver oog: 1 glimlicht binnen de buitenrand (model creme x5.3 y19-20)')
for y in (20,21): put('veroog',6,y,'0','ver oog: zwart ovaal (model 0 39)')
for y in (20,21,22): put('veroog',5,y,'0','ver oog: zwart ovaal (model 0 55-70)')
# 3 kammetje: haarlijn (9,14)-(9,15)-(8,16)-(8,17) en (12,16)-(13,16)-(13,17) blijven; stipjes x10 -> kopkleur
put('kammetje',10,16,'L','stipje weg, kopkleur (model L50)')
put('kammetje',10,17,'L','stipje weg, kopkleur (model L50)')
# KAN contour: onderkant ver oor (schaduwkant) doorlopend zwart i.p.v. om en om
put('contour',4,12,'0','onderrand ver oor: zwart doorlopend (geen om-en-om)')
# KAN borst: lichte schaduwrand onder in tint 7 waar het model donkerder creme toont
for x,y in ((19,39),(23,39),(20,40),(21,40),(22,40),(22,41),(23,41)): put('borst',x,y,'c','borst: schaduwrand onder (model tan creme)')
buiten=sum(1 for y in range(H) for x in range(W) if g[y][x]!=R[y][x] and not any(a<=x<=c and b<=y<=d for a,b,c,d in ZONES.values()))
print('diff buiten zones:',buiten,'| per zone:',dict(Counter(z for z,*_ in log)),'totaal',len(log))
PAL={'.':(0,0,0),'0':(24,16,20),'D':(66,34,18),'S':(108,58,26),'M':(160,92,40),'L':(194,120,56),'C':(244,221,190),'c':(212,174,132),
     'N':(106,76,64),'n':(140,110,94),'H':(132,102,70),'h':(184,148,106),'I':(62,66,78),'J':(86,92,104),'K':(110,116,128)}
ORDER=list(PAL); img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]; [pal.extend(PAL[k]) for k in ORDER]; pal+=[0,0,0]*(16-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save('r5/dikdik_r5.png',transparency=0)
Image.open('r5/dikdik_r5.png').convert('RGBA').resize((512,512),Image.NEAREST).save('r5/dikdik_r5_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g]},open('r5/grid.json','w'),indent=0)
with open('r5/log.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
for y in range(10,27): print('%2d '%y+''.join(g[y][:22]))
