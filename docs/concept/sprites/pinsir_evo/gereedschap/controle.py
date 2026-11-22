# controle.py SPRITE.png: Gen 3-eisen meten (kleuren, tintvlekjes < 3 px, lichte kleur op de buitenrand, losse zwarte pixels, zwart-%,
# selout/zwart om en om, aantal tinten per materiaal)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(set(o.ravel())),sorted(set(o.ravel())))
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
print('zwart %.1f%% van de figuur'%(100*(o==1).sum()/fg.sum()))
for nm,g in (('lijf',LIJF),('kaak',KAAK),('schild',SCHILD)): print('  %s tinten:'%nm,sorted(k for k in g if (o==k).any()),[(k,int((o==k).sum())) for k in sorted(g)])
tot=0
for k in range(2,14):
    lab,n=label(o==k,False); pts=[tuple(np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    tot+=len(pts)
    if pts: print('  tint %s (%d): %d vlekjes <3 px op %s'%(CH[k],k,len(pts),pts))
print('totaal tintvlekjes <3 px:',tot)
P=np.pad(o,1); F=P>0
rand=[(X,Y,CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in (4,5,7,8,10,11,12,13) and not all(F[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))]
print('lichte kleur op de buitenrand:',rand)
lab,n=label(o==1,True)
los=[tuple(np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<=2 and not any(P[Y+1+dy,X+1+dx]==0 for Y,X in np.argwhere(lab==i) for dy in (-1,0,1) for dx in (-1,0,1))]
print('losse zwarte pixels/paartjes (niet aan de rand):',los)
