# r3 = r2 + benoemde reparaties na keuring (BIJNA), alles uit het model gelezen met celfrac.py / modelcel.py.
# Bewijst diff 0 buiten de zones. Coordinaten hier sprite-lokaal (canvas = lokaal + (10,6)).
import json, numpy as np
from collections import Counter
from PIL import Image
src=json.load(open('r2/grid.json')); OX,OY=src['OX'],src['OY']
g=[list(r) for r in src['grid']]; H=len(g); W=len(g[0])
# silhouet groeit: kolom/rij erbij niet nodig (alles binnen 43x52)
ZONES={'kuif':(14,8,19,12),'haarlijnen':(5,13,15,18),'oog':(12,19,18,25),'mond':(9,28,14,30),'borst':(16,34,18,39)}
log=[]
def put(z,x,y,c,why):
    x0,y0,x1,y1=ZONES[z]; assert x0<=x<=x1 and y0<=y<=y1,(z,x,y)
    if g[y][x]!=c: log.append((z,x,y,g[y][x],c,why)); g[y][x]=c
# 1 kuif (model: donkerbruine bovenrand x15-17 y9, inkeping (17,10), tweede trede (18,11) met zwarte rand rechts)
put('kuif',17,9,'D','bovenrand pluk loopt door in donkerbruin (model D44)')
put('kuif',17,10,'D','inkeping tussen de twee trappen (model 0 47) als binnenlijn')
put('kuif',16,11,'D','haarlijn in de pluk (model D35)')
put('kuif',18,11,'M','tweede trede van de pluk (model licht/donker gemengd)')
put('kuif',19,11,'0','zwarte rand rechts van de tweede trede (model zwarte rand x18.7-19)')
# 2 haarlijnen: A (9,14)-(9,15)-(10,16)-(10,17), B (12,16)-(13,16)-(13,17), C (8,16)-(8,17); rest vlaktint uit het model
put('haarlijnen',6,13,'S','vlak: model D49/S30, donker vlak i.p.v. M-blokje')
put('haarlijnen',10,13,'L','vlak: model L37 (geen lijn)')
put('haarlijnen',9,15,'D','haarlijn A (model 0 32)')
put('haarlijnen',10,16,'D','haarlijn A (model 0 32)')
put('haarlijnen',10,17,'D','haarlijn A, taps einde (model 0 25)')
put('haarlijnen',9,17,'L','vlak: model L41 (los pixeltje weg)')
put('haarlijnen',11,17,'L','vlak: model L50 (los pixeltje weg)')
# 3 oog x12-18 y19-25, per cel uit celfrac.py (drempel zwart >=40%)
OOG=['-MMCCCM','-MC00CC','MCDDDDC','C0DC0DC','C0D00DC','D0SSS0C','DCCCCCM']
for j,row in enumerate(OOG):
    for i,c in enumerate(row):
        if c!='-': put('oog',12+i,19+j,c,'oog uit model (celfrac)')
# 4 mond/kin: mondlijn als binnenlijn, kin (1 px) en kaakonderrand zoals model
put('mond',10,28,'D','mondhoek (model 0 39) als binnenlijn')
for x in (11,12,13):
    put('mond',x,29,'S','kin/onderkaak (model S71-76)')
    put('mond',x,30,'0','onderrand kaak (model zwarte lijn op de celgrens 29/30)')
# 5 borst links: selout in donkerste tint i.p.v. licht creme op de buitenrand
for x,y in ((16,34),(16,35),(16,36),(18,39)): put('borst',x,y,'D','selout borst lichtkant (index 2)')
# --- bewijs diff 0 buiten de zones ---
r2=src['grid']; buiten=0
for y in range(H):
    for x in range(W):
        if r2[y][x]!=g[y][x] and not any(a<=x<=c and b<=y<=d for a,b,c,d in ZONES.values()): buiten+=1
print('diff buiten zones:',buiten); print('per zone:',dict(Counter(z for z,*_ in log)),'totaal',len(log))
PAL={'.':(0,0,0),'0':(24,16,20),'D':(66,34,18),'S':(108,58,26),'M':(160,92,40),'L':(194,120,56),'C':(244,221,190),'c':(212,174,132),
     'N':(106,76,64),'n':(140,110,94),'H':(132,102,70),'h':(184,148,106),'I':(62,66,78),'J':(86,92,104),'K':(110,116,128)}
ORDER=list(PAL); img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]; [pal.extend(PAL[k]) for k in ORDER]; pal+=[0,0,0]*(16-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save('r3/dikdik_r3.png',transparency=0)
Image.open('r3/dikdik_r3.png').convert('RGBA').resize((512,512),Image.NEAREST).save('r3/dikdik_r3_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'r2':r2},open('r3/grid.json','w'),indent=0)
with open('r3/log.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
