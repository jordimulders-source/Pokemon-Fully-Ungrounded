# Ronde 2: reparaties op r1/mate_variant_vlek.png, alles gemeten op het model (omtrek.py, dekking.py, meerderheid.py,
# randmetingen per halve rij in het 1024-model). Niets getekend: elke pixel staat op een gemeten modelplek.
import numpy as np; from PIL import Image
im=Image.open('r2/basis.png'); PAL=im.getpalette(); a=np.asarray(im).astype(int); b=a.copy()
L={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'G':6,'H':7,'I':8,'s':9,'t':10,'u':11}
Z={'mond':(17,46,30,54),'omtrek':None,'hand_l':(11,40,16,50),'oog_r':(27,34,35,43)}
REP=[]
# 1. mond: modelcontour per halve rij (hoeken r47, bovenlijn zakt naar r49 in het midden, zijkanten schuin, onderboog r53, lip eronder)
M={47:"c#ccccccc##c",48:"####ccc##aa#",49:"c#aa###aaaa#",50:"c#aaaaaaaaa#",51:"bd#aaaaaaa#c",52:"bbd#aaaaa#dc"}
for y,r in M.items():
    for i,ch in enumerate(r): REP.append(('mond',18+i,y,ch))
for i,ch in enumerate("bbd#####dc"): REP.append(('mond',19+i,53,ch))
REP+= [('mond',24,54,'d'),('mond',25,54,'d')]
# 2. omtrek: buitenrand op de gemeten modelcurve (model L/R per rij)
REP+= [('omtrek',50,46,'#'),('omtrek',49,46,'b'),     # R 50,6 (was 50)
       ('omtrek',15,50,'#'),                          # L 15,1 (was 16)
       ('omtrek',18,54,'#'),                          # L 18,4 (was 19)
       ('omtrek',12,43,'.'),('omtrek',13,43,'a')]     # hand: recht stuk x12 van 5 naar 4 rijen, hoek afgerond
# 3. nabije hand: glans linksboven (model d), vingerlijn (model a), schaduw onderin (model b)
REP+= [('hand_l',14,42,'d'),('hand_l',13,44,'d'),('hand_l',14,45,'a'),('hand_l',13,47,'b'),('hand_l',14,48,'b')]
# 4. rechteroog: groen ovaal volgens modelgrenzen per halve rij, zwarte rand boven/links/rechts, donkerbruine onderrand, lip
REP+= [('oog_r',33,36,'c'),('oog_r',28,38,'#'),('oog_r',29,38,'H'),('oog_r',28,39,'#'),('oog_r',29,39,'H'),('oog_r',34,40,'#'),
       ('oog_r',31,41,'H'),('oog_r',32,41,'H'),('oog_r',33,41,'a'),('oog_r',31,42,'a'),('oog_r',32,42,'a'),('oog_r',33,42,'d')]
per={}
for z,x,y,ch in REP:
    v=L[ch]
    if b[y,x]!=v: b[y,x]=v; per[z]=per.get(z,0)+1
p=Image.fromarray(b.astype('uint8'),'P'); p.putpalette(PAL); p.save('r2/mate.png',transparency=0)
d=b!=a; print('gewijzigd per zone',per,'totaal',int(d.sum()))
# bewijs: diff 0 buiten de zones
zones=[(17,46,30,54),(11,40,16,50),(27,34,35,43),(49,46,50,46),(15,50,15,50),(18,54,19,54)]
buiten=[(x,y) for y,x in zip(*np.where(d)) if not any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in zones)]
print('diff buiten de zones:',len(buiten),buiten)
