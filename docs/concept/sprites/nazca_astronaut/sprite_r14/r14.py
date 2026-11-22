# r14: romp van r13-P_rood bevroren; alleen mouwen (bovenarmen) en shortspijpen (dijen) krijgen een eigen stof.
# Basis = r13-png (rollen terug via palet). Schoudernaden (LA x28, RA rij 31) horen bij de romp en blijven.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r9')
from gen import B, stuk, tint, H, W
from basis import KL
EX={'Q':(150,36,42),'Y':(240,196,78)}; KL2=dict(KL); KL2.update(EX); INV={v:k for k,v in KL2.items()}
im=Image.open('../sprite_r13/astro_P_rood.png'); pal=np.array(im.getpalette()[:48]).reshape(16,3)
R13=np.array([INV.get(tuple(c),'?') for c in pal])[np.asarray(im)]; assert '?' not in R13
CREME=set('LMDSBbRr')
def naad(y,x): return (stuk[y,x]=='LA' and x==28) or (stuk[y,x]=='RA' and y==31)
LEDE=np.array([[stuk[y,x] in ('LA','RA','LL','RL') and not naad(y,x) for x in range(W)] for y in range(H)])
def kol(s,x): return [j for j in range(H) if stuk[j,x]==s and LEDE[j,x]]
def rij(s,y): return [i for i in range(W) if stuk[y,i]==s and LEDE[y,i]]
def boord(y,x): return any(B[y+a,x+b] in CREME and not stuk[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
# --- motieven: geven per ledemaatpixel een materiaal: g grond, m motief, n tweede motiefkleur, o boord
def trapjes(s,y,x):        # getrapte zaagtandjes (driehoekje van 3 px), zoals r12
    if s in ('LL','RL'):
        r=rij(s,y); i=x-min(r); p=(y-35)%4 if y>=35 else 9
        return 'm' if (p==0 and i==0) or (p==1 and i<2) else 'g'
    if s=='LA':
        c=kol(s,x); j=y-min(c); n=len(c); p=(x-19)%4 if x<=26 else 9
        return 'm' if (p==0 and j==n-1) or (p==1 and j>=n-2) else 'g'
    r=rij(s,y); i=x-min(r); p=(y-32)%4                 # RA (rij 32-36)
    return 'm' if (p==0 and i==0) or (p==1) else 'g'
def blokjes(s,y,x):        # 2x2 getrapte blokjes, kleur wisselt m/n per herhaling
    BL={'LL':[(35,29,'m'),(39,28,'n'),(43,29,'m')],'RL':[(35,34,'n'),(39,35,'m'),(43,34,'n')],
        'LA':[(27,22,'m'),(28,25,'n')],'RA':[(33,38,'m')]}
    for y0,x0,c in BL[s]:
        if y0<=y<=y0+1 and x0<=x<=x0+1 and LEDE[y,x]: return c
    return 'g'
def dwars(s,y,x):          # 1 px goud, 2 px zwart, dwars op het ledemaat
    if s in ('LL','RL'): return 'm' if (y-35)%3==0 else 'g'
    if s=='LA': return 'm' if (x-19)%3==0 else 'g'
    return 'm' if (y-33)%3==0 else 'g'
O=[0,0,1,1,2,2,1,1]       # getrapte zigzag: positie per rij/kolom, 2 stappen per tree
def zigzag(s,y,x):
    if s in ('LL','RL'):
        r=rij(s,y); a=min(r); w=len(r)
        def pos(yy): return min(O[(yy-34)%8],w-1)
        return 'm' if x-a==pos(y) or (y>34 and x-a==pos(y-1) and pos(y)!=pos(y-1)) else 'g'
    if s=='LA':
        c=kol(s,x); n=len(c); j=y-min(c)
        def pos(xx): return min([0,1,1,0][(xx-18)%4],n-1)
        return 'm' if j==pos(x) or (x>18 and j==pos(x-1) and pos(x)!=pos(x-1)) else 'g'
    r=rij(s,y); i=x-min(r); return 'm' if i==[0,0,1,1][(y-32)%4] else 'g'
def S5(s,y,x): return trapjes(s,y,x)
VAR={  # motief, kleuren per deel ('arm','been'): materiaal -> (licht, midden, schaduw), selout
 'S1':(trapjes,{'arm':dict(g=('B','B','b'),m=('Y','Y','Y'),o=('Y','Y','D'),sel='b')}),
 'S2':(blokjes,{'arm':dict(g=('Y','Y','D'),m=('R','R','Q'),n=('1','1','1'),o=('Q','Q','Q'),sel='D')}),
 'S3':(dwars,  {'arm':dict(g=('3','2','1'),m=('Y','Y','Y'),o=('Y','Y','D'),sel='1')}),
 'S4':(zigzag, {'arm':dict(g=('L','M','D'),m=('R','R','Q'),o=('Q','Q','Q'),sel='S')}),
 'S5':(S5,     {'arm':dict(g=('Y','Y','D'),m=('1','1','1'),o=('1','1','1'),sel='D'),
                'been':dict(g=('B','B','b'),m=('W','W','L'),o=('W','W','L'),sel='b')}),
}
def bouw(v):
    f,kl=VAR[v]; R=R13.copy()
    for y in range(H):
        for x in range(W):
            if not LEDE[y,x]: continue
            s=stuk[y,x]; p=kl.get('been' if s in ('LL','RL') else 'arm',kl['arm'])
            m='o' if boord(y,x) else f(s,y,x)
            R[y,x]=p[m][tint[y,x]]
    # selout lichtkant: alleen buitenlijnpixels die uitsluitend aan ledemaat (niet aan romp) grenzen
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K': continue
            nb=[(y,x+1),(y+1,x),(y,x-1),(y-1,x)]
            if any(stuk[a,b]=='RO' or (stuk[a,b] and not LEDE[a,b]) for a,b in nb): continue
            for a,b in ((y,x+1),(y+1,x)):
                if LEDE[a,b] and ((b==x+1 and B[y,x-1]=='.') or (a==y+1 and B[y-1,x]=='.' and x<=31)):
                    s=stuk[a,b]; R[y,x]=kl.get('been' if s in ('LL','RL') else 'arm',kl['arm'])['sel']; break
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,(v,keys)
    out=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; out.putpalette(flat+[0]*(768-len(flat))); out.save('astro_%s.png'%v,transparency=0)
    return R,keys
if __name__=='__main__':
    for v in VAR:
        R,k=bouw(v); print(v,len(k),'kleuren')
