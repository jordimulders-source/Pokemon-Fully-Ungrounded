# snel vel: argumenten = P-pngs, 8x naast elkaar op grijs met raster
import sys; from PIL import Image
ims=[Image.open(p) for p in sys.argv[2:]]
W=sum(64*8+8 for _ in ims); out=Image.new('RGB',(W,64*8),(200,200,200))
x=0
for im in ims:
    a=im.convert('RGBA') if im.mode!='P' else Image.open(im.filename).convert('RGBA')
    out.paste(a.resize((512,512),0),(x,0),a.resize((512,512),0)); x+=520
out.save(sys.argv[1])
