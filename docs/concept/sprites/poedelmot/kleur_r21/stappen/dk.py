import sys,numpy as np
from PIL import Image
P='/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/'
x0,y0=139,150; s=(854-139)/62; top,left=17,1
c=np.asarray(Image.open(P+'referenties/samengesteld.png').convert('RGB')).astype(float)
lum=c.mean(2); g=(c[...,1]>c[...,0]+15)  # groen = achtergrond
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); th=int(sys.argv[5]); R=[l.rstrip('\n') for l in open(sys.argv[6])]
print('    '+''.join(str(x%10) for x in range(X0,X1))+'   '+''.join(str(x%10) for x in range(X0,X1))+'   lum/25')
for y in range(Y0,Y1):
    a='';b=''
    for x in range(X0,X1):
        bx=x0+(x-left)*s; by=y0+(y-top)*s
        sl=(slice(int(by),int(by+s)),slice(int(bx),int(bx+s)))
        L=lum[sl]; G=g[sl]; fg=~G
        if R[y][x]=='.': a+='.'; b+='.'; continue
        d=((L<th)&fg).sum()/max(1,fg.sum())
        a+=str(min(9,int(d*10)))
        mu=L[fg&(L>=th)].mean() if (fg&(L>=th)).any() else 0
        b+= '-' if mu==0 else str(min(9,int(mu/25)))
    print(f'{y:>3} '+a+'   '+R[y][X0:X1]+'   '+b)
