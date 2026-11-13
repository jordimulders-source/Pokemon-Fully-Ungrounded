# zoom.py: romp (x10-46, y14-52) van basis + opties op 10x naast elkaar -> argv[1]
import sys,pal
from PIL import Image
fs=['basis_r11.txt']+[f'opt_O{i}.txt' for i in range(1,5)]
b=(10,14,46,52); Z=10; ims=[pal.rgb(pal.load(f)).crop(b).resize(((b[2]-b[0])*Z,(b[3]-b[1])*Z),Image.NEAREST) for f in fs]
o=Image.new('RGB',(len(ims)*(ims[0].width+10),ims[0].height),'white')
for i,im in enumerate(ims): o.paste(im,(i*(im.width+10),0))
o.save(sys.argv[1])
