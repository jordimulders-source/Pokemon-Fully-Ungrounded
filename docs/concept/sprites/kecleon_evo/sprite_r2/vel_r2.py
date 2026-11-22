# Vel: r2 | r1 | verkleind model | originele Gen 3-Kecleon (alle 8x), 1x op licht/donker, paletstrook met meetplek.
import json
from PIL import Image, ImageDraw
P=json.load(open('palet_gemeten.json'))
BG=(200,206,214,255)
def op(im,c,f):
    t=Image.new('RGBA',im.size,c); t.alpha_composite(im); return t.resize((im.width*f,im.height*f),Image.NEAREST)
r2=Image.open('kecleon_evo_r2.png').convert('RGBA')
r1=Image.open('../sprite_r1/kecleon_evo_r1.png').convert('RGBA')
m=Image.new('RGBA',(64,64),(0,0,0,0)); m.alpha_composite(Image.open('../sprite_r1/model_verkleind63.png').convert('RGBA'),(0,1))
k=Image.open('../../../../../graphics/pokemon/kecleon/anim_front_gba.png')
pal=[int(v) for v in open('../../../../../graphics/pokemon/kecleon/normal_gba.pal').read().split()[3:]]
k.putpalette(pal+[0]*(768-len(pal))); k=k.crop((0,0,64,64)).convert('RGBA')
import numpy as np
ka=np.array(k); ka[(ka[...,0]==pal[0])&(ka[...,1]==pal[1])&(ka[...,2]==pal[2])]=0; k=Image.fromarray(ka)
W=Image.new('RGBA',(4*522+10+150,512+60+len(P)*22+20),(235,235,235,255))
d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(r2,'r2'),(r1,'r1'),(m,'verkleind model'),(k,'Kecleon Gen 3 (origineel)')]):
    W.paste(op(im,BG,8),(10+522*i,30)); d.text((14+522*i,10),t+' (8x)',fill=(0,0,0))
x=10+4*522
for i,c in enumerate([(248,248,248,255),(36,36,44,255)]):
    W.paste(op(r2,c,2),(x,30+140*i)); W.paste(op(r2,c,1),(x+32,320+80*i))
y=560
d.text((10,y),'palet r2: kleur | rgb | gemeten in (bestand, x,y) | groep',fill=(0,0,0)); y+=18
namen={'r1':'model/r1_nat100.png','r2':'model/r2_nat100.png'}
for key,v in P.items():
    d.rectangle([10,y,40,y+18],fill=tuple(v['rgb'])+(255,),outline=(0,0,0))
    bron='r1_nat100' if v['bron'].startswith('r1') else 'r2_nat100'
    d.text((50,y+3),f"{key}  {tuple(v['rgb'])}   {bron} ({v['plek'][0]},{v['plek'][1]})   {v['bron']}  (n={v['n']}, mediaan)",fill=(0,0,0)); y+=22
d.rectangle([10,y,40,y+18],fill=(255,255,255,255),outline=(0,0,0)); d.text((50,y+3),'w  (255,255,255)   glans in de pupil (model: lichte pixel in de pupil van combi_kop)',fill=(0,0,0))
W.convert('RGB').save('vel.png')
