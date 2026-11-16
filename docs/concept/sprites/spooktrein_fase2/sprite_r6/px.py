# Modelhelderheid per spritepixel uit het natieve raster (gem/p15/min) + spriteindex. Gebruik: px.py x0 y0 x1 y1 [gem|p15|min] [sprite]
import sys, numpy as np; from PIL import Image
s,X0,Y0,oy,XC,k=[float(v) for v in open('../sprite_r2/sprite.meta').read().split()]
a=np.asarray(Image.open('../sprite_r5/natief.png').convert('RGB')).astype(float); L=a@[0.3,0.59,0.11]
def nx_of(mx): return mx if mx<XC else XC+(mx-XC)/k
def stats(sx,sy):
    ya,yb=Y0+(sy-oy)/s, Y0+(sy+1-oy)/s; xa,xb=nx_of(X0+sx/s), nx_of(X0+(sx+1)/s)
    ys=range(int(np.floor(ya)),int(np.ceil(yb))); xs=range(int(np.floor(xa)),int(np.ceil(xb)))
    v=np.array([L[y,x] for y in ys for x in xs if 0<=y<199 and 0<=x<199])
    return v.mean(), np.percentile(v,15), v.min()
M=np.zeros((3,64,64))
for sy in range(64):
    for sx in range(64): M[:,sy,sx]=stats(sx,sy)
np.save('modelstats.npy',M)
if len(sys.argv)>4:
    x0,y0,x1,y1=map(int,sys.argv[1:5]); w={'gem':0,'p15':1,'min':2}[sys.argv[5] if len(sys.argv)>5 else 'gem']
    o=np.asarray(Image.open(sys.argv[6] if len(sys.argv)>6 else 'sprite.png')).astype(int); ch='.#23456789abcd'
    print('    '+''.join('%4d'%x for x in range(x0,x1+1)))
    for y in range(y0,y1+1): print('%3d '%y+''.join('%3d%s'%(min(M[w,y,x],999),ch[o[y,x]]) for x in range(x0,x1+1)))
