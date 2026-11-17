# Natief model met het spritepixel-rooster erover (elke spritecel 1,75 natief) + de sprite zelf ernaast, voor reparatie per pixel.
# Gebruik: python3 rooster.py sprite.png uit.png x0 y0 x1 y1
import sys, numpy as np; from PIL import Image, ImageDraw
sp,out=sys.argv[1],sys.argv[2]; X0,Y0,X1,Y1=map(int,sys.argv[3:7]); S=24
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
N=np.asarray(Image.open('natief.png').convert('RGB'))
w,h=X1-X0,Y1-Y0; v=Image.new('RGB',(2*w*S+12,h*S+14),'white'); d=ImageDraw.Draw(v)
k=S/s
for j in range(h):
    for i in range(w):
        # model: natief pixels in de cel
        pass
ny0=NY0+(Y0-top+oy0)*s; nx0=NX0+(X0-fx+ox0)*s
for yy_ in range(int(ny0)-1,int(ny0+h*s)+2):
    for xx_ in range(int(nx0)-1,int(nx0+w*s)+2):
        if not(0<=yy_<100 and 0<=xx_<100): continue
        px=(xx_-nx0)*k; py=(yy_-ny0)*k
        d.rectangle([w*S+12+px,14+py,w*S+12+px+k,14+py+k],fill=tuple(int(c) for c in N[yy_,xx_]))
d.rectangle([w*S+12+w*S,0,2*w*S+12,h*S+14],fill='white'); d.rectangle([0,0,2*w*S+12,13],fill='white')
im=Image.open(sp); p=im.getpalette(); a=np.asarray(im)
for j in range(h):
    for i in range(w):
        kk=a[Y0+j,X0+i]; col=(255,255,255) if kk==0 else tuple(p[3*kk:3*kk+3])
        d.rectangle([i*S,14+j*S,i*S+S-1,14+j*S+S-1],fill=col)
for i in range(w+1):
    c=(255,0,0) if (X0+i)%5==0 else (120,160,255)
    d.line([i*S,14,i*S,14+h*S],fill=c); d.line([w*S+12+i*S,14,w*S+12+i*S,14+h*S],fill=c)
    if (X0+i)%5==0: d.text((i*S+2,1),str(X0+i),fill='red'); d.text((w*S+14+i*S,1),str(X0+i),fill='red')
for j in range(h+1):
    c=(255,0,0) if (Y0+j)%5==0 else (120,160,255)
    d.line([0,14+j*S,w*S,14+j*S],fill=c); d.line([w*S+12,14+j*S,2*w*S+12,14+j*S],fill=c)
    if (Y0+j)%5==0: d.text((2,15+j*S),str(Y0+j),fill='red')
v.save(out)
