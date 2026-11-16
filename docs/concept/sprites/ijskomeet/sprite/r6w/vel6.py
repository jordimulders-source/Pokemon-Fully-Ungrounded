import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image, ImageDraw
from p6 import from_txt, save, PAL
o=from_txt('r6.txt'); save(o,'r6')
im=Image.open('r6.png'); print(im.mode, len(set(np.asarray(im).ravel())),'indices incl. 0')
def rgba(p): return Image.open(p).convert('RGBA')
def on(bg,img):
    b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
r6=rgba('r6.png'); r5=rgba('r5.png'); mod=Image.open('model_12x.png').convert('RGB')
W=1536+40; V=Image.new('RGB',(W,512+20+504+20+160),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(on((255,255,255,255),r6.resize((512,512),0)),(0,0)); V.paste(on((255,255,255,255),r5.resize((512,512),0)),(532,0)); V.paste(mod.resize((512,512),Image.LANCZOS),(1064,0))
d.text((4,4),'r6',fill=(255,0,0)); d.text((536,4),'r5',fill=(255,0,0)); d.text((1068,4),'model',fill=(255,0,0))
y0=532
def crop12(img,box,s=12):
    x0,y_0,x1,y1=box; return on((255,255,255,255),img.crop(box).resize(((x1-x0)*s,(y1-y_0)*s),0))
kb=(18,22,40,42); sb=(0,38,36,62)
k6=crop12(r6,kb); km=mod.crop((kb[0]*12,kb[1]*12,kb[2]*12,kb[3]*12))
V.paste(k6,(0,y0)); V.paste(km,(k6.size[0]+8,y0))
s6=crop12(r6,sb,8); sm=mod.crop((sb[0]*12,sb[1]*12,sb[2]*12,sb[3]*12)).resize(s6.size,Image.LANCZOS)
x=2*k6.size[0]+24; V.paste(s6,(x,y0)); V.paste(sm,(x,y0+s6.size[1]+4)) if False else V.paste(sm,(x+s6.size[0]+8,y0)) if x+2*s6.size[0]+8<=W else None
d.text((4,y0+2),'kern r6 | model (12x)',fill=(255,0,0)); d.text((x+4,y0+2),'schotsen r6 | model (8x)',fill=(255,0,0))
y1=y0+504+20
for k,bg in enumerate([(255,255,255,255),(40,40,48,255)]):
    V.paste(on(bg,r6),(10+k*220,y1)); V.paste(on(bg,r6.resize((128,128),0)),(84+k*220,y1))
V.save('vel_r6.png'); print(V.size)
