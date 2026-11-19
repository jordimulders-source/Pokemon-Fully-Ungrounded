# vel.png: r1 | vorige (af/picapau_evo.png) | model verkleind, 8x; kop 12x naast het model; 1x en 2x op licht en donker
import sys; import numpy as np; from PIL import Image, ImageDraw
def rgba(f):
    im=Image.open(f)
    if im.mode=='P': im.save('_tmp.png',transparency=0); im=Image.open('_tmp.png')
    return im.convert('RGBA')
cur=rgba('picaraio.png'); prev=rgba(sys.argv[1] if len(sys.argv)>1 else '../../af/picapau_evo.png')
o=np.load('r1.npy'); ys,xs=np.where(o>0); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1; dx=(64-w)//2-xs.min(); dy=63-h-ys.min()
# model op spriteformaat: 1024 -> zelfde raster (cel 15.36 px, oorsprong 4*5.12 / 5.12), oppervlakgemiddelde
mi=Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')
S=15.36; box=(int(4*5.12),int(5.12),int(4*5.12+64*S),int(5.12+66*S))
m1=mi.crop(box).resize((64,66),Image.BOX); mod=Image.new('RGB',(64,64),(255,255,255)); mod.paste(m1,(dx,dy)); mod=mod.convert('RGBA')
def on(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
W=3*512+40; H=24+512+30+20*12+20
V=Image.new('RGB',(W,H),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(cur,'r1'),(prev,'vorige (af/picapau_evo.png)'),(mod,'model r9 verkleind (oppervlak)')]):
    V.paste(on(im,(255,255,255,255),8),(10+i*522,20)); d.text((10+i*522,4),t,fill=(0,0,0))
# kop: spritecoords x 6..34, y 0..20
x0,y0,x1,y1=6+dx,0+dy,34+dx,20+dy
kc=on(cur.crop((x0,y0,x1,y1)),(255,255,255,255),12)
km=mi.crop((int(4*5.12+6*S),int(5.12+0*S),int(4*5.12+34*S),int(5.12+20*S))).resize(kc.size,Image.LANCZOS)
yk=20+512+26; V.paste(kc,(10,yk)); V.paste(km,(20+kc.width,yk)); d.text((10,yk-14),'kop 12x  |  model',fill=(0,0,0))
x=40+2*kc.width
for bg in ((248,248,248,255),(40,40,48,255)):
    V.paste(on(cur,bg,1),(x,yk)); V.paste(on(cur,bg,2),(x+74,yk)); x+=220
V.save('vel.png'); print(V.size)
