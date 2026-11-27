# vel.png: model (op spriteschaal, 8x) | kale 0,80 | r1 | fase 3 af, plus gezicht-close-up 16x (model | kaal | r1)
import os, json; import numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); G=json.load(open(os.path.join(H,'geo_0.80.json')))
def s2m(i,j): return ((i-G['ox'])*G['T']+G['cx'], (j-G['oy'])*G['T']+G['cy'])
model=Image.open(os.path.join(H,'../../model.png')).convert('RGB')
def mcrop(i0,j0,i1,j1,z):
    a=s2m(i0,j0); b=s2m(i1,j1); return model.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize(((i1-i0)*z,(j1-j0)*z),Image.LANCZOS)
def spr(p,i0,j0,i1,j1,z):
    im=Image.open(p); im.save('/tmp/_v.png',transparency=im.info.get('transparency',0)) if False else None
    a=im.convert('RGBA'); bg=Image.new('RGBA',a.size,(200,230,200,255)); bg.alpha_composite(a)
    return bg.crop((i0,j0,i1,j1)).resize(((i1-i0)*z,(j1-j0)*z),Image.NEAREST).convert('RGB')
P=[None,os.path.join(H,'../maten/kaal_0.80.png'),os.path.join(H,'zandloper_fase2_r1.png'),os.path.join(H,'../../../fase3/af/zandloper_fase3.png')]
T=['model (spriteschaal)','kale reductie 0,80','r1','fase 3 af']
W=4*520; out=Image.new('RGB',(W,512+30+20*16+30),(255,255,255)); d=ImageDraw.Draw(out)
for k,p in enumerate(P):
    im=mcrop(0,0,64,64,8) if p is None else spr(p,0,0,64,64,8)
    out.paste(im,(k*520,30)); d.text((k*520+4,8),T[k],fill=(0,0,0))
# close-up gezicht: sprite (20..40, 18..30) op 16x
i0,j0,i1,j1=20,18,40,29; z=16; y=512+60
for k,p in enumerate(P[:3]):
    im=mcrop(i0,j0,i1,j1,z) if p is None else spr(p,i0,j0,i1,j1,z)
    out.paste(im,(k*(20*z+16),y))
d.text((4,y-20),'gezicht 16x: model | kaal 0,80 | r1',fill=(0,0,0))
out.save(os.path.join(H,'vel.png'))
