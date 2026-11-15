# Voorhoofd: per spritepixel de klasse van het model (orig = 99,3+16,9(x-7) / 191,5+16,9(y-18)), kernmonster (midden 60%).
import numpy as np
from PIL import Image
m=np.asarray(Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')).astype(int)
r,g,b=m[...,0],m[...,1],m[...,2]; L=0.299*r+0.587*g+0.114*b
lila=(b>g+10)&(r-b<30)&(L>95)
lilad=(b>g+5)&(r-b<30)&(L<=95)&(L>55)
k=16.896
def cel(x,y,f=0.6):
    cx,cy=99.3+(x-7+.5)*k,191.5+(y-18+.5)*k; h=k*f/2
    s=(slice(int(cy-h),int(cy+h)),slice(int(cx-h),int(cx+h)))
    return lila[s].mean(),lilad[s].mean(),L[s].mean()
if __name__=='__main__':
    a=np.array(Image.open('../p5/welp_p5.png'))
    print('   '+''.join(str(x%10) for x in range(8,28)))
    for y in range(17,29):
        s=''
        for x in range(8,28):
            l,d,lum=cel(x,y)
            s+= 'L' if l>.5 else 'l' if l>.25 else 'D' if d>.3 or lum<70 else '.'
        print('%2d '%y+s+'   '+''.join(' ' if a[y,x]==0 else '%x'%a[y,x] for x in range(8,28)))
