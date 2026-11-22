# controle.py: technische controle r3 (kleuren, alpha = basis, losse pixels/kleine clusters per tint, lichte kleur op de buitenrand, zwart).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import label
f=sys.argv[1] if len(sys.argv)>1 else 'sprite_r3/altaria_r3.png'
im=Image.open(f); o=np.asarray(im).astype(int); b=np.asarray(Image.open('sprite_r3/basis_kop15.png')).astype(int)
fig=o>0; print('modus',im.mode,'kleuren incl. transparant',len(np.unique(o)),'| alpha-diff met basis',int((fig!=(b>0)).sum()),'| figuur',int(fig.sum()))
NAAM=['tr','pupil','w-sel','w-donk','w-mid','w-licht','w-hoog','v-sel','v-donk','v-mid','v-licht','static','glans']
for k in range(1,13):
    lab,n=label(o==k,acht=False); kl=[(lab==i).sum() for i in range(1,n+1)]
    print('%-8s %4d px, %2d clusters, < 3 px: %d'%(NAAM[k],(o==k).sum(),n,sum(1 for s in kl if s<3)))
N4=((-1,0),(1,0),(0,-1),(0,1))
rand=[(X,Y,NAAM[o[Y,X]]) for Y,X in zip(*np.where(fig)) if any(o[Y+dy,X+dx]==0 for dy,dx in N4) and o[Y,X] in (5,6,10,12)]
print('lichte kleur op de buitenrand:',rand)
los=[(X,Y) for Y,X in zip(*np.where(fig)) if all(o[Y+dy,X+dx]!=o[Y,X] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('pixels zonder 8-buur van dezelfde tint:',len(los),los)
