# Sprite op S x met de modelomtrek (rood) en de zwarte modellijnen (blauw, lum<40) erover. Gebruik: overlay.py sprite uit x0 y0 x1 y1
import sys,numpy as np; from PIL import Image, ImageDraw
sp,out=sys.argv[1],sys.argv[2]; X0,Y0,X1,Y1=map(int,sys.argv[3:7]); S=20
M=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(int); fg=M.min(2)<200; L=(M*[.299,.587,.114]).sum(2)
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
im=Image.open(sp); p=im.getpalette(); a=np.asarray(im); w,h=X1-X0,Y1-Y0
v=Image.new('RGB',(w*S,h*S),'white'); d=ImageDraw.Draw(v)
for j in range(h):
    for i in range(w):
        k=a[Y0+j,X0+i]; d.rectangle([i*S,j*S,i*S+S-1,j*S+S-1],fill=(255,255,255) if k==0 else tuple(p[3*k:3*k+3]))
v=np.asarray(v).copy()
for py in range(h*S):
    for px in range(w*S):
        sx=X0+px/S; sy=Y0+py/S
        mx=int((NX0+(sx-fx+ox0)*s)*10.24-1.0); my=int((NY0+(sy-top+oy0)*s)*10.24-1.0)
        if not(1<=mx<1023 and 1<=my<1023): continue
        if fg[my,mx]!=fg[my,mx+1] or fg[my,mx]!=fg[my+1,mx]: v[py,px]=(255,0,0)
        elif L[my,mx]<40 and (px+py)%3==0: v[py,px]=(0,150,255)
img=Image.fromarray(v); d=ImageDraw.Draw(img)
for i in range(w+1):
    if (X0+i)%5==0: d.line([i*S,0,i*S,h*S],fill=(0,200,0)); d.text((i*S+2,2),str(X0+i),fill=(0,160,0))
for j in range(h+1):
    if (Y0+j)%5==0: d.line([0,j*S,w*S,j*S],fill=(0,200,0)); d.text((2,j*S+2),str(Y0+j),fill=(0,160,0))
img.save(out)
