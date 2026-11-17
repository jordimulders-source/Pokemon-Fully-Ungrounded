# per spritepixel modelkleur (gemiddelde) als RGB-hex en klasse. python3 mpx.py x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); S=968/62
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
def blk(i,j):
    xa,ya=24+(i-1)*S,1+(j-4)*S; b=a[max(0,int(round(ya))):int(round(ya+S)),max(0,int(round(xa))):int(round(xa+S))].reshape(-1,3); return b
print('    '+''.join('%12d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        b=blk(i,j); m=b.mean(0); L=b.sum(1)/3; k=(L<45).mean()
        s+=' %3d,%3d,%3d%s'%(m[0],m[1],m[2],'K' if k>.45 else ('k' if k>.25 else ' '))
    print('%3d '%j+s)
