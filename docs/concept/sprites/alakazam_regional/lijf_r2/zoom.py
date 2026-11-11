# zoom.py uit.png [Z]: borst (x22-39, y20-38) van basis + S1..S8 naast elkaar
import sys,pal
from PIL import Image
fs=['basis_O1r.txt']+[f'opt_S{i}.txt' for i in range(1,9)]
b=(22,20,39,38); Z=int(sys.argv[2]) if len(sys.argv)>2 else 12
ims=[pal.rgb(pal.load(f)).crop(b).resize(((b[2]-b[0])*Z,(b[3]-b[1])*Z),Image.NEAREST) for f in fs]
o=Image.new('RGB',(len(ims)*(ims[0].width+8),ims[0].height),'white')
for i,im in enumerate(ims): o.paste(im,(i*(im.width+8),0))
o.save(sys.argv[1])
