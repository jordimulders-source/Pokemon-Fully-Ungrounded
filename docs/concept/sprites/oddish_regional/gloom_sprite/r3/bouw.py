# r3 = r2 + lavatinten in de brok (per kierpixel gemeten op het model) + afwerking. Vorm/plek van de kieren ongewijzigd.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen(); c[:20]=0; c[122:]=0; c[:,:21]=0; c[:,127:]=0
im=Image.open('r2/gloom_r2.png'); o=np.array(im).astype(int); r2=o.copy()
pal=im.getpalette()[:45]+[150,40,32]          # 15 = sintel (donkerste gloed, kier in de schaduw)
RANG=[15,9,10,11]                             # sintel < diep < oranje < geel
tel={}
# --- 1. kieren in de brok: tint naar gemeten modelgloed per pixel; schaduwkant van de brok (rechts/onder) één stap donkerder ---
kier=[(X,Y) for Y in range(11,26) for X in range(17,41) if o[Y,X]==10]
for X,Y in kier:
    f=l=0
    for u,v,w in overlap(X,Y):
        if c[v,u]==4: f+=w; l+=w*L[v,u]
    m=l/f if f else 130
    r=1 if m<118 else 2 if m<150 else 3
    if X>=34 or Y>=23: r-=1                   # schaduwkant (licht linksboven)
    if X<=26 and Y<=19 and r<3: r+=0
    o[Y,X]=RANG[max(r,0)]
tel['lava']=int((o!=r2).sum())
# --- 2. afwerking (x,y,van,naar; oude waarde gecontroleerd) ---
W=[(32,35,1,5),(32,36,1,5),(33,37,1,5),(32,38,1,5),   # mondring rechts: buitenring = bordeaux (model donker bordeaux, zoals links), alleen de binnenlijn zwart
   (31,38,6,1),                                       # binnenlijn opening rechts doorlopend (model: doorgaande donkere curve, reductie brak hem op 1 px)
   (14,40,6,7),(15,40,6,7),                           # vinnetje links: los 2-px schaduwvlekje -> midden (schaduw blijft eronder op y41)
   (30,36,9,10)]                                      # los diep-gloedpixel in de mond -> oranje
for x,y,v,n in W:
    assert o[y,x]==v,(x,y,o[y,x],v); o[y,x]=n
tel['afwerking']=len(W)
def save(o,p):
    q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(pal+[0]*(768-len(pal))); q.save(p,transparency=0)
save(o,'r3/gloom_r3.png')
toon(o,10,53,3,55); print(tel)
for n,(sl) in {'lavabrok':(slice(11,26),slice(17,41)),'mond':(slice(32,42),slice(18,35)),'vin links':(slice(38,43),slice(8,17))}.items(): print(n,int((o[sl]!=r2[sl]).sum()))
