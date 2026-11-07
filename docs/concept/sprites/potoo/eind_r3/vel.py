# vel.png: eind_r2 8x | eind_r3 8x | model 8x (zelfde kader), daaronder 1x licht/donker.
import json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
z=8; W=64*z
def sp(path,bgc):
    t=Image.open(path).convert('RGBA'); bg=Image.new('RGBA',(64,64),bgc+(255,)); bg.alpha_composite(t); return bg.convert('RGB')
m=Image.open(P+'model/model_lijf_30.png').convert('RGBA')
mc=m.crop((int(X0),int(Y0),int(X0+64*s),int(Y0+64*s))).resize((W,W),Image.LANCZOS)
mb=Image.new('RGBA',(W,W),(255,255,255,255)); mb.alpha_composite(mc)
v=Image.new('RGB',(3*W+20,W+90),(255,255,255))
for i,p in enumerate((P+'eind_r2/potoo.png',P+'eind_r3/potoo.png')):
    v.paste(sp(p,(255,255,255)).resize((W,W),Image.NEAREST),(i*(W+10),0))
    v.paste(sp(p,(255,255,255)),(i*(W+10)+10,W+12)); v.paste(sp(p,(40,40,48)),(i*(W+10)+90,W+12))
v.paste(mb.convert('RGB'),(2*(W+10),0))
ms=m.crop((int(X0),int(Y0),int(X0+64*s),int(Y0+64*s))).resize((64,64),Image.LANCZOS)
for j,c in enumerate(((255,255,255),(40,40,48))):
    b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(ms); v.paste(b.convert('RGB'),(2*(W+10)+10+80*j,W+12))
v.save('vel.png')
