"""vel.png: r9 | r8 | model (8x), Taillow + Raticate (Gen 3, 8x), close-up rug (16x), 1x licht/donker."""
import sys; sys.path.insert(0,'../kleur_r8/stappen'); from tl import *
from PIL import ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
import importlib.util
_s=importlib.util.spec_from_file_location('p9','palet.py'); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m); P9=_m.PAL
R9=raster('raster.txt'); R8=raster('../kleur_r8/raster.txt')
def rim(R,P,bg=(255,255,255)):
    im=Image.new('RGB',(64,64)); im.putdata([bg if c=='.' else P[int(c,16)] for r in R for c in r]); return im
a=rim(R9,P9); b=rimg(R8)
ref=[Image.open(G+n+'/anim_front_gba.png').convert('RGB').crop((0,0,64,64)) for n in ('taillow','raticate')]
W=Image.new('RGB',(5*520+10,1000),'white'); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(a,'r9'),(b,'r8'),(model(0,0,64,64,8),'model'),(ref[0],'Taillow (Gen 3)'),(ref[1],'Raticate (Gen 3)')]):
    W.paste(im if im.size==(512,512) else im.resize((512,512),0),(i*520,20)); d.text((i*520+4,4),t,fill=(0,0,0))
# close-up rug x26-46, r25-36 op 16x: r9 | r8 | model
for i,im in enumerate([grid(a.crop((26,25,46,36)).resize((320,176),0),26,25,16),grid(b.crop((26,25,46,36)).resize((320,176),0),26,25,16),grid(model(26,25,46,36,16),26,25,16)]):
    W.paste(im,(i*330,560)); d.text((i*330+4,542),['r9 rug 16x','r8 rug 16x','model rug 16x'][i],fill=(0,0,0))
# 1x licht/donker
y=760
for j,bg in enumerate([(255,255,255),(232,232,216),(48,48,64),(16,16,16)]):
    W.paste(rim(R9,P9,bg),(1020+j*150,y)); W.paste(rim(R8,PAL,bg),(1020+j*150,y+80))
d.text((1020,y-16),'1x r9 (boven) / r8 (onder) op licht en donker',fill=(0,0,0))
W.save('vel.png')
