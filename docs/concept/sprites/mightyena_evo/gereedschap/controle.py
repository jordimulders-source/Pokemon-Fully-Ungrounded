# controle.py SPRITE.png: Gen 3-eisen meten (kleuren, kleine tintvlekjes, lichte buitenrand, losse zwarte pixels, zwart-%, zwart/selout om en om)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(set(o.ravel())))
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
print('zwart %.1f%% van de figuur'%(100*(o==1).sum()/fg.sum()))
for k in range(2,14):
    lab,n=label(o==k,acht=(k in (2,3,4,11))); pts=[tuple(np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px op %s'%(CH[k],k,len(pts),pts))
P=np.pad(o,1); F=P>0
rand=[(X,Y,CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in (6,7,8,13) and not all(F[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))]
print('lichte kleur op de buitenrand:',rand)
los=[(X,Y) for Y,X in zip(*np.where(o==1)) if all(P[Y+1+dy,X+1+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
# om en om op de rand: randpixel zwart met een randbuur selout (4) en omgekeerd, langs dezelfde rand (tellen)
r=[(X,Y) for Y,X in zip(yy,xx) if not all(F[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))]
R=set(r); wissel=[(X,Y) for X,Y in r if o[Y,X]==4 for dx,dy in ((1,0),(0,1),(1,1),(1,-1),(-1,0),(0,-1),(-1,-1),(-1,1)) if (X+dx,Y+dy) in R and o[Y+dy,X+dx]==1]
# om en om = een seloutpixel met aan twee kanten zwart op de rand en zelf geen seloutbuur op de rand
om=[(X,Y) for X,Y in set(wissel) if not any((X+dx,Y+dy) in R and o[Y+dy,X+dx]==4 for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy)]
print('randovergangen selout<->zwart:',len(set(wissel)),'| losse seloutpixels tussen zwart (om en om):',sorted(om))
