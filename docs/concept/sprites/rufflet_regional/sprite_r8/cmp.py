# vergelijk: sprite (12x) naast natief model (6x) zelfde schaal, met rasterlijnen per 2 sprite-px... 
import numpy as np, sys; from PIL import Image, ImageDraw
f=sys.argv[1]; out=sys.argv[2]; x0,y0,x1,y1=[int(v) for v in sys.argv[3:7]]; S=int(sys.argv[7]) if len(sys.argv)>7 else 12
s=Image.open(f).convert('RGBA'); t=Image.new('RGB',(64,64),(255,255,255)); t.paste(s,(0,0),s)
A=t.crop((x0,y0,x1,y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
n=Image.open('../sprite_r1/natief.png').convert('RGB')
nx0,ny0=2*(x0-15)+18,2*(y0-18)+4
B=n.crop((nx0,ny0,nx0+2*(x1-x0),ny0+2*(y1-y0))).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
V=Image.new('RGB',(2*A.width+20,A.height+20),(255,255,255)); V.paste(A,(0,20)); V.paste(B,(A.width+20,20))
d=ImageDraw.Draw(V)
for im_x in (0,A.width+20):
    for x in range(x0,x1):
        if x%5==0: d.line([(im_x+(x-x0)*S,20),(im_x+(x-x0)*S,20+A.height)],fill=(255,0,255) if x%10==0 else (255,180,255))
        if x%5==0: d.text((im_x+(x-x0)*S+1,2),str(x),fill=(0,0,0))
    for y in range(y0,y1):
        if y%5==0: d.line([(im_x,20+(y-y0)*S),(im_x+A.width,20+(y-y0)*S)],fill=(255,0,255) if y%10==0 else (255,180,255)); d.text((im_x+2,20+(y-y0)*S+1),str(y),fill=(0,0,255))
V.save(out)
