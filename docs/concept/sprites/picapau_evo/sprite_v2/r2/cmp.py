# Close-up: sprite-uitsnede (spritecoords x0,y0,x1,y1) op schaal s naast hetzelfde stuk van het model, met raster
import sys; import numpy as np; from PIL import Image, ImageDraw
f,x0,y0,x1,y1,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
import subprocess; subprocess.run(['python3','toon.py',f,'_tmp/cmp.png','1'])
sp=Image.open('_tmp/cmp.png').crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),0)
OY,OX=1,4; c=lambda v,o:(o+3*v)*5.12
mi=Image.open('../../gemini/r9_prompt_v6.png').convert('RGB').crop((int(c(x0,OX)),int(c(y0,OY)),int(c(x1,OX)),int(c(y1,OY)))).resize(sp.size,Image.LANCZOS)
V=Image.new('RGB',(sp.width*2+10,sp.height),(255,255,255)); V.paste(sp,(0,0)); V.paste(mi,(sp.width+10,0))
d=ImageDraw.Draw(V)
for k in range(x1-x0+1):
    for off in (0,sp.width+10): d.line([(off+k*s,0),(off+k*s,sp.height)],fill=(210,210,230) if k%4 else (150,150,255))
for k in range(y1-y0+1):
    d.line([(0,k*s),(V.width,k*s)],fill=(210,210,230) if k%4 else (150,150,255))
V.save(out)
