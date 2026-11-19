# vel.png: r4 | r3 | model verkleind (8x); onder: kop 12x r4 | kop 12x model | diff r3->r4 (rood) | 1x en 2x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
def rgba(f):
    im=Image.open(f); im.save('_tmp/tmp.png',transparency=0); return Image.open('_tmp/tmp.png').convert('RGBA')
cur=rgba('picaraio.png'); prev=rgba('../r3/picaraio.png')
mi0=Image.open('../../gemini/r9_prompt_v6.png').convert('RGB'); S=15.36
mi=Image.new('RGB',(1024,1060),(255,255,255)); mi.paste(mi0,(0,11))  # 11 px witte rand boven: png-rij y -> modelrij S*y+0.76
# png (x,y) -> model: x0=4*5.12+S*x, y0=S*y-10.24
m=mi.crop((int(20.48),1,int(20.48+64*S),int(1+64*S))).resize((64,64),Image.BOX).convert('RGBA')
def on(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
W=3*522+10; H=24+512+30+20*12+30
V=Image.new('RGB',(W,H),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(cur,'r4'),(prev,'r3'),(m,'model r9 verkleind (oppervlak)')]):
    V.paste(on(im,(255,255,255,255),8),(10+i*522,20)); d.text((10+i*522,4),t,fill=(0,0,0))
x0,y0,x1,y1=6,0,34,20
kc=on(cur.crop((x0,y0,x1,y1)),(255,255,255,255),12)
km=mi.crop((int(20.48+S*x0),int(1+S*y0),int(20.48+S*x1),int(1+S*y1))).resize(kc.size,Image.LANCZOS)
yk=20+512+26; V.paste(kc,(10,yk)); V.paste(km,(20+kc.width,yk)); d.text((10,yk-14),'kop 12x r4  |  model',fill=(0,0,0))
a=np.array(Image.open('../r3/picaraio.png')); b=np.array(Image.open('picaraio.png'))
g=np.array(on(cur,(255,255,255,255),1)).astype(int); g=(g*0.35+165).astype('uint8'); g[a!=b]=(230,30,30)
x=30+2*kc.width; V.paste(Image.fromarray(g).resize((192,192),0),(x,yk)); d.text((x,yk-14),'diff r3->r4',fill=(0,0,0)); x+=205
for bg in ((248,248,248,255),(40,40,48,255)):
    V.paste(on(cur,bg,1),(x,yk)); V.paste(on(cur,bg,2),(x,yk+74)); x+=140
V.save('vel.png'); print(V.size)
