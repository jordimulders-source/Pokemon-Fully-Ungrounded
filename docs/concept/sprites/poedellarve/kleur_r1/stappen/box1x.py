# box1x.py out [x0 y0 x1 y1 zoom]: BOX-verkleind model | sprite, op 1x-niveau (pixels) vergroot
import sys
from PIL import Image
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/'
k=13.55; X0,Y0=236-k*12,346-k*33
src=Image.open(H+'referenties/model_gekozen.png').convert('RGB')
m=src.crop((int(X0),int(Y0),int(X0+64*k),int(Y0+64*k))).resize((64,64),Image.BOX)
p=Image.open(H+'kleur_r1/poedellarve.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(40,100,60,255)); bg.alpha_composite(p); s=bg.convert('RGB')
a=list(map(int,sys.argv[2:7])) if len(sys.argv)>2 else [0,0,64,64,6]
x0,y0,x1,y1,z=a
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white')
o.paste(m.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),(0,0))
o.paste(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),((x1-x0)*z+8,0))
o.save(sys.argv[1])
