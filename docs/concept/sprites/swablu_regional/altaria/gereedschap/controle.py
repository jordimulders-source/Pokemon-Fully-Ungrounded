# controle.py SPRITE.png (Altaria-palet): Gen 3-eisen meten (kleuren, kleine tintvlekjes, lichte buitenrand, losse zwarte pixels, zwart-%, helderheidsstappen)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(set(o.ravel())))
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),fg.sum()))
print('zwart %.1f%% | static %.1f%% van de figuur'%(100*(o==1).sum()/fg.sum(),100*(o==10).sum()/fg.sum()))
Lp=[.299*r+.587*g+.114*b for r,g,b in PAL]
print('helderheid wolk',[int(Lp[k]) for k in (2,3,4,5)],'violet',[int(Lp[k]) for k in (6,7,8)],'lavendelwit',int(Lp[9]),'static',int(Lp[10]))
for k in range(2,10):
    lab,n=label(o==k,acht=False); kl=[(lab==i).sum() for i in range(1,n+1)]
    pts=[tuple(int(t) for t in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px op %s'%(CH[k],k,len(pts),pts))
licht={4,5,8,9}
rand=[(int(X),int(Y),CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in licht and (not fg[Y,X-1] or not fg[Y,X+1] or not fg[Y-1,X] or not fg[Y+1,X])]
print('lichte kleur op de buitenrand (static niet meegeteld):',rand)
los=[(int(X),int(Y)) for Y,X in zip(*np.where(o==1)) if all(o[Y+dy,X+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
lab,n=label(o==10,acht=True); print('static-stukken (px):',sorted(int((lab==i).sum()) for i in range(1,n+1)))
