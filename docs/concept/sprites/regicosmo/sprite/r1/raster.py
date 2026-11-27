# Hulpmiddel: natief model (uitvergroot) met het spriteraster erover + spritecoordinaten.  python3 raster.py x0 y0 x1 y1 uit.png
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image, ImageDraw; import kaal as kl, gemeen as g
x0,y0,x1,y1=map(int,sys.argv[1:5]); uit=sys.argv[5]; Z=40
n=Image.open(os.path.join(g.D,'natief.png')).convert('RGB')
M=n.resize((n.width*16,n.height*16),0)
W=Image.new('RGB',((x1-x0)*Z,(y1-y0)*Z),'white'); dr=ImageDraw.Draw(W)
for y in range(y0,y1):
    for x in range(x0,x1):
        nx0=kl.X0+(x-kl.OX)/kl.s; ny0=kl.Y0+(y-kl.OY)/kl.s; nx1=nx0+1/kl.s; ny1=ny0+1/kl.s
        t=M.crop((int(nx0*16),int(ny0*16),int(nx1*16),int(ny1*16))).resize((Z,Z),0)
        W.paste(t,((x-x0)*Z,(y-y0)*Z))
for x in range(x0,x1): dr.line([((x-x0)*Z,0),((x-x0)*Z,W.height)],fill=(0,200,0)); dr.text(((x-x0)*Z+2,2),str(x),fill=(0,120,255))
for y in range(y0,y1): dr.line([(0,(y-y0)*Z),(W.width,(y-y0)*Z)],fill=(0,200,0)); dr.text((2,(y-y0)*Z+12),str(y),fill=(255,0,255))
W.save(uit)
