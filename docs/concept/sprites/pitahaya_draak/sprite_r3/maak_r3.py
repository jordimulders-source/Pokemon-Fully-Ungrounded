# r3 = r2 + MOET-lijst keurder r2 (33 wissels, per pixel gemeten op het model) + KAN 1 (paletwaarde idx 3).
from PIL import Image
import numpy as np
im=Image.open('sprite_r2/pitahaya_r2.png'); a=np.array(im); pal=im.getpalette()
W=[(37,10,2,3),(36,15,2,3),(29,18,2,3),(35,19,2,3),(38,27,2,4),
(25,14,1,5),(31,14,1,2),(31,15,1,2),(30,13,1,8),
(25,39,1,8),(25,40,1,8),(33,39,1,8),(20,43,1,10),(17,45,1,11),(21,43,1,8),(21,44,1,8),(24,50,1,8),(25,51,1,8),
(23,49,1,8),(23,50,1,8),(20,52,1,8),(21,52,1,10),
(39,39,8,9),(38,40,8,9),
(38,28,1,2),(38,29,1,2),(38,30,1,2),(37,31,1,2),
(35,39,1,8),(35,40,1,8),(36,40,1,8),(37,40,1,8),(37,41,1,8)]
for x,y,o,n in W:
    assert a[y,x]==o,(x,y,a[y,x],o); a[y,x]=n
r,g,b=pal[9:12]; print('idx3 oud',(r,g,b),'lum',round(.299*r+.587*g+.114*b))
out=Image.fromarray(a,'P'); out.putpalette(pal); out.save('sprite_r3/pitahaya_r3_zonderpalet.png',transparency=0)
print(len(W),'wissels')
for i in range(12): r,g,b=pal[3*i:3*i+3]; print(i,(r,g,b),round(.299*r+.587*g+.114*b))
