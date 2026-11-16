# Jordi (16 nov), over de losse vlam rechtsboven: "deze vlam hier is aan de onderkant een rechte lijn, daar mag iets meer contrast in, misschien 1 of 2 pixels anders"
from PIL import Image, ImageDraw
import numpy as np
src=Image.open('../r12/sprite_B_p2.png'); a0=np.array(src); pal=src.getpalette()
V={'A':{(44,6):0,(42,6):10},          # punt rechts weg + tintwissel in de lijn
   'B':{(43,6):0,(41,6):10},          # inkeping in het midden
   'C':{(42,7):1,(44,6):0},           # bolling omlaag in het midden, punt rechts weg
   'D':{(41,7):1,(42,7):1}}           # 2 px bolling omlaag
outs=[]
for k,ch in V.items():
    a=a0.copy()
    for (x,y),v in ch.items(): a[y,x]=v
    im=Image.fromarray(a,'P'); im.putpalette(pal); im.save(f'sprite_{k}.png',transparency=0); outs.append((k,f'sprite_{k}.png'))
outs.append(('r12 p2','../r12/sprite_B_p2.png'))
S=24; W=Image.new('RGB',(16+len(outs)*(14*S+12),8*S+60+140),(235,235,235)); d=ImageDraw.Draw(W)
for i,(k,f) in enumerate(outs):
    rgba=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',rgba.size,(255,255,255,255)); bg.alpha_composite(rgba)
    x=16+i*(14*S+12); d.text((x,4),k,fill=(0,0,0))
    W.paste(bg.crop((35,1,49,9)).resize((14*S,8*S),Image.NEAREST).convert('RGB'),(x,20))
    W.paste(bg.convert('RGB').resize((128,128),Image.NEAREST),(x,8*S+40))
W.save('vel.png')
