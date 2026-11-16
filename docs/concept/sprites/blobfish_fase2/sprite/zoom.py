# zoom.py sprite.png nx0 ny0 nx1 ny1 uit.png : modeluitsnede (natief, 12x) naast dezelfde zone in de sprite (18x), boven elkaar
import sys; from PIL import Image
f,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
m=Image.open('model_natief.png'); w=Image.new('RGBA',m.size,'white'); w.alpha_composite(m)
mc=w.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
s=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',s.size,'white'); bg.alpha_composite(s); s=bg.convert('RGB')
sx0,sy0=(x0-11)/1.5+1,(y0-21)/1.5+17; sx1,sy1=(x1-11)/1.5+1,(y1-21)/1.5+17
S=18; s=s.resize((64*S,64*S),Image.NEAREST).crop((int(sx0*S),int(sy0*S),int(sx1*S),int(sy1*S)))
v=Image.new('RGB',(max(mc.width,s.width),mc.height+s.height+10),'white'); v.paste(mc,(0,0)); v.paste(s,(0,mc.height+10)); v.save(out)
