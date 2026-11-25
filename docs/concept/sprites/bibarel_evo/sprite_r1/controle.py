# controle.py SPRITE.png : Gen 3-eisen meten (kleuren, tinten per groep, vlekjes <3 px, lichte buitenrand, losse zwarte pixels)
import sys,numpy as np; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
o=laad(sys.argv[1]); fg=o>0; yy,xx=np.where(fg)
print('kleuren excl. transparant',len(set(o.ravel()))-1,'| bbox x%d-%d y%d-%d | %d px | zwart %.1f%%'%(xx.min(),xx.max(),yy.min(),yy.max(),fg.sum(),100*(o==1).sum()/fg.sum()))
G={'bruin':(2,3,4,5),'creme':(15,6,7),'donker':(8,9,10),'oranje':(11,12),'wit':(13,14)}
for g,ks in G.items(): print('  %s: %s'%(g,[(NAAM[k],int((o==k).sum())) for k in ks if (o==k).any()]))
vl=[]
for k in range(2,16):
    lab,n=ndimage.label(o==k,structure=np.ones((3,3)) if k in (2,8,12,15,14) else None)
    for i in range(1,n+1):
        p=np.argwhere(lab==i)
        if len(p)<3: vl.append((NAAM[k],tuple(p[0][::-1]),len(p)))
print('vlekjes <3 px:',len(vl)); [print('   ',v) for v in vl]
P=np.pad(o,1)
rand=[(x,y,NAAM[o[y,x]]) for y,x in zip(yy,xx) if o[y,x] in (5,6,7,13,14,10) and any(P[y+1+dy,x+1+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))]
print('lichte kleur op de buitenrand:',rand)
los=[(x,y) for y,x in zip(*np.where(o==1)) if sum(P[y+1+dy,x+1+dx] in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)==0]
print('losse zwarte pixels:',los)
