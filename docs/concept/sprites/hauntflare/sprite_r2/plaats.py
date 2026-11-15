# Zoekt de plek van het Haunter-blok op r1: alle gezichtspixels op de bol (r1-boltint of r1-gezicht),
# >=1 px bol tussen gezicht en ring/omlijning, >=2 px bolroze links van het linker oog; dichtst bij het modelgezicht.
from PIL import Image; import numpy as np
from scipy import ndimage as nd
R1='docs/concept/sprites/hauntflare/sprite_r1/'; S='docs/concept/sprites/hauntflare/sprite_r2/'
o=np.array(Image.open(R1+'hauntflare_r1.png')).astype(int); gz1=np.load(R1+'gezicht_masker.npy')
yy,xx=np.mgrid[:64,:64]; ell=((xx-28)/18.5)**2+((yy-32.5)/17)**2<=1
bol=ell&(np.isin(o,[5,6,7,8,9])|gz1)
# rand-selout van de bol (5/6 tegen transparant of omlijning) telt niet als binnenkant
binnen=bol&~nd.binary_dilation(~bol,np.ones((3,3)))
C=np.load(S+'gezicht_r2.npy'); cy,cx=np.where(C>0)
oog_l=[(y,x) for y,x in zip(cy,cx) if C[y,x]==3 and x<=4]   # linker oog (Haunter x<=16)
res=[]
for Y in range(5,40):
    for X in range(5,40):
        py,px=cy+Y,cx+X
        if py.max()>63 or px.max()>63: continue
        if not binnen[py,px].all(): continue
        ok=True
        for y,x in oog_l:
            if not (bol[y+Y,x+X-1] and bol[y+Y,x+X-2]): ok=False
        if not ok: continue
        res.append((abs(X-(14-1))+abs(Y-(24-1)),X,Y))
res.sort(); print('mogelijk:',len(res),res[:10])
