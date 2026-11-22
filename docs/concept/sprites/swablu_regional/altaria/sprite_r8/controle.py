# controle.py: Gen 3-controles voor r8. python3 sprite_r8/controle.py [png]
import sys, numpy as np; sys.path.insert(0,'gereedschap')
from PIL import Image; from gemeen import label
p=sys.argv[1] if len(sys.argv)>1 else 'sprite_r8/altaria_r8.png'
im=Image.open(p); o=np.array(im); pal=im.getpalette()
pr=np.array(Image.open('sprite_r5/proef_eindkeuring.png'))
gebruikt=sorted(set(o.ravel())); print('kleuren incl. transparant:',len(gebruikt), '(index 0 transparant:',0 in gebruikt,')')
print('alpha-diff met r5-proef:',int(((o>0)!=(pr>0)).sum()))
print('pupil/zwart (index 1) px:',int((o==1).sum()), 'posities',[(int(x),int(y)) for y,x in zip(*np.where(o==1))])
fig=o>0; N4=((-1,0),(1,0),(0,-1),(0,1))
rand=np.zeros_like(fig)
for Y,X in zip(*np.where(fig)): rand[Y,X]=any(not fig[Y+dy,X+dx] for dy,dx in N4)
Lm={k:.299*pal[3*k]+.587*pal[3*k+1]+.114*pal[3*k+2] for k in gebruikt}
licht=[(int(X),int(Y),int(o[Y,X])) for Y,X in zip(*np.where(rand)) if Lm[o[Y,X]]>=150]
print('lichte pixels (L>=150) op de buitenrand:',len(licht),licht)
los=[]
for k in gebruikt:
    if k==0: continue
    lab,n=label(o==k,acht=True)
    for i in range(1,n+1):
        if (lab==i).sum()==1: Y,X=np.argwhere(lab==i)[0]; los.append((int(X),int(Y),int(k)))
print('pixels zonder 8-buur van dezelfde tint:',len(los),los)
