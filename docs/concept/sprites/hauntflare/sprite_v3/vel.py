# Vel v3: v3 8x | v2 8x | basis 8x; gezicht 12x naast Haunter 12x; v3 1x en 2x op licht/donker
from PIL import Image, ImageDraw; import numpy as np, json
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v3/'
def opwit(im,bg=(255,255,255)):
    im=im.convert('RGBA'); w=Image.new('RGBA',im.size,bg+(255,)); w.alpha_composite(im); return w.convert('RGB')
v3=Image.open(S+'hauntflare_v3.png').convert('RGBA'); v2=Image.open(D+'sprite_v2/hauntflare_v2.png').convert('RGBA')
ba=Image.open(D+'basis/basis_64.png')
h=Image.open('graphics/pokemon/haunter/anim_front.png').convert('RGBA').crop((0,0,64,64))
hp=np.array(h); hp[(hp[...,0]==0x98)&(hp[...,1]==0xd0)&(hp[...,2]==0xa0)]=(255,255,255,255); h=Image.fromarray(hp)
V=Image.new('RGB',(3*522+10,522+330),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(v3,'Hauntflare v3'),(v2,'v2'),(ba,'basis')]):
    V.paste(opwit(im).resize((512,512),0),(10+i*522,10)); d.text((10+i*522,524),t,fill=(0,0,0))
g=json.load(open(D+'sprite_v2/bouw_log.json'))['gezicht_offset']; hx0,hy0=11,26
V.paste(opwit(v3).crop((hx0+g[0],hy0+g[1],hx0+g[0]+26,hy0+g[1]+22)).resize((312,264),0),(10,545))
V.paste(opwit(h).crop((hx0,hy0,hx0+26,hy0+22)).resize((312,264),0),(332,545))
d.text((10,812),'gezicht v3 12x | Haunter 12x',fill=(0,0,0))
for j,bg in enumerate([(248,248,240),(40,40,48),(255,255,255),(0,0,0)]):
    V.paste(opwit(v3,bg),(700+j*80,545)); V.paste(opwit(v3,bg).resize((128,128),0),(700+j*140,630))
V.save(S+'vel.png')
