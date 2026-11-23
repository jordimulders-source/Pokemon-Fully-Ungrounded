# model per spritecel (rood raster) | r3 | r4, buikzone, met coordinaten (Jordi: "leg ze allebei op een raster")
import sys; sys.path[:0]=['gereedschap','sprite_r1']
import numpy as np; from PIL import Image
import bouw_a0; from raster import modelcrop, grid
S,OX,OY=bouw_a0.S,bouw_a0.OX,bouw_a0.OY
x0,y0,x1,y1,z=22,36,46,58,32
A=grid(modelcrop(S,OX,OY,x0,y0,x1,y1,z),x0,y0,z)
def spr(p):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,(200,230,200,255)); b.alpha_composite(im)
    return grid(b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),x0,y0,z,(120,120,120))
P=[A,spr('sprite_r3/A0.png'),spr('sprite_r6/A0.png')]
v=Image.new('RGB',(A.width*3+20,A.height),'white')
for i,p in enumerate(P): v.paste(p,(i*(A.width+10),0))
v.save('sprite_r6/raster_buik.png')
