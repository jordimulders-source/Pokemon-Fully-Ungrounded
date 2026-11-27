# Ronde 3 vanaf ../sprite_bijl_r2/oog_B.png (oog B + silhouet bevroren).
# Stap 1 poten, stap 2 schaduw/tinten hele sprite: tint per pixel uit de modelhelderheid (cel-gemiddelde, licht gladgestreken
# binnen de eigen kleurgroep zodat grenzen gebogen lopen), drempels per groep uit de modeltonen; lijnen/buitenlijn/oog blijven.
import numpy as np; from PIL import Image
import lib1 as l
B0=Image.open('../sprite_bijl_r2/oog_B.png'); B=np.array(B0).astype(int); S=B.copy()
PAL=[tuple(B0.getpalette()[i*3:i*3+3]) for i in range(16)]
V8=np.array(Image.open('../swaps_r1/v8.png')).astype(int)
FIG=B>0
GROEP={1:1,2:0,3:2,4:2,5:2,6:3,7:3,8:3,9:4,10:4,11:4,12:4,13:5,14:5,15:5}
def g(i): return GROEP.get(int(i),0)
OOG={(x+(-8),y+7) for x,y in [(25,22),(26,22),(22,23),(23,23),(24,23),(25,23),(26,23),(23,24),(24,24),(25,24),(26,24),(24,25),(25,25)]}
OOG={(y,x) for x,y in OOG}
def leeg(y,x): return not(0<=y<64 and 0<=x<64) or not FIG[y,x]
RAND={(y,x) for y in range(64) for x in range(64) if FIG[y,x] and any(leeg(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)))}
LIJN={(y,x) for y in range(64) for x in range(64) if V8[y,x]==1 and (y,x) not in RAND}   # binnenlijnen (model-zwart) uit r1/r2
LOG=[]
def zet(y,x,v,stap):
    if (y,x) in OOG or not FIG[y,x]: raise SystemExit('bevroren pixel %s'%((y,x),))
    if S[y,x]!=v: LOG.append((stap,y,x,int(S[y,x]),int(v))); S[y,x]=v
def zone(y,x):
    if x<=13 or (x<=15 and y>=31): return 'snavel'
    if x<=26 and y<=36: return 'kop'
    if g(B[y,x])==5 or (g(B[y,x])==1 and any(0<=y+a<64 and 0<=x+b<64 and g(B[y+a,x+b])==5 for a in(-1,0,1) for b in(-1,0,1))):
        return 'poot rechts' if x>=44 else 'poot links'
    return 'lijf'

# palet: tinten in de richting van v8, schaduw koeler/verzadigder, licht warmer; stappen ±30-40
PAL[3]=(60,57,58);  PAL[4]=(104,97,89);  PAL[5]=(182,170,150)      # snavel steen
PAL[6]=(50,52,62);  PAL[7]=(86,84,90);   PAL[8]=(128,120,114)      # lijf antraciet
PAL[13]=(86,72,62); PAL[14]=(146,126,100); PAL[15]=(204,176,136)   # poten beige

# modelhelderheid per spritepixel: gemiddelde, p15 en max van de niet-zwarte modelpixels in de cel (px.py-maten)
SUB=4
cel={}
for j in range(l.H*SUB):
    Y=int(np.floor(l.OY+((j+0.5)/SUB-l.Y0)*l.S))
    if not 0<=Y<64: continue
    ny=j//SUB
    for i in range(l.W*SUB):
        X=int(np.floor(l.OX+((i+0.5)/SUB-l.X0)*l.S))
        if not 0<=X<64: continue
        nx=i//SUB
        if not l.FIG[ny,nx]: continue
        cel.setdefault((Y,X),[]).append(l.L[ny,nx])
GEM=np.full((64,64),np.nan); P15=np.full((64,64),np.nan); MAXL=np.full((64,64),np.nan)
for (y,x),v in cel.items():
    v=np.array(v); w=v[v>=40]
    if len(w)==0: continue
    GEM[y,x]=w.mean(); P15[y,x]=np.percentile(w,15); MAXL[y,x]=w.max()

def glad(mask,T,sig=0.8):
    """gewogen gemiddelde binnen dezelfde groep (gebogen grenzen i.p.v. modelveelhoeken)"""
    out=T.copy(); r=2
    for y,x in zip(*np.where(mask)):
        s=w=0.0
        for a in range(-r,r+1):
            for b in range(-r,r+1):
                yy,xx=y+a,x+b
                if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and not np.isnan(T[yy,xx]):
                    k=np.exp(-(a*a+b*b)/(2*sig*sig)); s+=k*T[yy,xx]; w+=k
        if w: out[y,x]=s/w
    return out
VUL=lambda y,x: FIG[y,x] and (y,x) not in RAND and (y,x) not in LIJN and (y,x) not in OOG
PAL[15]=(196,170,132)   # één lichte pootint voor hooglicht op de poot en de tenen (palet vol, geen index vrij)

def stap_poten():
    M=np.array([[VUL(y,x) and g(B[y,x])==5 for x in range(64)] for y in range(64)])
    for y,x in zip(*np.where(M)):
        t=GEM[y,x]
        if np.isnan(t): continue
        ver=x>=44                                   # verre (rechter) poot als geheel donkerder
        t2=t-6 if ver else t
        if t2<98 or (P15[y,x]<62 and t2<118): v=13              # schaduwkant / schubring / gewricht (gemeten donker)
        elif t2>=128: v=15
        else: v=14
        zet(y,x,v,'poten')
DREMPEL={2:(80,125,(3,4,5)),3:(88,120,(6,7,8))}
def stap_tinten():
    for gr,(d1,d2,(a,b,c)) in DREMPEL.items():
        M=np.array([[VUL(y,x) and g(B[y,x])==gr for x in range(64)] for y in range(64)])
        T=GEM   # geen gladstrijken: modellijnen (veerstreepjes) blijven
        for y,x in zip(*np.where(M)):
            t=T[y,x]
            if np.isnan(t): continue
            zet(y,x,a if t<d1 else (c if t>=d2 else b),'tinten')
    # kuif/kop: tan (11) en donker roodbruin (9) volgen de modelhelderheid; rood en oranje blijven (kleur, geen schaduw)
    M=np.array([[VUL(y,x) and B[y,x] in (9,11) for x in range(64)] for y in range(64)])
    T=GEM
    for y,x in zip(*np.where(M)):
        if not np.isnan(T[y,x]): zet(y,x,9 if T[y,x]<92 else 11,'tinten')
def opruimen():
    """tintvlakjes < 3 px (vulpixels) -> meest voorkomende buurtint van dezelfde groep (lijnen, rand, oog blijven)"""
    for _ in range(3):
        for idx in (3,4,5,6,7,8,9,11,14,15):
            if False: pass
            seen=set()
            for y0,x0 in zip(*np.where(S==idx)):
                if (y0,x0) in seen: continue
                comp=[(y0,x0)]; st=[(y0,x0)]; seen.add((y0,x0))
                while st:
                    y,x=st.pop()
                    for a,b in((-1,0),(1,0),(0,-1),(0,1)):
                        q=(y+a,x+b)
                        if 0<=q[0]<64 and 0<=q[1]<64 and S[q]==idx and q not in seen: seen.add(q); comp.append(q); st.append(q)
                if len(comp)>=3: continue
                if idx in (3,6,9) and len(comp)==2: continue   # 2-px streepje in de donkerste tint = modellijn (veer), blijft
                for y,x in comp:
                    if not VUL(y,x): continue
                    c={}
                    for a,b in((-1,0),(1,0),(0,-1),(0,1)):
                        yy,xx=y+a,x+b
                        if 0<=yy<64 and 0<=xx<64 and S[yy,xx]>1 and S[yy,xx]!=idx and g(S[yy,xx])==g(idx) and VUL(yy,xx): c[S[yy,xx]]=c.get(S[yy,xx],0)+1
                    if c: zet(y,x,max(c,key=c.get),'opruimen')
def opslaan(pad,A=None):
    A=S if A is None else A
    im=Image.fromarray(A.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0)
if __name__=='__main__':
    stap_poten(); opslaan('alleen_poten.png'); P1=S.copy()
    stap_tinten(); opruimen()
    np.save('r3.npy',S); opslaan('terreurvogel_bijl_r3.png')
    from collections import Counter
    print(sorted(Counter((s,zone(y,x)) for s,y,x,a,b in LOG).items()))
    print('afwijkend t.o.v. r2/oog_B per zone:',dict(Counter(zone(y,x) for y,x in zip(*np.where(S!=B)))))
    print('alpha-diff',int(((S>0)!=FIG).sum()),'oog gewijzigd',sum(S[p]!=B[p] for p in OOG))
