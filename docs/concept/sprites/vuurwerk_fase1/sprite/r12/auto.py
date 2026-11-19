# Voorstel per spritepixel uit het natieve raster: lijn (lum<75) / huls-of-kop (beige) / huid (licht/mid/schaduw op lum)
import numpy as np; from PIL import Image; import sys
sys.path.insert(0,'../r10'); from txt import CH
n=np.asarray(Image.open('../r10/natief.png').convert('RGB')).astype(int)
R,G,B=n[...,0],n[...,1],n[...,2]; lum=.3*R+.59*G+.11*B
bg=n.min(2)>=236; line=(lum<75)&~bg; beige=(G>=0.68*R)&(B<=G+12)&~line&~bg
F,OX,OY=2.4,76.6,14.6
def stats(r,c):
    j,i=r-1,c-17; x0,x1=OX+i*F,OX+(i+1)*F; y0,y1=OY+j*F,OY+(j+1)*F
    w=np.zeros(4); L=0; Lw=0
    for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
        wy=min(y1,yy+1)-max(y0,yy)
        for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
            wx=min(x1,xx+1)-max(x0,xx); a=wx*wy
            if a<=0: continue
            k=0 if bg[yy,xx] else 1 if line[yy,xx] else 2 if beige[yy,xx] else 3
            w[k]+=a
            if k==3: L+=lum[yy,xx]*a; Lw+=a
    return w/w.sum(), (L/Lw if Lw else 0)
a=np.array(Image.open('../r11/sprite.png'))
r0,r1,c0,c1=map(int,sys.argv[1:5])
print('     '+''.join(str(c%10) for c in range(c0,c1)))
for r in range(r0,r1):
    s=''; t=''
    for c in range(c0,c1):
        w,L=stats(r,c)
        if w[1]>=0.35: ch='#'
        elif w[0]>=0.5: ch='.'
        elif w[2]>=0.5: ch='k'
        else: ch='l' if L>=165 else 'm' if L>=125 else 's'
        s+=ch
    print('%3d  '%r+s+'   r11 '+''.join(CH[v] for v in a[r,c0:c1]))
