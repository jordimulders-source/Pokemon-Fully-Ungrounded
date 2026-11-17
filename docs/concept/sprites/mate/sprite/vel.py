# vel.png: sprite 8x | model verkleind naar hetzelfde formaat (zelfde plaatsing) | 1x op licht en donker
import sys, numpy as np; from PIL import Image, ImageDraw
sp,out=sys.argv[1],sys.argv[2]; extra=sys.argv[3:]   # extra: eerdere rondes
def rgba(f):
    im=Image.open(f); a=np.asarray(im); p=np.array(im.getpalette()[:768]).reshape(-1,3)
    r=np.zeros((64,64,4),'uint8'); r[...,:3]=p[a]; r[...,3]=(a>0)*255; return Image.fromarray(r)
def op(img,bg):
    b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
S=8; o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
# canvas (0,0) en (64,64) -> modelcoördinaten
def tm(sx,sy): return ((NX0+(sx-fx+ox0)*s)*10.24-1.0,(NY0+(sy-top+oy0)*s)*10.24-1.0)
M=Image.open('../referenties/model.png').convert('RGB'); (a0,b0),(a1,b1)=tm(0,0),tm(64,64)
big=Image.new('RGB',(3000,3000),'white'); big.paste(M,(1000,1000))
mod=big.crop((int(a0)+1000,int(b0)+1000,int(a1)+1000,int(b1)+1000)).resize((64*S,64*S),Image.LANCZOS)
fs=[sp]+extra; W=(len(fs)+1)*(64*S+10)+140; v=Image.new('RGB',(W,64*S+30),(235,235,235)); d=ImageDraw.Draw(v)
for k,f in enumerate(fs):
    v.paste(op(rgba(f),(255,255,255,255)).resize((64*S,64*S),Image.NEAREST),(k*(64*S+10),24)); d.text((k*(64*S+10)+4,6),f,fill='black')
x=len(fs)*(64*S+10); v.paste(mod,(x,24)); d.text((x+4,6),'model (zelfde schaal)',fill='black')
x+=64*S+10; R=rgba(sp)
v.paste(op(R,(255,255,255,255)),(x,24)); v.paste(op(R,(40,40,48,255)),(x,24+70))
v.paste(op(R,(255,255,255,255)).resize((128,128),Image.NEAREST),(x,24+150)); v.paste(op(R,(40,40,48,255)).resize((128,128),Image.NEAREST),(x,24+290))
d.text((x,10),'1x / 2x',fill='black'); v.save(out)
