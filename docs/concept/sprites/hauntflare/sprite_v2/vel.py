# Vel: v2 8x | basis 8x | model verkleind (oppervlak) 8x | Haunter 8x; gezicht 12x naast Haunter 12x; v2 1x licht/donker
from PIL import Image, ImageDraw; import numpy as np
import json
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v2/'
def opwit(im,bg=(255,255,255)):
    im=im.convert('RGBA'); w=Image.new('RGBA',im.size,bg+(255,)); w.alpha_composite(im); return w.convert('RGB')
v2=Image.open(S+'hauntflare_v2.png').convert('RGBA')
ba=Image.open(D+'basis/basis_64.png')
m=np.asarray(Image.open(D+'model/model_claude_natief.png').convert('RGB'))
ys,xs=np.where(m.min(2)<0xe0); mc=Image.fromarray(m[ys.min():ys.max()+1,xs.min():xs.max()+1])
s=62/max(mc.size); mv=mc.resize((round(mc.size[0]*s),round(mc.size[1]*s)),Image.BOX)
mm=Image.new('RGB',(64,64),'white'); mm.paste(mv,((64-mv.size[0])//2,64-mv.size[1]-1))
h=Image.open('graphics/pokemon/haunter/anim_front.png').convert('RGBA').crop((0,0,64,64))
hp=np.array(h); hp[(hp[...,0]==0x98)&(hp[...,1]==0xd0)&(hp[...,2]==0xa0)]=(255,255,255,255); h=Image.fromarray(hp)
V=Image.new('RGB',(4*522+10,522+400),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(opwit(v2),'Hauntflare v2'),(opwit(ba),'basis (basis_64)'),(mm,'model verkleind (oppervlak)'),(opwit(h),'Haunter Gen 3')]):
    V.paste(im.resize((512,512),0),(10+i*522,10)); d.text((10+i*522,512+12),t,fill=(0,0,0))
g=json.load(open(S+'bouw_log.json'))['gezicht_offset']
# gezicht: Haunter x13-33,y28-45 -> v2 op offset; uitsnede 26x22 rond het blok
hx0,hy0=11,26
fz=opwit(v2).crop((hx0+g[0],hy0+g[1],hx0+g[0]+26,hy0+g[1]+22)).resize((312,264),0)
fh=opwit(h).crop((hx0,hy0,hx0+26,hy0+22)).resize((312,264),0)
V.paste(fz,(10,560)); V.paste(fh,(332,560)); d.text((10,830),'gezicht v2 12x | Haunter 12x (zelfde uitsnede t.o.v. het blok)',fill=(0,0,0))
for j,bg in enumerate([(248,248,240),(40,40,48),(255,255,255),(0,0,0)]):
    V.paste(opwit(v2,bg),(700+j*80,560))
    V.paste(opwit(v2,bg).resize((128,128),0),(700+j*140,650))
V.save(S+'vel.png')
