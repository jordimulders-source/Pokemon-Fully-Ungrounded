# Spriteraster (rode lijnen, coordinaten) over het natieve r7-model, naast de sprite op dezelfde schaal. Uitsnede in spritepx.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
sp,out,x0,y0,x1,y1=sys.argv[1],sys.argv[2],*[int(v) for v in sys.argv[3:7]]; F=int(sys.argv[7]) if len(sys.argv)>7 else 24
n=Image.open('natief_r7.png').convert('RGB')
# natief -> pixels: natieve px op F*S schermpx
fx=F*S
u0=NX0+(x0-OX)/S; v0=NY0+(y0-OY)/S
W=(x1-x0)*F; H=(y1-y0)*F
mm=Image.new('RGB',(W,H),'white'); na=np.asarray(n)
for j in range(H):
    pass
yy,xx=np.mgrid[0:H,0:W]; uu=np.floor(u0+xx/fx).astype(int); vv=np.floor(v0+yy/fx).astype(int)
ok=(uu>=0)&(vv>=0)&(uu<na.shape[1])&(vv<na.shape[0]); arr=np.full((H,W,3),255,'uint8'); arr[ok]=na[vv[ok],uu[ok]]
mm=Image.fromarray(arr); d=ImageDraw.Draw(mm)
im=Image.open(sp); o=np.array(im); a=rgb(o,(248,248,248))[y0:y1,x0:x1]
si=Image.fromarray(a).resize((W,H),Image.NEAREST); d2=ImageDraw.Draw(si)
for dd in (d,d2):
    for X in range(x0,x1+1): dd.line([((X-x0)*F,0),((X-x0)*F,H)],fill=(255,0,0) if X%5==0 else (255,170,170))
    for Y in range(y0,y1+1): dd.line([(0,(Y-y0)*F),(W,(Y-y0)*F)],fill=(255,0,0) if Y%5==0 else (255,170,170))
    for X in range(x0,x1):
        if X%5==0: dd.text(((X-x0)*F+2,2),str(X),fill=(0,0,255))
    for Y in range(y0,y1):
        if Y%5==0: dd.text((2,(Y-y0)*F+2),str(Y),fill=(0,0,255))
v=Image.new('RGB',(W*2+12,H),'white'); v.paste(si,(0,0)); v.paste(mm,(W+12,0)); v.save(out)
