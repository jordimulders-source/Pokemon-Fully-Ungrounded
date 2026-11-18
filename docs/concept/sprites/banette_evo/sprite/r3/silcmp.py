# silhouet: model (niet-wit dekking) vs sprite: python3 silcmp.py npy x0 y0 x1 y1  ('#' beide, '+' alleen model, '-' alleen sprite)
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); fg=(a.min(2)<235)
S=968/62; g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]
print('    '+''.join('%x'%(i%16) for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        xa,ya=24+(i-1)*S,1+(j-4)*S; c=fg[max(0,int(round(ya))):int(round(ya+S)),max(0,int(round(xa))):int(round(xa+S))].mean()
        m=c>=0.5; sp=g[j,i]>0
        s+='#' if m and sp else ('+' if m else ('-' if sp else ' '))
    print('%3d '%j+s)
