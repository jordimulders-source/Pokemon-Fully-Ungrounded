# sprite (npy/png) naast een RGBA-laag in r7-coordinaten, zelfde uitsnede en schaal, met spriteraster
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *; from reduceer import s2o
sp,laag,out=sys.argv[1:4]; x0,y0,x1,y1=[int(v) for v in sys.argv[4:8]]; F=int(sys.argv[8]) if len(sys.argv)>8 else 16
o=np.array(Image.open(sp)) if sp.endswith('png') else np.load(sp)
a=Image.fromarray(rgb(o,(200,230,255))[y0:y1,x0:x1]).resize(((x1-x0)*F,(y1-y0)*F),Image.NEAREST)
L=Image.open(laag).convert('RGBA'); bg=Image.new('RGBA',L.size,(200,230,255,255)); bg.alpha_composite(L)
ox0,oy0=s2o(x0,y0); ox1,oy1=s2o(x1,y1); b=bg.crop((int(ox0),int(oy0),int(ox1),int(oy1))).resize(a.size,Image.NEAREST).convert('RGB')
for im in (a,b):
    d=ImageDraw.Draw(im)
    for X in range(x1-x0+1): d.line([(X*F,0),(X*F,im.height)],fill=(255,0,0) if (X+x0)%5==0 else (255,190,190))
    for Y in range(y1-y0+1): d.line([(0,Y*F),(im.width,Y*F)],fill=(255,0,0) if (Y+y0)%5==0 else (255,190,190))
v=Image.new('RGB',(a.width*2+10,a.height),'white'); v.paste(a,(0,0)); v.paste(b,(a.width+10,0)); v.save(out)
