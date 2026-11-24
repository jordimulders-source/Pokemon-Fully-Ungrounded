# r3 basis: r2-sprite + maskers (kop, krans-middelpunten) in spritecoördinaten, uit dezelfde bronnen als r2.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'claydol_sprite_r2'); sys.path.insert(0,'claydol_sprite_r1')
from kaal2 import kaal
from klassen import klasse, PAL
from kopmasker import kopmasker
S2=np.array(Image.open('claydol_sprite_r2/claydol_r2.png')).astype(int)
KAAL,A,NY,NX=kaal(2)
V2=np.load('claydol_sprite_r2/vlakken.npy')
kn,_=klasse('claydol_sprite_r2/model_r2_s2.png'); KOPN=kopmasker(kn)
KOP=np.zeros((64,64),bool); ok=NY>=0; KOP[ok]=KOPN[NY[ok],NX[ok]]
KR={'K1':(38.5,17.5,'.'),'K2':(30.5,22.5,'-'),'K3':(22.5,31.5,'.'),'K4':(20.5,40.5,'-'),'K5':(26.0,50.0,'.'),
    'R1':(58.5,17.5,'.'),'R2':(66.5,22.5,'-'),'R3':(75.5,31.5,'.'),'R4':(76.5,40.5,'-'),'R5':(71.0,50.0,'.')}
def sp(cx,cy):
    m=NY>=0; xs=NX[m].ravel(); ys=NY[m].ravel(); X=np.where(m)[1]; Y=np.where(m)[0]
    o=np.argsort(xs); p=np.argsort(ys)
    return float(np.interp(cx,xs[o],X[o])), float(np.interp(cy,ys[p],Y[p]))
KRS={n:(*sp(cx,cy),t) for n,(cx,cy,t) in KR.items()}
def opslaan(S,pad):
    im=Image.fromarray(S.astype('uint8'),'P'); pal=[c for p in PAL for c in p]; pal+=[0]*(48-len(pal)); im.putpalette(pal)
    im.save(pad,transparency=0)
if __name__=='__main__':
    for n,v in KRS.items(): print(n,'%.1f %.1f %s'%v)
    for y in range(0,64): print('%2d '%y+''.join(('#' if KOP[y,x] else '0123456789ABCDEF'[S2[y,x]]) if S2[y,x] else '.' for x in range(64)))
