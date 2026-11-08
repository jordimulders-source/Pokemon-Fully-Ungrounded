# box1x.py sprite.png out [x0 y0 x1 y1 zoom]: BOX-verkleind model | sprite op 1x-niveau vergroot (naar poedelmot/kleur_r20/stappen/box1x.py)
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/'
m=Image.open(D+'gemini_samen/stappen/model_512.png').convert('RGB').resize((64,64),Image.BOX)
p=Image.open(sys.argv[1]).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(p); s=bg.convert('RGB')
x0,y0,x1,y1,z=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else [0,0,64,64,6]
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'red')
o.paste(m.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),(0,0))
o.paste(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),((x1-x0)*z+8,0))
o.save(sys.argv[2])
