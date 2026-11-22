"""Proef: Jordi's krabbel (lijnen over het icoon) mechanisch omzetten, zonder maker.
Lijnen -> 1-px pixellijnen (afstand tot de streep <= drempel, daarna L-hoeken weg) ->
gebieden tussen de lijnen vlak gevuld met hun meerderheidskleur (geen blur) -> oog = gebied binnen de oog-ovaal.
python3 krabbel_raster.py uit.png [drempel]"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
uit=sys.argv[1]; DR=float(sys.argv[2]) if len(sys.argv)>2 else 0.42
a=np.array(Image.open(R+'krabbel_jordi_kop.png').convert('RGB')).astype(int)
base=np.array(Image.open(R+'icon_a2_af.png')); P=Image.open(R+'icon_a2_af.png').getpalette()
ic=base[:32].copy()
cs=24.75; x0=548.5-4*cs; y0=33.5-cs; OY,OX=7,0+2-4+4  # G[j,i] <-> icoon (7+j, 2+i) bij x0=548.5-4cs -> i=0 is kolom 2-? (zie meting)
OX=2
zwart=(a.max(2)<60)&(np.arange(a.shape[1])[None,:]>440)       # Jordi's zwarte streep (rechterpaneel)
bruin=(abs(a[...,0]-190)<40)&(abs(a[...,1]-140)<40)&(abs(a[...,2]-100)<45)&(np.arange(a.shape[1])[None,:]>440)
# bruine oorlijn alleen waar die niet op een bruine icoonpixel ligt is lastig; we nemen alleen zwart
dist=nd.distance_transform_edt(~zwart)
lijn=np.zeros((32,32),bool)
for j in range(int((a.shape[0]-y0)//cs)):
    for i in range(int((a.shape[1]-x0)//cs)):
        cy,cx=y0+(j+.5)*cs,x0+(i+.5)*cs
        if cy>=a.shape[0] or cx>=a.shape[1]: continue
        d=dist[int(cy),int(cx)]
        if d<=DR*cs: lijn[OY+j,OX+i]=True
# L-hoeken weg (pixel-perfect lijnen): pixel met een buur boven/onder EN links/rechts, en die buren niet elkaars buur via hem
for _ in range(2):
    for y in range(1,31):
        for x in range(1,31):
            if not lijn[y,x]: continue
            v=lijn[y-1,x] or lijn[y+1,x]; h=lijn[y,x-1] or lijn[y,x+1]
            n=lijn[y-1:y+2,x-1:x+2].sum()-1
            if v and h and n==2: lijn[y,x]=False
sil=ic>0
kop=np.zeros((32,32),bool); kop[7:24,2:16]=True   # alleen het kopgebied (krabbelgebied)
L=lijn&sil&kop
# gebieden tussen de lijnen
pad=np.pad(sil,1); rand=sil&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
reg,nr=nd.label(sil&kop&~L&~rand)
out=ic.copy()
NORM={6:6,7:7,8:9,9:9,3:3,2:3,14:7,15:7,1:0}
for k in range(1,nr+1):
    m=reg==k; vals=[NORM.get(v,v) for v in ic[m] if v not in (14,15,1)]
    if not vals: continue
    c=np.bincount(vals).argmax()
    # klein gesloten gebied midden in de kop = oog (Jordi's ovaal)
    ys,xs=np.nonzero(m)
    if m.sum()<=3 and not (ys.min()==7 or xs.min()==2): c=15
    out[m]=c
out[L]=15
im=Image.fromarray(np.vstack([out,out]).astype(np.uint8),'P'); im.putpalette(P); im.save(uit)
for r in out[6:26,0:20]: print(''.join('.' if v==0 else '%x'%v for v in r))
