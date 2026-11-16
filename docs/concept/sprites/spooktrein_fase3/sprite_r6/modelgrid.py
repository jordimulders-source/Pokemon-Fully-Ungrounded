# Model per spritepixel (vlakgemiddelde uit model.webp, mapping uit sprite_r4/vel.py) -> dichtstbijzijnde r4-paletkleur.
import sys; from PIL import Image; import numpy as np
m=np.array(Image.open('model/model.webp').convert('RGB')).astype(float)
K=13.77; BX,BY,OY=102,71,2
pal=np.array(Image.open('sprite_r4/sprite.png').getpalette()[:13*3]).reshape(13,3).astype(float)
x0,x1,y0,y1=[int(v) for v in sys.argv[1:5]]
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for sy in range(y0,y1):
    s=''
    for sx in range(x0,x1):
        a=m[int(BY+(sy-OY)*K)+2:int(BY+(sy-OY+1)*K)-2, int(BX+sx*K)+2:int(BX+(sx+1)*K)-2].reshape(-1,3).mean(0)
        if a.min()>225: s+='.'; continue
        k=int(np.argmin(((pal[1:]-a)**2).sum(1)))+1; s+='%X'%k
    print('%2d '%sy+s)
