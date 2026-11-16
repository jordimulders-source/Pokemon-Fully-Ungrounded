# cmp.py IDX.npy OUT x0 y0 x1 y1 : spritezone (64-coörd) op 18x naast hetzelfde stuk model (natief) op 12x, met raster+coördinaten
import sys; sys.path.insert(0,'sprite_r1'); from PIL import Image, ImageDraw; import numpy as np; import pal; from render import img
idx=np.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[3:7])
s=img(idx,pal.TROUW,1,(255,255,255)).crop((x0,y0,x1,y1)); S=18
s=s.resize((s.width*S,s.height*S),Image.NEAREST); d=ImageDraw.Draw(s)
for x in range(x1-x0):
    d.line([(x*S,0),(x*S,s.height)],fill=(0,160,255)); d.text((x*S+2,2),str(x0+x)[-2:],fill=(0,120,255))
for y in range(y1-y0):
    d.line([(0,y*S),(s.width,y*S)],fill=(0,160,255)); d.text((2,y*S+2),str(y0+y),fill=(255,0,0))
n=Image.open('basis/natief.png').convert('RGB')
nx0=17+(x0-9)*1.5; ny0=18+(y0-8)*1.5
m=n.crop((int(nx0),int(ny0),int(nx0+(x1-x0)*1.5),int(ny0+(y1-y0)*1.5)))
m=m.resize((m.width*12,m.height*12),Image.NEAREST)
out=Image.new('RGB',(s.width+m.width+10,max(s.height,m.height)),(255,255,255)); out.paste(s,(0,0)); out.paste(m,(s.width+10,0)); out.save(sys.argv[2])
