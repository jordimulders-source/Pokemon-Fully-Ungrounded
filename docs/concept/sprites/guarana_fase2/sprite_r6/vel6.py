# vel r6: r6 | r5A | fase 1 op 8x; trossen 12x (r6 | r5A | model op schaal); 1x op licht en donker; + toets naast de maatstaf (toets.png)
# voor_jordi_r6_8x.png = r6 naast fase 1, allebei 8x, wit
import sys; sys.path.insert(0,'sprite_r6'); from gemeen2 import *; import numpy as np; from PIL import Image, ImageDraw
W=(255,255,255)
def rgba8(path,s=8,bg=W):
    im=Image.open(path).convert('RGBA') if not path.endswith('r6.png') else None
    a=Image.open(path)
    if a.mode=='P': a.info['transparency']=0
    a=a.convert('RGBA'); B=Image.new('RGBA',a.size,bg+(255,)); B.alpha_composite(a); return B.convert('RGB').resize((a.width*s,a.height*s),0)
r6='sprite_r6/guarana2_r6.png'; r5='sprite_r5/guarana2_r5_A.png'; f1='../guarana/af/guarana.png'
M=Image.fromarray(np.load('sprite_r6/model64.npy').astype('uint8'))
V=Image.new('RGB',(1584,1260),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(((r6,'r6 (8x)'),(r5,'r5 A (8x)'),(f1,'fase 1 af (8x)'))):
    V.paste(rgba8(p),(i*528,20)); d.text((i*528+4,4),t,fill='black')
y=560; d.text((4,y-14),'trossen 12x: r6 | r5 A | model op schaal (L, M, R)',fill='black'); x=0
for (x0,y0,x1,y1) in ((2,15,22,40),(16,8,40,32),(38,16,62,40)):
    for src in (r6,r5,None):
        c=(M if src is None else rgba8(src,1)).crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),0)
        if x+c.width>1584: x=0; y+=c.height+16
        V.paste(c,(x,y)); x+=c.width+6
    x+=24
ys=1180
xs=0
for bg in ((255,255,255),(240,232,208),(152,208,160),(40,40,48),(16,24,40)):
    V.paste(rgba8(r6,1,bg),(xs,ys)); xs+=72
d.text((xs+8,ys+28),'r6 1x op licht en donker',fill='black')
V.save('sprite_r6/vel.png')
T=Image.new('RGB',(1056,512),'white'); T.paste(rgba8(r6),(0,0)); T.paste(rgba8(f1),(544,0)); T.save('sprite_r6/voor_jordi_r6_8x.png')
# toets: r6 | fase 1 | dundragoon | skinguin op 8x (kijkbeeld, geen oplevering)
K=Image.new('RGB',(2112,512),'white')
for i,p in enumerate((r6,f1,'../dundragoon/af/dundragoon.png','../skinguin/af/skinguin.png')): K.paste(rgba8(p),(i*528,0))
K.save('sprite_r6/toets.png')
print(V.size)
