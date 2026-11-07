import sys,numpy as np
from PIL import Image
P='/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/'
x0,y0=139,150; s=(854-139)/62; top,left=17,1
c=np.asarray(Image.open(P+'referenties/samengesteld.png').convert('RGB')).astype(float)
lum=c.mean(2)
def blk(x,y):
    bx=x0+(x-left)*s; by=y0+(y-top)*s
    return lum[int(by):int(by+s),int(bx):int(bx+s)]
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); mode=sys.argv[5] if len(sys.argv)>5 else 'mean'
R=[l.rstrip('\n') for l in open(sys.argv[6])] if len(sys.argv)>6 else None
print('    '+''.join(f"{x:>5}" for x in range(X0,X1)))
for y in range(Y0,Y1):
    row=f'{y:>3} '
    for x in range(X0,X1):
        b=blk(x,y)
        v={'mean':b.mean(),'min':b.min(),'dark':100*(b<100).mean()}[mode]
        ch=R[y][x] if R else ''
        row+=f'{int(v):>4}{ch}'
    print(row)
