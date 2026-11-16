# Meet per spritepixel het aandeel donkere modelpixels (lum<drempel) in zijn 12x12-blok; print raster naast de sprite.
import sys, numpy as np; from PIL import Image
a=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float); lum=a@[0.299,0.587,0.114]
sp=np.asarray(Image.open(sys.argv[1])); x0,y0,x1,y1=map(int,sys.argv[2:6]); T=float(sys.argv[6]) if len(sys.argv)>6 else 130
print('    '+''.join('%d'%(x%10) for x in range(x0,x1)),'   ',''.join('%d'%(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    r=''
    for x in range(x0,x1):
        b=lum[120+y*12:132+y*12,106+x*12:118+x*12]; f=(b<T).mean()
        r+=' ' if f<0.08 else ('.' if f<0.2 else ('o' if f<0.35 else '#'))
    print('%2d  '%y+r,'   ',''.join('.123456789ABCDEF'[v] for v in sp[y,x0:x1]))
