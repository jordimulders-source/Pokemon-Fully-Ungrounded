# kijkvel: sprite (zonder rand) op 12x naast natief model op dezelfde schaal. python3 kijk.py IN.txt UIT.png
import numpy as np; from PIL import Image; import sys
from reduce_pal import PAL
o=np.loadtxt(sys.argv[1],dtype=int); H,W=o.shape; Z=12
rgb=np.array([(235,235,235)]+PAL[1:])[o].astype('uint8')
sp=Image.fromarray(rgb).resize((W*Z,H*Z),Image.NEAREST)
nat=Image.open('natief.png').crop((17,20,84,82)).resize((W*Z,H*Z),Image.LANCZOS)
v=Image.new('RGB',(W*Z*2+10,H*Z),'white'); v.paste(sp,(0,0)); v.paste(nat,(W*Z+10,0))
from PIL import ImageDraw; dr=ImageDraw.Draw(v)
for k in range(0,W,5): dr.text((k*Z+2,2),str(k),fill=(255,0,0))
for k in range(0,H,5): dr.text((2,k*Z+2),str(k),fill=(255,0,0))
v.save(sys.argv[2])
