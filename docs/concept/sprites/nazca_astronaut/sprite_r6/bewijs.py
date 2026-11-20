# alpha-diff t.o.v. r4 en: kop + onderarmen + onderbenen ongewijzigd (RGB) t.o.v. r4-A
import numpy as np; from PIL import Image
def rgb(f):
    im=Image.open(f); p=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(16,3); return p,pal[p]
p4,c4=rgb('../sprite_r4/astro_A.png')
o=np.load('mat.npy'); H,W=o.shape; x0=(64-W)//2; y0=64-H
r4=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r4/rollen_hand.txt') if l.strip()])
pat=np.zeros((64,64),bool); pat[y0:y0+H,x0:x0+W]=(o!=r4)
for f in ['astro_P1.png','astro_P2.png']:
    p,c=rgb(f); a=((p>0)!=(p4>0)).sum(); d=(c!=c4).any(2)&(p>0)
    buiten=d&~pat
    ys,xs=np.where(d)
    print(f,'alpha-diff',a,'| kleur anders:',d.sum(),'px, png-rijen %d-%d'%(ys.min(),ys.max()),'| anders buiten patroonzone:',buiten.sum(), list(zip(*np.where(buiten)))[:12])
print('kopzone (png-rij < %d) in patroonzone:'%(y0+20), pat[:y0+20].sum())
