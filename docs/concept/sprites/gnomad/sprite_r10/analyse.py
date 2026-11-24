# Analyse r9: per buitenlijnpixel groep, normaal en voorstel (alleen printen/visualiseren)
from PIL import Image
import math,sys
im=Image.open('../sprite_r9/gnomad.png'); a=im.load()
G={2:'M',3:'M',4:'M',5:'M',6:'H',7:'H',8:'H',0xc:'S',0xd:'S',0xe:'S',9:'B',0xa:'B',0xb:'B',0xf:'R'}
BASE={'M':2,'H':6,'S':0xe,'B':9}
def T(x,y): return not(0<=x<64 and 0<=y<64) or a[x,y]==0
OUTC={1,2,6,0xe,9}
outl=[(x,y) for y in range(64) for x in range(64) if a[x,y] and a[x,y] in OUTC and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
res={}
for x,y in outl:
    # groep: meerderheid niet-zwarte, niet-transparante buren in straal 2, voorkeur niet-buitenlijn
    cnt={}
    for dx in range(-2,3):
        for dy in range(-2,3):
            X,Y=x+dx,y+dy
            if T(X,Y) or (X,Y)==(x,y): continue
            c=a[X,Y]
            if c==1: continue
            g=G[c]; w=1 if (X,Y) in outl else 3
            cnt[g]=cnt.get(g,0)+w/(abs(dx)+abs(dy))
    g=max(cnt,key=cnt.get) if cnt else '?'
    nx=ny=0
    for dx in range(-2,3):
        for dy in range(-2,3):
            if (dx or dy) and T(x+dx,y+dy):
                d=math.hypot(dx,dy); nx+=dx/d**2; ny+=dy/d**2
    n=math.hypot(nx,ny) or 1; nx/=n; ny/=n
    res[(x,y)]=(g,nx,ny,(nx+ny)/math.sqrt(2))
if __name__=='__main__':
    for k,v in sorted(res.items(),key=lambda t:(t[0][1],t[0][0])): print(k,a[k],v[0],'%.2f'%v[3])
