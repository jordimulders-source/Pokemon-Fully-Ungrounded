# Ronde 9: manen links kleiner (onderrand aan de borstkant N px hoger); vrijgekomen deel = borst/hals uit model A3.
import numpy as np, r8lib as L, r8
from PIL import Image
from scipy import ndimage as nd
Am=np.asarray(Image.open('r3/model_A3.png').convert('RGB')).astype(int)
R_,G_,B_=Am[...,0],Am[...,1],Am[...,2]; lum=Am@[.299,.587,.114]
LIJN=lum<70; MHAAR=(B_<R_*0.31)&(R_>=110)&~LIJN&(lum<200); MVACHT=(~MHAAR)&~LIJN&(lum<200)&(R_-B_>60)
SHIFT=lum[MVACHT].mean()-lum[MHAAR].mean()   # haar -> vacht: zelfde helderheidsverloop, tinten van het lijf
x0,p=91,16
CEL=np.zeros((L.H,L.W)); CN=np.zeros((L.H,L.W))
for y in range(L.H):
    for x in range(L.W):
        s=(slice(y*p,(y+1)*p),slice(x0+x*p,x0+(x+1)*p)); m=(MHAAR|MVACHT)[s]
        if m.sum()>20:
            v=lum[s][m].astype(float); v=np.where(MHAAR[s][m],v+SHIFT,v); CEL[y,x]=v.mean(); CN[y,x]=1
# volume op lijfschaal: modelhelderheid over ±1 cel (de strengen van het haar zijn geen lijfvolume)
GL=nd.gaussian_filter(CEL,1.2)/np.maximum(nd.gaussian_filter(CN,1.2),1e-6)
def lijftoon(x,y): l=GL[y,x]; return 'L' if l>=181 else 'M' if l>=160 else 'D'
def snede(N):
    """onderrand van de manen aan de borstkant: lijn door (12, 44-N) en (24, 42); alles eronder (x<=24) komt vrij"""
    def b(x): return 44-N+(42-(44-N))*(x-12)/12.0
    return {(x,y) for x,y in L.HAAR if x<=24 and y>b(x)}

def diep0(mask,x,y):
    k=0
    while all((x+a,y+b) in mask for a in range(-k,k+1) for b in range(-k,k+1)): k+=1
    return k
class Vorm9(L.Vorm):
    def __init__(s,N):
        super().__init__(); s.N=N; s.vrij=snede(N); s.mask-=s.vrij; s.mask0=set(s.mask)
    def rand(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label='rand',diepte=1):
        sn=L.snip(naam,x0,y0,x1,y1,flip); h,w=len(sn),len(sn[0]); ext=set()
        st=[(i,j) for j in range(h) for i in (0,w-1)]+[(i,j) for i in range(w) for j in (0,h-1)]
        while st:
            i,j=st.pop()
            if not(0<=i<w and 0<=j<h) or (i,j) in ext or sn[j][i]!='.': continue
            ext.add((i,j)); st+=[(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        for j,row in enumerate(sn):
            for i,c in enumerate(row):
                t=(dx+i,dy+j); sx=x0+((w-1-i) if flip else i); sy=y0+j
                if t not in L.ZONE or c=='#': continue
                if c=='.':
                    if (i,j) in ext and t in s.mask0 and diep0(s.mask0,*t)<=diepte: s.mask.discard(t); s.weg.add(t)
                    continue
                R=L.R6[t[1]][t[0]]
                if t not in L.HAAR and not (R in '.0' or (R=='M' and t not in L.HALS)): continue
                if t in s.vrij and not any((t[0]+a,t[1]+b) in s.mask0 for a in(-1,0,1) for b in(-1,0,1)) and diepte<9:
                    pass
                s.mask.add(t); s.weg.discard(t)
                if c in 'lm': s.kleur[t]=c
                s.bron[t]=(label,naam,sx,sy,c)
    def maak(s,slagschaduw=True):
        g=[r[:] for r in L.R6]; H,W=len(g),len(g[0])
        changed=True
        while changed:
            changed=False
            for p in list(s.weg):
                x,y=p
                if all((x+a,y+b) in s.mask for a,b in((1,0),(-1,0),(0,1),(0,-1))): s.mask.add(p); s.weg.discard(p); changed=True
        lijf=set()
        for x,y in L.HAAR:
            if (x,y) in s.mask: continue
            if (x,y) in s.vrij: g[y][x]='F'; lijf.add((x,y))
            else: g[y][x]='~'
        seen=set(); st=[(0,y) for y in range(H)]+[(x,0) for x in range(W)]
        while st:
            x,y=st.pop()
            if not(0<=x<W and 0<=y<H) or (x,y) in seen or g[y][x] not in '.~': continue
            seen.add((x,y)); st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for _ in range(3):
            for y in range(H):
                for x in range(W):
                    if g[y][x]=='~':
                        if (x,y) in seen: g[y][x]='.'; s.bron[(x,y)]=('achtergrond (rand gerafeld)',)
                        else:
                            nb=[g[y+b][x+a] for a,b in((1,0),(-1,0),(0,1),(0,-1)) if g[y+b][x+a] in 'MDL']
                            if nb: g[y][x]=max(set(nb),key=nb.count); s.bron[(x,y)]=('lijf zichtbaar (rand gerafeld)',)
        for y in range(H):
            for x in range(W):
                if g[y][x]=='~': s.mask.add((x,y))
        # vrijgekomen: borst/hals in lijftinten uit de modelhelderheid; aan de buitenrand de buitenlijn 0
        vals=sorted(GL[y,x] for x,y in lijf); n=len(vals)
        tL=vals[int(n*0.75)] if n else 999; tD=vals[int(n*0.25)] if n else 0
        for x,y in lijf:
            l=GL[y,x]; g[y][x]='L' if l>=tL else 'M'; s.bron[(x,y)]=('borst: lijftint uit modelhelderheid (lichtste 25% L, rest M)',)
        for x,y in lijf:
            if any(g[y+b][x+a]=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1))): g[y][x]='0'; s.bron[(x,y)]=('borst: buitenlijn',)
        vol=[q for q in s.mask if q in s.kleur]
        for q in s.mask:
            x,y=q
            if q in s.kleur: c=s.kleur[q]
            else:
                r=min(vol,key=lambda v:(v[0]-x)**2+(v[1]-y)**2); c=s.kleur[r]; s.bron.setdefault(q,('veld-herhaald',)+tuple(s.bron[r][1:]))
            g[y][x]=c
        for x,y in s.mask:
            buren=[(a,b) for a,b in((-1,0),(0,-1),(1,0),(0,1)) if (x+a,y+b) not in s.mask and ((x+a,y+b) in lijf or g[y+b][x+a] not in '0DKd')]
            if not buren: continue
            g[y][x]='0' if any(a>0 or b>0 for a,b in buren) else 'd'
            s.bron.setdefault((x,y),('omtrek',))
        # netheid: lichte tintvlakjes < 3 px in de borst -> M
        from scipy import ndimage as _nd
        import numpy as _np
        A=_np.zeros((H,W),bool)
        for x,y in lijf:
            if g[y][x]=='L': A[y,x]=True
        lab,n=_nd.label(A)
        for k in range(1,n+1):
            if (lab==k).sum()<3:
                for y,x in _np.argwhere(lab==k): g[y][x]='M'; s.bron[(x,y)]=('borst: M (L-vlakje < 3 px)',)
        # slagschaduw van de manen op de borst (Arcanine: lijf direct onder/naast de kraag donker): 1 px onder de manenrand
        for x,y in lijf:
            if g[y][x] in 'LM' and any((x+a,y-1) in s.mask for a in (-1,0,1)): g[y][x]='D'; s.bron[(x,y)]=('borst: slagschaduw onder de manen',)
        if slagschaduw:
            for x,y in L.ZONE:
                if g[y][x]=='M' and (x,y) not in L.HALS and (x,y) not in lijf and (x-1,y) in s.mask and g[y][x-1]=='0': g[y][x]='D'; s.bron[(x,y)]=('slagschaduw op lijf',)
        s.lijf=lijf
        return [''.join(r) for r in g]
