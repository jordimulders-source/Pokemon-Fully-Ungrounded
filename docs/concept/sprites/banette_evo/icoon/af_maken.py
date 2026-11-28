"""af/icon_8x.png (front 4x + frame 1 en 2 op 8x) en af/icon_anim.gif uit af/icon.png"""
import numpy as np
from PIL import Image
D='docs/concept/sprites/banette_evo/'
ic=Image.open(D+'icoon/af/icon.png'); a=np.array(ic)
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
def rgb(x):
    o=IP[x].astype(np.uint8); o[x==0]=(115,197,164); return Image.fromarray(o)
fr=Image.open(D+'af/shuppetto.png').convert('RGBA').resize((256,256),Image.NEAREST)
W=Image.new('RGB',(256*3+20,256),(115,197,164)); W.paste(fr,(0,0),fr)
W.paste(rgb(a[:32]).resize((256,256),Image.NEAREST),(266,0)); W.paste(rgb(a[32:]).resize((256,256),Image.NEAREST),(532,0))
W.save(D+'icoon/af/icon_8x.png')
fs=[rgb(a[:32]).resize((128,128),Image.NEAREST),rgb(a[32:]).resize((128,128),Image.NEAREST)]
fs[0].save(D+'icoon/af/icon_anim.gif',save_all=True,append_images=fs[1:],duration=267,loop=0)
print(ic.size,ic.mode,ic.info.get('transparency'))
