"""Silhouet kolibrie pre-evo, v2 (bolletje).
Bron lijf: Jordi's foto 5 (uitvlieger in de hand), gespiegeld zodat de kop links zit; omtrek punt voor punt
(coördinaten in de gespiegelde uitsnede 500..880 x 780..1100). Zones met de hand: bek vervangen door een
open bedelbekje schuin omhoog (foto 3), opstaande vleugelpunten weggelaten (lazen als oren, les eindvorm),
kort staartstompje rechtsonder (foto 1), twee pootjes.
"""
from PIL import Image, ImageDraw
import numpy as np
W,H=420,360
blob=[(98,112),(112,96),(140,82),(180,68),(220,60),(262,60),(300,70),(328,92),(340,130),(336,180),
      (324,222),(304,258),(266,288),(222,300),(180,296),(134,280),(106,250),(92,210),(88,170),(92,140)]
boven=[(104,104),(40,58),(46,52),(118,96)]          # bovensnavel schuin omhoog-links
boven=[(118,98),(98,102),(38,56),(110,128)]
onder=[(104,140),(46,112),(52,124),(110,152)]       # ondersnavel: open gaap
staart=[(310,240),(368,280),(360,300),(300,282)]
pootjes=[[(176,292),(170,316),(188,316),(194,294)],[(228,296),(226,318),(244,318),(246,296)]]
def maak(doel_h=38, delen=None):
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    for p in (delen or [blob,boven,onder,staart]+pootjes): d.polygon(p,fill=255)
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
    Image.fromarray((~out*255).astype('uint8')).save('silhouet_v2_1x.png')
    print('px',out.sum())
