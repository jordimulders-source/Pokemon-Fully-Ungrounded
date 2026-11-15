# Per spritecel: aandeel lila (L/l) en creme (C/c) in het originele model (16.9 modelpx per spritepx).
import numpy as np
from PIL import Image
m=np.asarray(Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')).astype(int)
r,g,b=m[...,0],m[...,1],m[...,2]; L=0.299*r+0.587*g+0.114*b
lila=(b>g+12)&(r-b<25)&(L>95)
creme=(g>180)&(r>195)&(r-b>20)&(L<245)
k=16.896
def cel(x,y):
    x0,x1=int(99.3+(x-7)*k),int(99.3+(x-6)*k); y0,y1=int(191.5+(y-18)*k),int(191.5+(y-17)*k)
    return lila[y0:y1,x0:x1].mean(), creme[y0:y1,x0:x1].mean()
if __name__=='__main__':
    a=np.array(Image.open('../r11/welp_r11.png'))
    out=np.zeros((64,64),'U1')
    for y in range(17,63):
        s=''
        for x in range(5,60):
            if a[y,x]==0: s+=' '; continue
            l,c=cel(x,y)
            s+= 'L' if l>.45 else 'C' if c>.45 else 'l' if l>.2 else 'c' if c>.2 else '.'
        print('%2d '%y+s)
