# Samengesteld Claydol-model op modelresolutie (natief raster 99x99, pitch 10,24), alleen knippen/plakken uit bronpixels:
#  basis r5; afwerking rond de twee grote ogen uit r3; derde oog weg (steen uit dezelfde rij overgenomen);
#  krans . - . - : stipjesogen uit r6, streepjesogen uit r5 (zelfde plekken; symmetrisch rond de punt, begint met een stipje).
import numpy as np; from PIL import Image
B='claydol_model/'
r5=np.asarray(Image.open(B+'natief_r5.png')).astype(int)
r3=np.asarray(Image.open(B+'natief_r3.png')).astype(int)
r6=np.asarray(Image.open(B+'natief_r6.png')).astype(int)
M=r5.copy(); bron=np.full(r5.shape[:2],'5',dtype='<U2')
def rood(a): return (a[:,:,0]-a[:,:,1])>40
H,W=r5.shape[:2]; yy,xx=np.mgrid[0:H,0:W]
# 1) derde oog weg: x 60..bnd-1 = steen van kolom 59 (zelfde rij), bnd..67 = facetsteen van kolom 68 (zelfde rij).
#    bnd = facetgrens, doorgetrokken tussen rij 34 (x66) en rij 46 (x67) langs de rand van het facet.
bnd={33:66,34:66,35:67,36:67,37:68,38:68,39:68,40:68,41:68,42:68,43:68,44:68,45:68,46:67}
for y,b in bnd.items():
    for x in range(60,68):
        if rood(r5)[y,x]: continue
        if y<=34 and r5[y,x].mean()<130: continue   # boven het oog: facetpixels zelf blijven
        M[y,x]=r5[y,59] if x<b else r5[y,68]; bron[y,x]='s' if x<b else 'f'
# 2) afwerking rond de ogen uit r3: ring net buiten de oogomlijning (genormaliseerde afstand 1,0-1,5),
#    niet op de neus (x38-44), niet op/boven de rode lijn, niet op de kopomlijning.
ogen=[(32.0,40.5,6.0,6.5),(50.5,41.5,6.5,6.5)]
ring=np.zeros((H,W),bool)
for cx,cy,rx,ry in ogen:
    d=np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2); ring|=(d>1.0)&(d<=1.5)
ring&=~((xx>=38)&(xx<=44)&(yy>=33)&(yy<=52))
ring&=~rood(r5)&~rood(r3)&(yy>=33)
ring&=(xx>=25)&(xx<=58)          # x24 = kopomlijning (krans ernaast); x59+ is in r3 al de omlijning/het wit van r3's derde oog
ring&=r5.mean(2)>40              # zwarte kopomlijning van r5 blijft
M[ring]=r3[ring]; bron[ring]='3'
# 3) krans: stipjesogen = heel het krans-oogvak uit r6 (r6 verschilt daar ook in de belichting; half overnemen gaf mengpixels),
#    streepjes blijven r5. Vakken: x0,y0,x1,y1 (natief); K5/R5 zo smal dat de staf erbuiten valt.
stip=[(35,14,42,22),(18,27,28,36),(23,47,28,53),(53,14,62,22),(71,27,81,37),(66,47,75,55)]
d6=np.abs(r5-r6).sum(2)>40
for x0,y0,x1,y1 in stip:
    m=np.zeros((H,W),bool); m[y0:y1+1,x0:x1+1]=True; m&=~ring
    M[m]=r6[m]; bron[m]='6'
Image.fromarray(M.astype('uint8')).save(B+'model_natief_samengesteld.png')
Image.fromarray(M.astype('uint8')).resize((W*10,H*10),Image.NEAREST).crop((80,80,900,900)).save(B+'model_samengesteld.png')
np.save(B+'bron.npy',bron)
for k,n in [('3','uit r3 (oogafwerking)'),('6','uit r6 (stipjes)'),('s','steen kol.59 (derde oog weg)'),('f','facetsteen kol.68 (derde oog weg)')]:
    print(n,(bron==k).sum())
