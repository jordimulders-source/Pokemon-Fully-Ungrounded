# r11: eigen patroon EN eigen kleur per deel. Kraag / romp (getrapte zigzag, romp.txt) / bovenarmen / dijen
# (tocapu-blokjes 2x2 verspringend, zoals r10-C). Zones en tint per kolom uit sprite_r9/gen.py.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r9')
from gen import B, stuk, tint, H, W
from basis import KL
M=np.full((H,W),'',dtype='<U1')
for l in open('romp.txt'):
    if l.startswith('#') or not l.strip(): continue
    y,xs,s=l.split(); y=int(y); x0=int(xs[1:])
    for i,c in enumerate(s):
        if c!='.': assert stuk[y,x0+i]=='RO',(y,x0+i); M[y,x0+i]=c
assert all(M[y,x] for y in range(H) for x in range(W) if stuk[y,x]=='RO')
# blokjes 2x2, verspringend, met 1 rij grond tot de romp en 3 rijen grond tot de creme knie
BLOK={'LL':[(35,29,30),(39,28,29),(43,29,30)],'RL':[(35,34,35),(39,35,36),(43,34,35)]}
for y in range(H):
    for x in range(W):
        s=stuk[y,x]
        if s in ('LL','RL'): M[y,x]='x' if any(y0<=y<=y0+1 and a<=x<=b for y0,a,b in BLOK[s]) else 'g'
        elif s=='LA': M[y,x]='x' if (22<=x<=23 and 27<=y<=28) or (26<=x<=27 and 28<=y<=29) else 'g'   # weg van de creme elleboog
        elif s=='RA': M[y,x]='x' if 32<=y<=33 else 'g'   # rij 35-36 grond: weg van de creme onderarm
def deel(y,x):
    s=stuk[y,x]
    if s=='RO': return 'kraag' if M[y,x]=='c' else 'romp'
    return {'LA':'arm','RA':'arm','LL':'dij','RL':'dij'}[s]
# per variant: kleur per (deel, materiaal) als (licht, midden, schaduw) + selout per deel
VAR={
 'K1':({'kraag':{'c':('Y','Y','D')},'romp':{'g':('3','2','1'),'a':('W','W','L'),'k':('W','W','L')},
        'arm':{'g':('R','R','r'),'x':('L','M','M')},'dij':{'g':('B','B','b'),'x':('L','M','M')}},
       {'kraag':'D','romp':'1','arm':'r','dij':'b'},{'Y':(240,196,78),'r':(140,36,40)}),
 'K2':({'kraag':{'c':('Y','Y','D')},'romp':{'g':('R','T','T'),'a':('L','M','D'),'k':('3','2','1')},
        'arm':{'g':('b','2','1'),'x':('Y','Y','D')},'dij':{'g':('Y','D','S'),'x':('3','3','2')}},
       {'kraag':'D','romp':'T','arm':'2','dij':'S'},{'Y':(240,196,78),'T':(150,50,42)}),
 'K3':({'kraag':{'c':('R','R','T')},'romp':{'g':('b','2','1'),'a':('Y','Y','D'),'k':('Y','Y','D')},
        'arm':{'g':('Y','Y','D'),'x':('b','b','2')},'dij':{'g':('T','T','S'),'x':('L','M','M')}},
       {'kraag':'K','romp':'2','arm':'D','dij':'S'},{'Y':(240,196,78),'T':(186,84,52)}),
}
def bouw(v):
    pal,sel,ex=VAR[v]; KL2=dict(KL); KL2.update(ex); R=B.copy()
    for y in range(H):
        for x in range(W):
            if stuk[y,x]: R[y,x]=pal[deel(y,x)][M[y,x]][tint[y,x]]
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K': continue
            if B[y,x-1]=='.' and stuk[y,x+1]: R[y,x]=sel[deel(y,x+1)]
            elif B[y-1,x]=='.' and stuk[y+1,x] and x<=31: R[y,x]=sel[deel(y+1,x)]
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,(v,len(keys),keys)
    im=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save('astro_%s.png'%v,transparency=0)
    return keys
if __name__=='__main__':
    for v in VAR: k=bouw(v); print(v,len(k),'kleuren:',' '.join(k[1:]))
