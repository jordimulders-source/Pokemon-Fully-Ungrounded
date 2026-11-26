# Gen 3-controle: maat, kleuren, transparantie, lichte kleur op de buitenrand, losse pixels, zwart-aandeel, pixeldiff tussen varianten.
import sys, numpy as np; from PIL import Image
from gemeen import PAL, NAAM, lum
fs=sys.argv[1:]
for f in fs:
    im=Image.open(f); o=np.array(im)
    print('==',f,im.size,im.mode,'transparency',im.info.get('transparency'))
    ys,xs=np.where(o>0); print(' figuur %dx%d (x%d-%d, y%d-%d), %d px, kleuren incl. transparant: %d'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1,xs.min(),xs.max(),ys.min(),ys.max(),(o>0).sum(),len(set(o.ravel()))))
    def g(y,x): return o[y,x] if 0<=y<64 and 0<=x<64 else 0
    licht=[(x,y,NAAM[o[y,x]]) for y,x in zip(ys,xs) if any(g(y+dy,x+dx)==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))) and lum(PAL[o[y,x]])>100]
    print(' lichte kleur op de buitenrand:',licht)
    los=[(x,y,NAAM[o[y,x]]) for y,x in zip(ys,xs) if all(g(y+dy,x+dx)!=o[y,x] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
    print(' losse pixels (geen gelijke 8-buur): %d'%len(los),los)
    print(' zwart %.1f%% van de figuur'%(100*(o==1).sum()/(o>0).sum()))
    for k in sorted(set(o.ravel())-{0}): print('   %2d %-14s %4d px'%(k,NAAM[k],(o==k).sum()))
if len(fs)>1:
    a=np.array(Image.open(fs[0]))
    for f in fs[1:]:
        b=np.array(Image.open(f)); ys,xs=np.where(a!=b)
        print('diff',fs[0],'<->',f,len(ys),'px, vak x%d-%d y%d-%d'%(xs.min(),xs.max(),ys.min(),ys.max()) if len(ys) else '')
