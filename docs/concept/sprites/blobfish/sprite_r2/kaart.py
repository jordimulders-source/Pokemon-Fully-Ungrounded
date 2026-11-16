# kaart.py x0 y0 x1 y1 : per spritepixel de modelinhoud van zijn 4x4-blok (16 natieve px):
#   aantal donker (<62) / licht (helderheid>=105: lip, glans, vinstraal) / max helderheid  + r1-index
import sys,numpy as np; from PIL import Image
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]
s=np.asarray(Image.open(sys.argv[5] if len(sys.argv)>5 else 'r1.png'))
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
def blk(x,y):
    ny=OY+4*(y-y0+ymin); nx=OX+4*(x-x0+xmin); return L[ny:ny+4,nx:nx+4]
print('    '+''.join('%9d'%x for x in range(X0,X1)))
for y in range(Y0,Y1):
    print('%3d '%y+''.join(('   %2d/%2d%x'%((blk(x,y)<62).sum(),(blk(x,y)>=105).sum(),s[y,x])) if s[y,x] else '        .' for x in range(X0,X1)))
