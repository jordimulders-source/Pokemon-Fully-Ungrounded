# vel.png: r1 | vorige (af/picapau.png) | model verkleind, 8x; kop 12x naast model; 1x licht/donker
import sys; import numpy as np; from PIL import Image, ImageDraw
def rgba(f):
    im=Image.open(f); im.save('/tmp/_t.png' if False else f) ; return Image.open(f).convert('RGBA')
cur=Image.open('picapau.png').convert('RGBA'); prev=Image.open(sys.argv[1] if len(sys.argv)>1 else '../../af/picapau.png').convert('RGBA')
# model 1x op dezelfde plek als de sprite: zelfde verschuiving als bouw.py
o=np.load('r4.npy'); ys,xs=np.where(o>0); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1; dx=(64-w)//2-xs.min(); dy=63-h-ys.min()
m=np.asarray(Image.open('model_1x.png').convert('RGB')).copy(); m[(m.min(2)>=225)]=255; mod=Image.new('RGB',(64,64),(255,255,255))
mod.paste(Image.fromarray(m),(dx,dy))
mod=mod.convert('RGBA')
def on(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
W=3*512+40; H=512+40+ 16*12+40+80
V=Image.new('RGB',(W,H),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(cur,'r4'),(prev,'r3'),(mod,'model verkleind')]):
    V.paste(on(im,(255,255,255,255),8),(10+i*522,24)); d.text((10+i*522,6),t,fill=(0,0,0))
# kop close-up: sprite x 17..42, y 2..27 (r1.npy-coords) -> canvas coords
x0,y0,x1,y1=17+dx,2+dy,42+dx,27+dy
kc=on(cur.crop((x0,y0,x1,y1)),(255,255,255,255),12)
mi=Image.open('../../gemini/r5_verbeter.png').convert('RGB'); c=lambda s:4.13+(1+3*s)*5.12
km=mi.crop((int(c(17)),int(c(2)),int(c(42)),int(c(27)))).resize(kc.size,Image.LANCZOS)
yk=24+512+16; V.paste(kc,(10,yk)); V.paste(km,(20+kc.width,yk)); d.text((10,yk-14),'kop 12x  |  model',fill=(0,0,0))
x=40+2*kc.width
for bg in ((248,248,248,255),(40,40,48,255)):
    V.paste(on(cur,bg,1),(x,yk)); V.paste(on(cur,bg,2),(x+70,yk)); x+=210
V.save('vel.png'); print(V.size)
