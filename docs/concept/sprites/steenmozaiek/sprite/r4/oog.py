# Oog: bovenkant niet meer afgekapt (Jordi: "bovenkant oog is wat afgekapt"). Basis r3 A; alleen pixels in x11-15, y17-20.
from PIL import Image; import numpy as np
b=Image.open('r3/steenjaguar_r3_A.png'); P=np.asarray(b).copy()
V={'1':{(13,18):1},                                   # koepel van 1 px, glans blijft midden
   '2':{(13,18):1,(12,19):15,(13,19):1},               # koepel + glans linksboven
   '3':{(12,18):1,(13,18):1,(14,18):1,(12,19):15,(13,19):1,(11,19):1,(15,19):1}}  # rond 5 breed bovenaan, glans linksboven
out=[]
for k,ed in V.items():
    q=P.copy()
    for (x,y),v in ed.items(): q[y,x]=v
    im=Image.fromarray(q,'P'); im.putpalette(b.getpalette()); im.info['transparency']=0; im.save(f'r4/oog_{k}.png',transparency=0); out.append(im)
crop=lambda im:im.convert('RGBA').crop((7,14,20,24)).resize((13*16,10*16),Image.NEAREST)
V_=Image.new('RGBA',(4*(13*16+10),10*16+120),(235,235,235,255))
for i,im in enumerate([b]+out):
    V_.paste(crop(im),(i*(13*16+10),0)); s=im.convert('RGBA'); V_.paste(s.crop((0,10,40,45)).resize((80,70),Image.NEAREST),(i*(13*16+10)+10,170)); V_.paste(s.crop((0,10,40,45)),(i*(13*16+10)+120,180))
V_.save('r4/oog_varianten.png')
