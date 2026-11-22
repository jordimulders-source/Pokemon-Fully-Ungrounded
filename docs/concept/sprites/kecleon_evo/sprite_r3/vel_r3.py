# Vel: r3 | r2 | originele Gen 3-Kecleon (8x), r3 op 1x en 2x op licht en donker, paletstrook r3.
import numpy as np
from PIL import Image, ImageDraw
from bouw_r3_palet import PAL
BG=(200,206,214,255)
def op(im,c,f):
    t=Image.new('RGBA',im.size,c); t.alpha_composite(im); return t.resize((im.width*f,im.height*f),Image.NEAREST)
r3=Image.open('kecleon_evo_r3.png').convert('RGBA')
r2=Image.open('../sprite_r2/kecleon_evo_r2.png').convert('RGBA')
k=Image.open('../../../../../graphics/pokemon/kecleon/anim_front_gba.png')
pal=[int(v) for v in open('../../../../../graphics/pokemon/kecleon/normal_gba.pal').read().split()[3:]]
k.putpalette(pal+[0]*(768-len(pal))); k=k.crop((0,0,64,64)).convert('RGBA')
ka=np.array(k); ka[(ka[...,0]==pal[0])&(ka[...,1]==pal[1])&(ka[...,2]==pal[2])]=0; k=Image.fromarray(ka)
namen={'k':'omlijning','r':'oranje lijn/selout','H':'oranje schaduw','G':'oranje midden','F':'oranje licht',
       'E':'mosterd lijn','C':'mosterd schaduw','B':'mosterd midden','A':'mosterd licht','p':'roze licht','q':'roze schaduw','w':'glans pupil'}
W=Image.new('RGBA',(3*522+10+150,512+60+len(namen)*22+10),(235,235,235,255))
d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(r3,'r3'),(r2,'r2'),(k,'Kecleon Gen 3 (origineel)')]):
    W.paste(op(im,BG,8),(10+522*i,30)); d.text((14+522*i,10),t+' (8x)',fill=(0,0,0))
x=10+3*522
for i,c in enumerate([(248,248,248,255),(36,36,44,255)]):
    W.paste(op(r3,c,2),(x,30+140*i)); W.paste(op(r3,c,1),(x+32,320+80*i))
d.text((x,10),'r3 2x / 1x',fill=(0,0,0))
y=560
d.text((10,y),'palet r3 (12 kleuren + transparant): letter | rgb | helderheid | rol',fill=(0,0,0)); y+=18
for key,nm in namen.items():
    c=PAL[key]; Y=round(0.299*c[0]+0.587*c[1]+0.114*c[2])
    d.rectangle([10,y,40,y+18],fill=tuple(c)+(255,),outline=(0,0,0))
    d.text((50,y+3),f"{key}  {tuple(c)}  Y={Y}  {nm}",fill=(0,0,0)); y+=22
W.convert('RGB').save('vel.png')
