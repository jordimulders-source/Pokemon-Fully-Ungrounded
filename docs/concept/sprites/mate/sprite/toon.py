# Per spritepixel de modelkleuren (natief) in de cel, als letters van het palet (dichtstbijzijnde). Gebruik: toon.py x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
P=np.array(Image.open('r1/kaal.png').getpalette()[:36]).reshape(-1,3); P[0]=(255,255,255); ch='.#abcdGHIstu'
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
for sy in range(Y0,Y1+1):
    row=[]
    for sx in range(X0,X1+1):
        ly=NY0+(sy-top+oy0)*s; lx=NX0+(sx-fx+ox0)*s
        cs=''.join(ch[((P-a[y,x])**2).sum(1).argmin()] for y in range(int(ly),int(np.ceil(ly+s))) for x in range(int(lx),int(np.ceil(lx+s))))
        row.append('%d:%s'%(sx,cs))
    print(sy,' '.join(row))
