# controle.py SPRITE.png [KAAL.png]: Gen 3-eisen meten (kleuren, kleine tintvlekjes, lichte buitenrand, losse zwarte pixels) + afwijking van kaal
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(set(o.ravel())),'palet',len(im.getpalette())//3)
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
for k in sorted(set(o.ravel())-{0,1}):
    lab,n=label(o==k,acht=False); pts=[tuple(int(v) for v in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px op %s'%(CH[k],k,len(pts),pts))
rand=[(int(X),int(Y),CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in (4,5,6,9,11,15) and (not fg[Y,X-1] or not fg[Y,X+1] or not fg[Y-1,X] or not fg[Y+1,X])]
print('lichte kleur op de buitenrand:',rand)
los=[(int(X),int(Y)) for Y,X in zip(*np.where(o==1)) if all(o[Y+dy,X+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels (niet aan rand/lijn):',los)
if len(sys.argv)>2:
    k=np.asarray(Image.open(sys.argv[2])).astype(int); d=k!=o; print('afwijkend van kaal:',d.sum(),'px')
