# Jordi (16 nov): "pokemon hebben over het algemeen geen special effects, dus daarom twijfel ik"
# Variant 1: losse barst linksonder weg. Barstpixels = verschil r10 B / r10 rond (maker haalde daar de barst weg, rest = model)
# plus de 2-px-verschuiving van r18; teruggezet naar r10 rond (dus model) en r17-opschoning behouden.
from PIL import Image, ImageDraw
import numpy as np
L=lambda f: np.array(Image.open(f))
B=L('../r10/sprite_B.png'); R=L('../r10/sprite_rond.png'); a17=L('../r17/sprite.png')
src=Image.open('../r18/sprite_2_ook_linksonder_verschoven.png'); cur=np.array(src)
zone=np.zeros_like(B,bool); zone[25:,:27]=True
S=(((B!=R)&(B!=0))|(cur!=a17))&zone
new=cur.copy()
for y,x in np.argwhere(S):
    if (x,y) in {(20,33),(21,34)}: new[y,x]=a17[y,x]
    elif B[y,x]!=R[y,x] and R[y,x]!=0 and B[y,x]!=0: new[y,x]=R[y,x]
    else: new[y,x]=0
new[34,11]=0; new[35,3]=0   # losse barstresten (1 px)
im=Image.fromarray(new,'P'); im.putpalette(src.getpalette()); im.save('sprite_1_zonder_barst.png',transparency=0)
outs=[('nu (r18 2)','../r18/sprite_2_ook_linksonder_verschoven.png'),('1: zonder losse barst','sprite_1_zonder_barst.png')]
S_=6; W=Image.new('RGB',(16+len(outs)*(64*S_+20),64*S_+60+140),(235,235,235)); d=ImageDraw.Draw(W)
for i,(k,f) in enumerate(outs):
    r=Image.open(f).convert('RGBA'); x=16+i*(64*S_+20); d.text((x,4),k,fill=(0,0,0))
    for j,c in enumerate([(255,255,255),(40,40,48)]):
        b=Image.new('RGBA',r.size,c+(255,)); b.alpha_composite(r)
        if j==0: W.paste(b.resize((64*S_,64*S_),Image.NEAREST).convert('RGB'),(x,20))
        W.paste(b.resize((128,128),Image.NEAREST).convert('RGB'),(x+j*140,64*S_+40))
W.save('vel.png')
