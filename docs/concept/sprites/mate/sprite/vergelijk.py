# Zone van de sprite (canvascoords) op S x naast hetzelfde stuk van het 1024-model op dezelfde schaal.
# Gebruik: python3 vergelijk.py sprite.png uit.png x0 y0 x1 y1 [S]
import sys, numpy as np; from PIL import Image, ImageDraw
sp,out=sys.argv[1],sys.argv[2]; X0,Y0,X1,Y1=map(int,sys.argv[3:7]); S=int(sys.argv[7]) if len(sys.argv)>7 else 16
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def tomodel(sx,sy):
    ny=NY0+(sy-top+oy0)*s; nx=NX0+(sx-fx+ox0)*s; return nx*10.24-1.0, ny*10.24-1.0
im=Image.open(sp); p=im.getpalette(); a=np.asarray(im)
w,h=X1-X0,Y1-Y0
v=Image.new('RGB',(2*w*S+10,h*S),'white'); d=ImageDraw.Draw(v)
for j in range(h):
    for i in range(w):
        k=a[Y0+j,X0+i]; col=(255,255,255) if k==0 else tuple(p[3*k:3*k+3])
        d.rectangle([i*S,j*S,i*S+S-1,j*S+S-1],fill=col)
M=Image.open('../referenties/model.png').convert('RGB')
mx0,my0=tomodel(X0,Y0); mx1,my1=tomodel(X1,Y1)
v.paste(M.crop((int(mx0),int(my0),int(mx1),int(my1))).resize((w*S,h*S),Image.LANCZOS),(w*S+10,0))
for i in range(w+1):
    if (X0+i)%5: continue
    for xo in (0,w*S+10): d.line([xo+i*S,0,xo+i*S,h*S],fill=(255,0,0))
for j in range(h+1):
    if (Y0+j)%5: continue
    c=(255,0,0)
    d.line([0,j*S,w*S,j*S],fill=c); d.line([w*S+10,j*S,2*w*S+10,j*S],fill=c)
v.save(out)
