"""Silhouet kolibrie pre-evo, v1.
Bron: Jordi's foto 1 (zittende jonge kolibrie, kop links), omtrek punt voor punt (fotocoördinaten).
Zones met de hand aangepast: kop 1,3x geschaald (fase 1: grote kop), lange snavel vervangen door een
kort open bekje (foto 3, nestjong dat om eten vraagt), staart ingekort tot stompje, pootjes los op de grond (geen tak).
"""
from PIL import Image, ImageDraw
import numpy as np, sys
W,H=1065,800
def poly(pts, scale=1.0, c=(0,0)):
    return [((x-c[0])*scale+c[0],(y-c[1])*scale+c[1]) for x,y in pts]
# lijf: rug, vleugel ingeklapt, buik (zonder kop en snavel)
lijf=[(395,250),(380,275),(385,300),(410,315),(418,350),(420,400),(428,450),(440,490),(455,520),(478,545),
      (520,562),(560,575),(600,585),(640,595),(668,610),(690,600),(692,560),(688,510),(680,455),(662,400),
      (635,350),(605,315),(578,285),(560,250),(500,250)]
# kop (omtrek foto 1: voorhoofd, kruin, achterhoofd, keel)
kop=[(395,205),(415,180),(445,163),(480,158),(512,168),(540,190),(556,218),(560,250),(540,275),(500,290),
     (440,295),(400,280),(380,255),(378,228)]
kc=(470,228)
staart=[(640,590),(700,605),(712,640),(680,650),(640,625)]
pootjes=[[(485,545),(478,585),(492,585),(500,550)],[(540,560),(538,598),(552,598),(556,565)]]
def bek(scale, kc, open_=True):
    # kort open bekje: punt van de kop links, bovensnavel iets omhoog, ondersnavel omlaag (gaap)
    bx,by=poly([(392,215)],scale,kc)[0]
    L=95
    boven=[(bx+8,by-14),(bx-L,by-28),(bx-L+6,by-18),(bx+8,by+4)]
    onder=[(bx+8,by+8),(bx-L*0.85,by+30),(bx-L*0.85+8,by+38),(bx+12,by+26)]
    return [boven,onder]
def maak(kopschaal=1.3, doel_h=40):
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    for p in [lijf,staart]+pootjes: d.polygon(p,fill=255)
    d.polygon(poly(kop,kopschaal,kc),fill=255)
    for p in bek(kopschaal,kc): d.polygon(p,fill=255)
    a=np.asarray(im)>0; ys,xs=np.nonzero(a)
    crop=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    s=doel_h/crop.height
    small=crop.resize((max(1,round(crop.width*s)),doel_h),Image.LANCZOS)
    m=(np.asarray(small)>=128)
    out=np.zeros((64,64),bool); h,w=m.shape
    ox=(64-w)//2; oy=64-h-6
    out[oy:oy+h,ox:ox+w]=m
    return out,im
if __name__=='__main__':
    out,big=maak()
    Image.fromarray((~out*255).astype('uint8')).save('silhouet_v1_1x.png')
    big.save('onderlaag_v1_groot.png')
    print('px',out.sum())
