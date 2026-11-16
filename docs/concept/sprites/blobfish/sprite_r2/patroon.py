# patroon.py X0 X1 Y0 Y1: natieve modelpixels per spritepixel (# donker <62, o 105-169, W >=170, . rest)
import sys,numpy as np; from PIL import Image
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]; bg=n.min(2)>=215
X0,X1,Y0,Y1=map(int,sys.argv[1:5])
ny0=OY+4*(Y0-y0+ymin); nx0=OX+4*(X0-x0+xmin)
print('    '+''.join('%-5d'%x for x in range(X0,X1)))
for yy in range(ny0,ny0+4*(Y1-Y0)):
    if (yy-ny0)%4==0: print('   '+'+'.join(['----']*(X1-X0)), Y0+(yy-ny0)//4)
    row=''
    for xx in range(nx0,nx0+4*(X1-X0)):
        if (xx-nx0)%4==0: row+='|'
        l=L[yy,xx]; row+= ' ' if bg[yy,xx] else ('#' if l<62 else ('o' if 105<=l<170 else ('W' if l>=170 else '.')))
    print('   '+row)
