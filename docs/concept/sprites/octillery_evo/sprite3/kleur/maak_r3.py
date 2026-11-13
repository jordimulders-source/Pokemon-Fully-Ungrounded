# r3 = r2 + de reparatielijst uit KEURING_tentakels.md (alleen benoemde pixels). Gebruik: python3 maak_r3.py
from PIL import Image; import numpy as np
im=Image.open('r2.png'); a=np.array(im); pal=im.getpalette(); b=a.copy()
def zet(px,v):
    for x,y in px:
        assert a[y,x]!=0,(x,y); b[y,x]=v
zet([(13,44)],1)                                   # 1 haaktentakel achter de kanonarm
zet([(48,46),(47,47),(46,48)],1)                   # 2 voet rechter kanonarm voor de lage tentakel
zet([(52,45)],1); zet([(53,37)],1)                 # 3, 4 open lijnpixels
zet([(x,46) for x in range(7,11)]+[(x,48) for x in range(10,13)],5)   # 5 lage tentakel links een massa
R=[(x,53) for x in range(51,55)]+[(x,54) for x in range(46,52)]+[(x,55) for x in range(44,47)]+[(43,54),(42,53)]
R+=[(41,54),(40,55),(40,56),(41,57),(42,56)]       # 6 krul rechterrol
L=[(24,52),(25,53),(26,54),(27,54),(23,52),(22,53),(21,54),(21,55),(22,56),(23,55)]   # 7 krul linkerrol
zet(R+L,1)                                         # 8 middenlijn + krul zwart
zet([(36,59),(37,60)],4)                           # 9 stompje weg
o=Image.fromarray(b,'P'); o.putpalette(pal); o.save('r3.png',transparency=0)
c=b.copy(); assert c[36,24]==12; c[36,24]=1
o=Image.fromarray(c,'P'); o.putpalette(pal); o.save('r3_pupil2.png',transparency=0)
print('gewijzigd t.o.v. r2:',int((a!=b).sum()),'px; silhouet-diff',int(((a>0)!=(b>0)).sum()))
