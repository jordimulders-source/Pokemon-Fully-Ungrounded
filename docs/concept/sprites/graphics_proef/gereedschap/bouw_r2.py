# Ronde 2 rugsprites: Sunperor (p1 + kop uit p3) en Hexpress (p4).
# python3 gereedschap/bouw_r2.py   (vanuit docs/concept/sprites/graphics_proef)
import numpy as np; from PIL import Image
from collections import Counter
SP='../'; K='kandidaat/'
def mapc(nat,pal,allowed):
    a=np.array(Image.open(nat).convert('RGB')).astype(int); bg=a.min(2)>215
    P=np.array(pal[:48]).reshape(-1,3)[allowed]
    d=((a[:,:,None,:]-P[None,None])**2).sum(3); idx=np.array(allowed)[d.argmin(2)]; idx[bg]=0
    return idx
def save(arr,pal,name):
    im=Image.fromarray(arr.astype('uint8'),'P'); im.putpalette(pal); im.info['transparency']=0
    im.save(K+name,transparency=0)
    p=list(pal); p[0:3]=[255,255,255]; w=Image.fromarray(arr.astype('uint8'),'P'); w.putpalette(p)
    w.convert('RGB').resize((arr.shape[1]*8,arr.shape[0]*8),Image.NEAREST).save(K+name.replace('.png','_8x.png'))
log=[]
# ================= 1. Sunperor rug v2 =================
fr=Image.open(SP+'koningstiran/af/sapa_inca.png'); sp=fr.getpalette(); sf=np.array(fr)
base=np.array(Image.open(K+'sunperor_rug_A_gaten_open.png')).astype(int)   # p1, gaten open; natief y -> y+9, x gelijk
DY=9
p3=mapc('nat_sunperor_rug_p3.png',sp,list(range(1,16)))
# kopmasker in p3 (natieve coords; kroonrand rij 21 is in p1 en p3 gelijk, dus zelfde plek)
KOP={22:range(32,37), 23:range(32,38), 24:range(31,39), 25:range(32,40), 26:range(32,40), 27:[33,34,38,39]}
kop=p3.copy()
kop[27,39]=13            # donkere snavelpunt (48576b) viel op bruin 3
kop[23,37]=14            # lichtste snavelpixel (f1f4fb) viel als achtergrond weg
for y,xs in KOP.items():  # lila (9) in de snavel = paletmisser -> licht snavelgrijs
    for x in xs:
        if kop[y,x]==9: kop[y,x]=14
v2=base.copy()
# oude p1-snavel weg (x37-41, rij 22-28), behalve wat de staf/kroon is (die ligt verder rechts)
for y in range(22,29):
    for x in range(37,42): v2[y+DY,x]=0
for y,xs in KOP.items():
    for x in xs: v2[y+DY,x]=kop[y,x]
log.append('sunperor v2: %d px anders dan versie A'%(v2!=base).sum())
save(v2,sp,'sunperor_rug_v2.png')
# ================= 2. Hexpress rug =================
fr=Image.open(SP+'spooktrein_fase3/af/spooktrein.png'); hp=fr.getpalette(); hf=np.array(fr)
h=mapc('nat_hexpress_rug_p4.png',hp,list(range(1,16)))
GROEN={2,3,4,5,6,13}
def vul(a,punten):
    # vul punten met de meest voorkomende rooktint van de buren (5x5), van buiten naar binnen
    todo=set(punten)
    for p in todo: a[p[1],p[0]]=-1
    while todo:
        klaar=[]
        for (x,y) in todo:
            nb=[a[j,i] for j in range(y-2,y+3) for i in range(x-2,x+3)
                if 0<=j<a.shape[0] and 0<=i<a.shape[1] and a[j,i] in GROEN]
            if len(nb)>=3: klaar.append(((x,y),Counter(nb).most_common(1)[0][0]))
        if not klaar: break
        for (x,y),v in klaar: a[y,x]=v; todo.discard((x,y))
    return a
h0=h.copy()
# streep linksonder in de rook (niet-groene pixels rij 37-41, x 0-21) + het witte lijntje dat ermee
# meeloopt naar de linkerrand (gaten in rij 37-40, x 0-9)
streep=[(x,y) for y in range(37,42) for x in range(0,22) if h[y,x] and h[y,x] not in GROEN]
gaten=[(x,y) for y in range(37,41) for x in range(0,10) if h[y,x]==0]
h=vul(h,streep+gaten)
# los ruispixel: grijs (38,1) midden in de rook
h=vul(h,[(38,1)])
log.append('hexpress: streep %d px, gaten %d px, ruis 1 px; totaal %d px anders dan kale omzetting'%(len(streep),len(gaten),(h!=h0).sum()))
ys,xs=np.where(h>0)
dx=2-xs.min(); dy=63-ys.max()
hx=np.zeros((64,64),int)
for y,x in zip(ys,xs): hx[y+dy,x+dx]=h[y,x]
log.append('hexpress geplaatst: x %d-%d, y %d-%d'%(xs.min()+dx,xs.max()+dx,ys.min()+dy,ys.max()+dy))
save(hx,hp,'hexpress_rug.png')
# ================= vergelijkingsvel =================
def rgb(a,pal):
    p=list(pal); p[0:3]=[255,255,255]; im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(p); return im.convert('RGB')
rows=[[Image.open('nat_sunperor_rug_p1.png').convert('RGB'),Image.open('nat_sunperor_rug_p3.png').convert('RGB'),rgb(v2,sp),rgb(sf,sp)],
      [Image.open('nat_hexpress_rug_p4.png').convert('RGB'),None,rgb(hx,hp),rgb(hf,hp)]]
C=64*8+16
vel=Image.new('RGB',(4*C,2*C),(255,255,255))
for i,r in enumerate(rows):
    for j,im in enumerate(r):
        if im is None: continue
        vel.paste(im.resize((im.width*8,im.height*8),Image.NEAREST),(j*C,i*C))
vel.save(K+'vergelijking_r2.png')
print('\n'.join(log))
for n,pal in [('sunperor_rug_v2.png',sp),('hexpress_rug.png',hp)]:
    a=np.array(Image.open(K+n)); print(n,Image.open(K+n).mode,a.shape,'kleuren',len(set(np.unique(a))-{0}))
