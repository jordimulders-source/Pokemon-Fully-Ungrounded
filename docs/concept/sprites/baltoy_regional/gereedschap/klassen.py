# Natief raster -> klassen (dichtstbijzijnde modelkleur). 0=transparant, 1=zwart lijn, 2=donkerbruin lijn, 3=donker, 4=midden-donker,
# 5=midden, 6=licht, 7=hooglicht, 8=rood licht, 9=rood donker. Centra = k-means op het natieve model (gemeten, niet gekozen).
import numpy as np; from PIL import Image
C=np.array([[255,255,255],[20,17,28],[64,56,51],[100,90,78],[123,112,97],[142,131,113],[185,174,155],[200,192,172],[202,84,83],[170,48,53]])
def laad(pad='gereedschap/natief.png'):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int)[13:83,15:83]
    d=((a[:,:,None]-C[None,None])**2).sum(3); return d.argmin(2), a
if __name__=='__main__':
    k,_=laad(); s='.KDdmMlhRr'
    for y,r in enumerate(k): print('%2d '%y+''.join(s[v] for v in r))
