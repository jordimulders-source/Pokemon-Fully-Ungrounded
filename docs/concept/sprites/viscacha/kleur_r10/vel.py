"""vel.png: r10 | r9 | model (8x), Taillow + Raticate (Gen 3, 8x), close-up rug (16x), 1x licht/donker."""
import sys; sys.path.insert(0,'../kleur_r8/stappen'); from tl import *
from PIL import ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
import importlib.util
_s=importlib.util.spec_from_file_location('p9','palet.py'); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m); P9=_m.PAL
R9=raster('raster.txt'); R8=raster('../kleur_r9/raster.txt')
def rim(R,P,bg=(255,255,255)):
    im=Image.new('RGB',(64,64)); im.putdata([bg if c=='.' else P[int(c,16)] for r in R for c in r]); return im
a=rim(R9,P9); b=rim(R8,P9)
ref=[Image.open(G+n+'/anim_front_gba.png').convert('RGB').crop((0,0,64,64)) for n in ('taillow','raticate')]
W=Image.new('RGB',(5*520+10,1000),'white'); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(a,'r10'),(b,'r9'),(model(0,0,64,64,8),'model'),(ref[0],'Taillow (Gen 3)'),(ref[1],'Raticate (Gen 3)')]):
    W.paste(im if im.size==(512,512) else im.resize((512,512),0),(i*520,20)); d.text((i*520+4,4),t,fill=(0,0,0))
# close-up rug x26-50, r25-47 op 16x: r10 | r9 | krabbel Jordi (rode lijn + stip)
K=Image.open('../kleur_r9/jordi_krabbel_rug.png').convert('RGB')
kc=K.crop((round(234.4+26*9.93),round(-7.9+25*9.93),round(234.4+50*9.93),round(-7.9+47*9.93))).resize((384,352),Image.NEAREST)
for i,im in enumerate([grid(a.crop((26,25,50,47)).resize((384,352),0),26,25,16),grid(b.crop((26,25,50,47)).resize((384,352),0),26,25,16),grid(kc,26,25,16)]):
    W.paste(im,(i*394,560)); d.text((i*394+4,542),['r10 rug 16x','r9 rug 16x','krabbel Jordi (r9)'][i],fill=(0,0,0))
# 1x licht/donker
y=760
for j,bg in enumerate([(255,255,255),(232,232,216),(48,48,64),(16,16,16)]):
    W.paste(rim(R9,P9,bg),(1200+j*150,y)); W.paste(rim(R8,P9,bg),(1200+j*150,y+80))
d.text((1200,y-16),'1x r10 (boven) / r9 (onder) op licht en donker',fill=(0,0,0))
W.save('vel.png')
