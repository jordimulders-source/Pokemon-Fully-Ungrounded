# proef r3 punt 3: roze in 2 tinten (per pixel op modelhelderheid) + 3 manieren om een index vrij te maken; vel 6x
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
exec(open('r3/paletmeting.py').read().split("print('roze nu")[0])
lm=lum(M)
def split(o):
  o=o.copy(); m=o==9; o[m&(lm<133)]=16; o[m&(lm>=133)]=17; return o
def rgb(o,pal): return Image.fromarray(np.array([[(255,255,255) if v==0 else pal[v] for v in r] for r in o],np.uint8)).resize((384,384),Image.NEAREST)
base=list(PAL)+[pl,pd_]
V={}
o2=split(o)
pa=list(base); pa[7]=PAL[2]; V['A: 7 rood donker -> bruin 2']=pa
pb=list(base); pb[8]=pl; V['B: 8 rood midden -> roze schaduw']=pb
pc=list(base); c=(104,66,60); pc[7]=c; pc[2]=c; V['C: 2+7 gedeeld (104,66,60)']=pc
V['ideaal (17 kleuren)']=base
vel=Image.new('RGB',(4*394,420),'white'); d=ImageDraw.Draw(vel)
for i,(k,p) in enumerate(V.items()): vel.paste(rgb(o2,p),(i*394,30)); d.text((i*394+4,6),k,fill=0)
vel.save('r3/roze_varianten.png')
