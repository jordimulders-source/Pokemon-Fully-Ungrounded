# r5 = r4a/r4b met Saturnus naar links tot 1 px van Mars (zelfde afstand als ijs-Mars). Alleen verplaatsen.
import numpy as np
from PIL import Image
from scipy import ndimage
for v in 'ab':
    s=Image.open(f'r4/regicosmo_r4{v}.png'); a=np.array(s)
    lab,n=ndimage.label(a>0,structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    sat=max(range(n),key=lambda i:objs[i][1].stop-objs[i][0].start*0.01)  # meest rechts
    mars=max(range(n),key=lambda i:(lab==i+1).sum())
    S=lab==sat+1; M=lab==mars+1
    def gap(m1,m2):
        d=ndimage.distance_transform_cdt(~m2,metric='chessboard'); return d[m1].min()-1
    print(v,'gap voor',gap(S,M))
    for dx in range(1,8):
        S2=np.roll(S,-dx,axis=1)
        if gap(S2,M)<1: break
        best=dx
    out=a.copy(); out[S]=0; yy,xx=np.nonzero(S); out[yy,xx-best]=a[yy,xx]
    print(v,'links',best,'gap na',gap(np.roll(S,-best,axis=1),M))
    o=Image.fromarray(out,'P'); o.putpalette(s.getpalette()); o.save(f'r5/regicosmo_r5{v}.png',transparency=0)
ims=[]
for f in ['r4/regicosmo_r4a.png','r5/regicosmo_r5a.png','r4/regicosmo_r4b.png','r5/regicosmo_r5b.png']:
    s=Image.open(f); a=np.array(s); rgb=np.array(s.convert('RGB')); rgb[a==0]=255; ims.append(Image.fromarray(rgb).resize((512,512),Image.NEAREST))
vel=Image.new('RGB',(512*4+48,512),(200,200,200))
for i,im in enumerate(ims): vel.paste(im,(i*528,0))
vel.save('r5/vel.png')
