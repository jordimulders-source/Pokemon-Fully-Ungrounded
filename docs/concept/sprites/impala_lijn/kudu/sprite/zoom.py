# zoom: sprite-uitsnede (spritecoord x0,y0,x1,y1 in het 51-brede raster) op 16x naast het model van dezelfde uitsnede + kale reductie
import sys
from PIL import Image
f,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
mod=sys.argv[7] if len(sys.argv)>7 else 'r2/model_A2a.png'
Z=16; s=Image.open(f); s.save('/tmp/_z.png',transparency=0); s=Image.open('/tmp/_z.png').convert('RGBA')
OX=6
sp=s.crop((OX+x0,y0,OX+x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
m=Image.open(mod).convert('RGBA').crop((91+x0*16,y0*16,91+x1*16,y1*16))
V=Image.new('RGBA',(sp.width*2+10,sp.height),(255,255,255,255)); V.paste(m,(0,0)); V.paste(sp,(sp.width+10,0),sp)
from PIL import ImageDraw
d=ImageDraw.Draw(V)
for i in range(x1-x0+1): d.line([(sp.width+10+i*Z,0),(sp.width+10+i*Z,sp.height)],fill=(200,200,200,80))
V.save(uit)
