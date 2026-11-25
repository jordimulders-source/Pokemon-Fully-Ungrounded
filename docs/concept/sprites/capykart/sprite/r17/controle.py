# controle.py SPRITE.png: Gen 3-eisen meten (formaat, kleuren, tintvlekjes <3 px, lichte buitenrand, losse zwarte pixels, zwart-%)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'sprite/r17'); from gemeen import label
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
CH='.K23456hHyrRBLgG'
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(im.getpalette())//3 if False else len(set(o.ravel())))
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),fg.sum()))
print('zwart %.1f%% van de figuur'%(100*(o==1).sum()/fg.sum()))
for k in range(2,16):
    lab,n=label(o==k,acht=(k in (2,7))); pts=[tuple(int(v) for v in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px op %s'%(CH[k],k,len(pts),pts))
licht={5,6,9,10,12,14}
rand=[(int(X),int(Y),CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in licht and (not fg[Y,X-1] or not fg[Y,X+1] or not fg[Y-1,X] or not fg[Y+1,X])]
print('lichte kleur op de buitenrand:',rand)
los=[(int(X),int(Y)) for Y,X in zip(*np.where(o==1)) if all(o[Y+dy,X+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
