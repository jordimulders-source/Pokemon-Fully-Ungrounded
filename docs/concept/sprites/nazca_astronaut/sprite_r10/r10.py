# r10: eigen patroon per deel. Romp = getrapte zigzag (romp.txt, hand); bovenarmen/dijen = optie A/B/C.
# Silhouet, kop, onderarmen/onderbenen en strepen = r9 (zelfde tuniekzone/tint uit sprite_r9/gen.py).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r9')
from gen import B, stuk, tint, H, W
from basis import KL
M0=np.full((H,W),'',dtype='<U1')
for l in open('romp.txt'):
    if l.startswith('#') or not l.strip(): continue
    y,xs,s=l.split(); x0=int(xs[1:])
    for i,c in enumerate(s):
        if c=='.': continue
        assert stuk[y:=int(y),x0+i]=='RO',(y,x0+i); M0[y,x0+i]=c
assert all(M0[y,x] for y in range(H) for x in range(W) if stuk[y,x]=='RO'), 'romp niet volledig'
def ledematen(opt):
    M=M0.copy()
    for y in range(H):
        for x in range(W):
            s=stuk[y,x]
            if s not in ('LA','RA','LL','RL'): continue
            m='g'
            if opt=='A':                       # ringbanden, 2 px, dwars op het ledemaat
                if s=='LA': m='ga'[((x-18)//2)%2]
                elif s=='RA': m='ga'[((y-31)//2)%2]
                else: m='ga'[((y-34)//2)%2]
            elif opt=='B':                     # lengtebaan: lichte streep over grond
                if s=='LA': m='a' if y==max(j for j in range(H) if stuk[j,x]=='LA') else 'g'
                elif s=='RA': m='a' if x==min(i for i in range(W) if stuk[y,i]=='RA') else 'g'
                elif s=='LL': m='a' if x==29 else 'g'
                else: m='a' if x==35 else 'g'
            elif opt=='C':                     # tocapu: 2x2 blokjes, om en om a en k, verspringend
                blok={'LL':{34:(29,30,'a'),38:(28,29,'k'),42:(29,30,'a'),46:(28,29,'k')},
                      'RL':{34:(34,35,'k'),38:(35,36,'a'),42:(34,35,'k'),46:(35,36,'a')}}
                if s in blok:
                    for y0,(xa,xb,c) in blok[s].items():
                        if y0<=y<=y0+1 and xa<=x<=xb: m=c
                elif s=='LA':
                    if (19<=x<=20 and 26<=y<=27): m='a'
                    if (24<=x<=25 and 28<=y<=29): m='k'
                elif s=='RA':
                    if 32<=y<=33: m='a'
                    if y>=35: m='k'
            M[y,x]=m
    return M
PAL={
 '1':(dict(g=('R','T','t'),a=('M','D','S'),k=('3','2','1'),sel='t'),{'T':(160,52,44),'t':(104,34,36)}),
 '3':(dict(g=('b','2','1'),a=('Y','y','S'),k=('L','M','D'),sel='2'),{'Y':(240,196,78),'y':(190,136,50)}),
}
def bouw(M,pal,extra):
    KL2=dict(KL); KL2.update(extra); R=B.copy()
    for y in range(H):
        for x in range(W):
            if stuk[y,x]: R[y,x]=pal[M[y,x]][tint[y,x]]
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K' or not any(stuk[a,b] for a,b in ((y,x+1),(y+1,x),(y,x-1),(y-1,x))): continue
            if (B[y,x-1]=='.' and stuk[y,x+1]) or (B[y-1,x]=='.' and stuk[y+1,x] and x<=31): R[y,x]=pal['sel']
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,(len(keys),keys)
    return R,KL2,keys
def schrijf(naam,R,KL2,keys):
    im=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[v for k in keys for v in KL2[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
if __name__=='__main__':
    for o in 'ABC':
        M=ledematen(o)
        for p,(pal,ex) in PAL.items():
            R,K2,keys=bouw(M,pal,ex); schrijf('astro_%s%s.png'%(o,p),R,K2,keys); print(o+p,len(keys),'kleuren')
        if '-v' in sys.argv:
            for y in range(26,48): print('  %2d '%y+''.join(M[y,x] if stuk[y,x] else ('#' if B[y,x]!='.' else ' ') for x in range(16,44)))
