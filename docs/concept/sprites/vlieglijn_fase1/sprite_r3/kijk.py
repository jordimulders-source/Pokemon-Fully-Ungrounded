# kijkvel: sprite op 12x naast natief model op dezelfde schaal, met raster. python3 kijk.py IN.txt UIT.png [S]
import numpy as np; from PIL import Image, ImageDraw; import sys
from reduce_pal import PAL
S=float(sys.argv[3]) if len(sys.argv)>3 else 1.34
o=np.loadtxt(sys.argv[1],dtype=int); H,W=o.shape; Z=14
rgb=np.array([(255,255,255)]+PAL[1:])[o].astype('uint8')
sp=Image.fromarray(rgb).resize((W*Z,H*Z),Image.NEAREST)
nat=Image.open('natief.png').convert('RGB').resize((1000,1000),Image.NEAREST).crop((170,200,int(170+W*S*10),int(200+H*S*10))).resize((W*Z,H*Z),Image.NEAREST)
v=Image.new('RGB',(W*Z*2+10,H*Z),'white'); v.paste(sp,(0,0)); v.paste(nat,(W*Z+10,0))
d=ImageDraw.Draw(v)
for off in (0,W*Z+10):
  for k in range(0,W+1,5): d.line([(off+k*Z,0),(off+k*Z,H*Z)],fill=(255,0,0) if k%10==0 else (255,170,170)); d.text((off+k*Z+2,2),str(k),fill=(255,0,0))
  for k in range(0,H+1,5): d.line([(off,k*Z),(off+W*Z,k*Z)],fill=(255,0,0) if k%10==0 else (255,170,170)); d.text((off+2,k*Z+2),str(k),fill=(255,0,0))
v.save(sys.argv[2])
