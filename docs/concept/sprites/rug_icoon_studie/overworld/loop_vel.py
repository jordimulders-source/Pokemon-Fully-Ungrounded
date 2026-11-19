# Loopframes op 8x: per soort voor0 voor1 achter0 achter1 opzij0 opzij1, rode punten = pixels die in frame 2 anders zijn.
# python3 loop_vel.py uit.png soort ...   (repo-root)
import sys,numpy as np
from PIL import Image,ImageDraw
G='graphics/pokemon'; Z=8
def pal(p):
    L=open(p).read().split('\n'); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(int(L[2]))]
sps=sys.argv[2:]; W=Image.new('RGB',(6*32*Z+7*8+80,len(sps)*(32*Z+8)),(150,190,150)); D=ImageDraw.Draw(W)
for r,sp in enumerate(sps):
    o=np.array(Image.open(f'{G}/{sp}/overworld.png'))[:32,:192]; P=pal(f'{G}/{sp}/overworld_normal.pal')
    D.text((2,r*(32*Z+8)+2),sp,fill=(0,0,0))
    for k in range(6):
        fr=o[:,k*32:(k+1)*32]; oth=o[:,(k^1)*32:((k^1)+1)*32]
        x0=80+k*(32*Z+8); y0=r*(32*Z+8)
        for y in range(32):
            for x in range(32):
                if fr[y,x]: D.rectangle([x0+x*Z,y0+y*Z,x0+x*Z+Z-1,y0+y*Z+Z-1],fill=P[fr[y,x]])
                if k%2 and fr[y,x]!=oth[y,x]: D.rectangle([x0+x*Z+3,y0+y*Z+3,x0+x*Z+4,y0+y*Z+4],fill=(255,0,0))
        for g in range(0,33,4): D.line([x0,y0+g*Z,x0+32*Z,y0+g*Z],fill=(120,160,120)); D.line([x0+g*Z,y0,x0+g*Z,y0+32*Z],fill=(120,160,120))
W.save(sys.argv[1])
