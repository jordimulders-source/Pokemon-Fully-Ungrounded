# Per spritecel op het 1024-model: % zwart (L<28) / % donkerbruin (28<=L<54), zelfde mapping als vergelijk.py
import sys,numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
M=np.asarray(Image.open(D+'../referenties/model.png').convert('RGB')).astype(float); L=(M*[.299,.587,.114]).sum(2)
o=np.load(D+'r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def tm(sx,sy): return (NX0+(sx-fx+ox0)*s)*10.24-1.0,(NY0+(sy-top+oy0)*s)*10.24-1.0
def m(sx,sy):
    x0,y0=tm(sx,sy); x1,y1=tm(sx+1,sy+1); c=L[int(round(y0)):int(round(y1)),int(round(x0)):int(round(x1))]
    return (c<28).mean(),((c>=28)&(c<54)).mean()
if __name__=='__main__':
    X0,Y0,X1,Y1=map(int,sys.argv[1:5]); r=np.asarray(Image.open(D+'r9/mate.png'))
    print('    '+' '.join('%5d'%x for x in range(X0,X1+1)))
    for y in range(Y0,Y1+1):
        print('%2d  '%y+' '.join('%2d/%2d'%tuple(round(99*v) for v in m(x,y)) for x in range(X0,X1+1)),'  '+''.join('.#abcdGHIstu'[v] for v in r[y,X0:X1+1]))
