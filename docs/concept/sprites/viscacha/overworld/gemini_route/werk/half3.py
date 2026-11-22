# natief -> 2x2: masker (>=2 van 4 niet-achtergrond), buitenrand = omlijning, binnen = meerderheidskleur;
# binnenlijnen uit het model (>=2 donker in blok) blijven 'o'. Niets getekend.
import sys, numpy as np
from half import labels, M
def half3(lab,oy,ox):
    H,W=lab.shape; h=(H-oy)//2; w=(W-ox)//2
    msk=np.zeros((h,w),bool); col=np.full((h,w),'.',dtype='<U1')
    for j in range(h):
        for i in range(w):
            b=lab[oy+2*j:oy+2*j+2, ox+2*i:ox+2*i+2].ravel()
            nb=(b=='.').sum(); nd=(b=='#').sum()
            if nb>=3: continue
            msk[j,i]=True
            rest=[x for x in b if x not in '.#']
            if nd>=2 or not rest: col[j,i]='o'
            else:
                vals,cnt=np.unique(rest,return_counts=True); col[j,i]=M[vals[cnt.argmax()]]
    out=col.copy()
    for j in range(h):
        for i in range(w):
            if not msk[j,i]: continue
            for y,x in ((j-1,i),(j+1,i),(j,i-1),(j,i+1)):
                if not(0<=y<h and 0<=x<w) or not msk[y,x]: out[j,i]='o'; break
    g=[''.join(r) for r in out]
    rows=[i for i,r in enumerate(g) if r.strip('.')]; g=g[rows[0]:rows[-1]+1]
    cols=[i for i in range(len(g[0])) if any(r[i]!='.' for r in g)]
    return [r[cols[0]:cols[-1]+1] for r in g]
if __name__=='__main__':
    n=sys.argv[1]; lab=labels(n)
    for oy in (0,1):
        for ox in (0,1):
            g=half3(lab,oy,ox); open(f'h3_{n}_{oy}{ox}.txt','w').write('\n'.join(g)+'\n'); print(n,oy,ox,len(g[0]),len(g))
