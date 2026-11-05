# Past bewerkingen.txt toe op ronde 12 en controleert: alpha-diff, open randen (zelfde regel als bouw.py eerdere rondes), losse pixels, diff per zone
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(H,'../../')
src=Image.open(os.path.join(K,'ronde12/nachtaap.png')); a=np.array(src); b=a.copy()
L='.kdsblmnwrijcetf'
for line in open(os.path.join(H,'bewerkingen.txt')):
    line=line.split('#')[0].strip()
    if not line: continue
    x,y,ch=line.split(); b[int(y),int(x)]=L.index(ch)
SIL=np.array([[c=='#' for c in l.rstrip('\n')] for l in open(os.path.join(K,'../silhouet/silhouet_bevroren.txt'))][:64])
print('alpha-diff:',int(((b!=0)!=SIL).sum()))
def openr(m):
    o=[]
    for y in range(64):
        for x in range(64):
            v=m[y,x]
            if v==0 or v in (1,2,14): continue
            if any(not(0<=x+dx<64 and 0<=y+dy<64) or m[y+dy,x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): o.append((x,y,L[v]))
    return o
print('open randen ronde 12:',len(openr(a)),'| ronde 13:',len(openr(b)),openr(b)[:10])
za=np.zeros((64,64),bool); za[30:41,40:50]=True
zb=np.zeros((64,64),bool); zb[48:63,2:31]=True
d=a!=b
print('gewijzigd zone A (achterwig):',int((d&za).sum()),'| zone B (armen/handen):',int((d&zb).sum()),'| buiten de zones:',int((d&~za&~zb).sum()))
def lone(m):
    r=[]
    for y in range(64):
        for x in range(64):
            v=m[y,x]
            if v and not any(m[y+dy,x+dx]==v for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and 0<=x+dx<64 and 0<=y+dy<64): r.append((x,y,L[v]))
    return r
la=set(lone(a)); lb=set(lone(b)); print('losse pixels nieuw:',sorted(lb-la),'| verdwenen:',sorted(la-lb))
im=Image.fromarray(b.astype(np.uint8),'P'); im.putpalette(src.getpalette()); im.save(os.path.join(H,'../nachtaap.png'),transparency=0)
pal=src.getpalette()[:48]
with open(os.path.join(H,'../normal.pal'),'w',newline='\r\n') as f: f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%tuple(pal[3*i:3*i+3]) for i in range(16)))
