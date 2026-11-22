# r12: Paracas-doek als t-shirt + shorts. Borst: groot Paracas-gezicht (romp.txt, hand). Mouwen/shorts: 2x2-blokjes
# waarvan de kleur per herhaling wisselt (diagonaal ritme), boord van 1 rij waar de stof de creme ledematen raakt.
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
CREME=set('LMDSBbRr')
# mouwen/shorts: getrapte zaagtandjes (goud driehoekje met zwarte schuine kant), herhaald; boord (o) waar de stof creme raakt
def kol(s,x): return [j for j in range(H) if stuk[j,x]==s]
def rij(s,y): return [i for i in range(W) if stuk[y,i]==s]
for y in range(H):
    for x in range(W):
        s=stuk[y,x]
        if s in ('RO',''): continue
        m='g'
        if s in ('LL','RL'):
            r=rij(s,y); i=x-min(r); p=(y-35)%4 if y>=35 else 9
            if p==0: m='yk'[i] if i<2 else 'g'
            elif p==1: m='yyk'[i] if i<3 else 'g'
        elif s=='LA':
            c=kol(s,x); j=y-min(c); n=len(c); p=(x-19)%4 if x<=26 else 9   # schouder (x27-28) grond: los van het linkeroog
            if p==0: m='y' if j==n-1 else 'g'
            elif p==1: m='y' if j>=n-2 else 'g'
            elif p==2: m='k' if j==n-1 else 'g'
        elif s=='RA':
            r=rij(s,y); i=x-min(r); p=(y-31)%4
            if p==1: m='y' if i==0 else 'g'
            elif p==2: m='y' if i==0 else 'k'
        if any(B[y+a,x+b] in CREME and not stuk[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1))): m='o'
        M[y,x]=m
VAR={  # materiaal -> (licht, midden, schaduw); sel = selout lichtkant
 'P_rood': (dict(g=('R','Q','Q'),y=('Y','Y','Y'),k=('1','1','1'),o=('Y','Y','D')),'Q',{'Q':(150,36,42),'Y':(240,196,78)}),
 'P_blauw':(dict(g=('b','N','N'),y=('Y','Y','Y'),k=('1','1','1'),o=('Y','Y','D')),'N',{'N':(30,38,96),'Y':(240,196,78)}),
 'P_zwart':(dict(g=('3','2','1'),y=('Y','Y','Y'),k=('R','R','R'),o=('Y','Y','D')),'1',{'Y':(240,196,78)}),
}
def bouw(v):
    pal,sel,ex=VAR[v]; KL2=dict(KL); KL2.update(ex); R=B.copy()
    for y in range(H):
        for x in range(W):
            if stuk[y,x]: R[y,x]=pal[M[y,x]][tint[y,x]]
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K': continue
            if (B[y,x-1]=='.' and stuk[y,x+1]) or (B[y-1,x]=='.' and stuk[y+1,x] and x<=31): R[y,x]=sel
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,(v,len(keys),keys)
    im=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save('astro_%s.png'%v,transparency=0)
    return keys
if __name__=='__main__':
    for v in VAR: k=bouw(v); print(v,len(k),'kleuren:',' '.join(k[1:]))
    for y in range(25,49): print('  %2d '%y+''.join(M[y,x] if stuk[y,x] else ('#' if B[y,x]!='.' else ' ') for x in range(16,44)))
