# Eindkeuring Ledian-evo: analyse van de buitenlijn van rood_c (alleen printen).
# Per buitenlijnpixel (grenst 4-buur aan transparant): groep van het onderdeel (meerderheid niet-zwarte buren r=2,
# gewogen), normaal naar buiten (gewogen transparante buren r=2) en lichtscore = normaal . (-1,-1)/sqrt2 (licht linksboven).
from PIL import Image
import math
SRC='../sprite_r2/rood_c.png'
a=Image.open(SRC).load()
G={7:'R',8:'R',9:'R',10:'R',3:'W',4:'W',5:'W',6:'W',11:'Y',12:'Y',2:'D'}
def T(x,y): return not(0<=x<64 and 0<=y<64) or a[x,y]==0
outl=[(x,y) for y in range(64) for x in range(64) if a[x,y] and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
S=set(outl)
res={}
for x,y in outl:
    cnt={}
    for dx in range(-2,3):
        for dy in range(-2,3):
            X,Y=x+dx,y+dy
            if T(X,Y) or (dx,dy)==(0,0): continue
            c=a[X,Y]
            if c==1: continue
            g=G[c]; w=1 if (X,Y) in S else 3
            cnt[g]=cnt.get(g,0)+w/(abs(dx)+abs(dy))
    g=max(cnt,key=cnt.get) if cnt else '?'
    nx=ny=0
    for dx in range(-2,3):
        for dy in range(-2,3):
            if (dx or dy) and T(x+dx,y+dy):
                d=math.hypot(dx,dy); nx+=dx/d**2; ny+=dy/d**2
    n=math.hypot(nx,ny) or 1; nx/=n; ny/=n
    res[(x,y)]=(g,nx,ny,-(nx+ny)/math.sqrt(2))
if __name__=='__main__':
    for y in range(64):
        s=''
        for x in range(64):
            v=a[x,y]
            if (x,y) in res:
                g,_,_,l=res[(x,y)]
                if v==1: s+= ('L' if l>0.2 else ('s' if l<-0.2 else '?')) if g=='R' else ({'Y':'y','W':'w','D':'d'}.get(g,'?') if l>0.2 else 'k')
                elif v==7: s+= 'O' if l<-0.2 else ('7' if l>0.2 else 'o')
                else: s+='0123456789abcdef'[v]
            else: s+='.' if v==0 else '0123456789abcdef'[v]
        print('%2d '%y+s)
