# Per spritepixel: dichtstbijzijnde paletkleur van modelgemiddelde (A), donkerste 25% (D) en zwartfractie (Z, 0-9). Gebruik: meet.py MODEL x0 y0 x1 y1
import sys,numpy as np; from PIL import Image; sys.path.insert(0,'.'); from box import win; from tekstraster import CH
pal=np.array(Image.open('../sprite_r4/pitahaya3_r4.png').getpalette()[:48]).reshape(16,3).astype(float)
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1=map(int,sys.argv[2:6])
def nb(c):
    if c.min()>245: return '.'
    return CH[1+np.argmin(((pal[1:]-c)**2).sum(1))]
print('    '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1)))
for Y in range(y0,y1):
    A='';D='';Z=''
    for X in range(x0,x1):
        b=win(M,X,Y); l=b@[.299,.587,.114]; o=np.argsort(l)
        A+=nb(b.mean(0)); D+=nb(b[o[:max(1,len(o)//4)]].mean(0)); Z+=str(min(9,int(10*(l<45).mean())))
    print('%3d %s   %s   %s'%(Y,A,D,Z))
