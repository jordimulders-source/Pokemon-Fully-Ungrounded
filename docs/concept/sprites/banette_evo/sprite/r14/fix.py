# r14 = r13 + reparaties 1-4 en o2 van keuring r13 (per pixel, Claude).
from PIL import Image; import numpy as np
im=Image.open('../r13/banette_evo.png'); a=np.array(im); pal=im.getpalette()
S=[((53,19),3),((53,20),3),((52,18),2),((51,21),1),                 # 1 rechterbel
   ((7,36),1),((8,37),3),((7,37),3),((9,35),3),((9,36),3),          # 2 linkerbel
   ((48,17),0),((49,17),1),                                         # 3 uitsteeksel/gaatje
   ((17,35),3)]                                                     # o2 scherpere tandpunt
S+=[((x,48),1) for x in range(25,30)]+[((25,49),0)]+[((x,49),0) for x in range(26,30)]   # 4 rokflap smaller naar links
log=[]
for (x,y),v in S:
    log.append((x,y,int(a[y,x]),v)); a[y,x]=v
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
for l in log: print(l)
