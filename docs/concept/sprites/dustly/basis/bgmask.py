# Achtergrond = bijna-wit dat aan de rand vastzit + de twee witte gaten tussen de slierten rechtsonder (puur wit, 253).
# Oogwit en tanden (bijna-wit, ingesloten, ±230) blijven figuur.
import sys; sys.path.insert(0,'basis'); from lab import label; import numpy as np; from PIL import Image
def bgmask():
    a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(int)
    w=a.min(2)>=200; lab,n=label(w); bg=np.zeros(w.shape,bool)
    for i in range(1,n+1):
        m=lab==i; ys,xs=np.where(m)
        if (ys.min()==0 or xs.min()==0 or ys.max()==99 or xs.max()==99) or (a[m].mean()>=250 and m.sum()>=20): bg|=m   # tand (2 px, 252) blijft
    return bg
