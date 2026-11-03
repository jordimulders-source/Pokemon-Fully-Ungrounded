# Metingen eindkeuring ronde 11 (alleen lezen)
import numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/'
im=Image.open(R+'kleur/ronde14/nachtaap.png'); a=np.array(im)
print('mode',im.mode,im.size,'transp',im.info.get('transparency'))
pal=[tuple(map(int,l.split())) for l in open(R+'kleur/ronde14/normal.pal').read().split('\n')[3:19]]
pimg=im.getpalette()[:48]; print('png-palet == .pal:', [tuple(pimg[i*3:i*3+3]) for i in range(16)]==pal)
op=a>0; print('pixels',op.sum())
sil=np.array([[c=='#' for c in l.strip()] for l in open(R+'silhouet/silhouet_bevroren.txt') if l.strip()])
print('alpha-diff txt',(sil!=op).sum())
try:
    n=np.load(R+'silhouet/silhouet_bevroren.npy'); print('alpha-diff npy',((n>0)!=op).sum())
except Exception as e: print('npy',e)
cnt={i:int((a==i).sum()) for i in range(1,16)}; print('kleuren',cnt)
print('aandeel zwart (1) %.3f, 1+2 %.3f'%(cnt[1]/op.sum(),(cnt[1]+cnt[2])/op.sum()))
H,W=a.shape
# rand: opake pixels naast transparant
edge=[(x,y) for y in range(H) for x in range(W) if op[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or not op[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
openr=[(x,y,int(a[y,x])) for x,y in edge if a[y,x] not in (1,2)]
print('randpixels',len(edge),'niet-omlijning op de rand (open):',openr)
print('donkere rand (1) aandeel %.2f'%(sum(a[y,x]==1 for x,y in edge)/len(edge)))
# losse pixels: kleur die geen 4-buur van dezelfde kleur heeft (binnen)
los=[]
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v in (0,1,2): continue
        if not any(0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]==v for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): los.append((x,y,int(v)))
print('losse pixels',len(los),los)
# rechte stukken >=4 van omlijning (1/2) op de rand, horizontaal/verticaal
def runs(mask):
    out=[]
    for y in range(H):
        x=0
        while x<W:
            if mask[y,x]:
                s=x
                while x<W and mask[y,x]: x+=1
                if x-s>=4: out.append(('h',y,s,x-1,x-s))
            else: x+=1
    for x in range(W):
        y=0
        while y<H:
            if mask[y,x]:
                s=y
                while y<H and mask[y,x]: y+=1
                if y-s>=4: out.append(('v',x,s,y-1,y-s))
            else: y+=1
    return out
em=np.zeros_like(op); 
for x,y in edge: em[y,x]=True
print('rechte stukken silhouetrand >=4:',runs(em))
dark=(a==1)|(a==2); inner=dark&~em
print('rechte stukken interne lijnen >=4:',runs(inner))
# wiggen
F=(a==15); six=(a==6)
print('F px',F.sum(),'lila(6) px',six.sum())
for y in range(24,42):
    print(y,''.join('F' if F[y,x] else ('6' if six[y,x] else '.') for x in range(18,50)))
