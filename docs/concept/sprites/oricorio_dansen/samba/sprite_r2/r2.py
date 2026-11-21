# r2 vanaf r1 (r1_kls.npy). Jordi 21 nov: "Samba is de waaier erg druk en gekarteld, misschien een aantal veren wat meer geel maken.
# De kuif onderscheidt zich nog niet voldoende en de vleugels lijken nu 2 losse vleugels achter elkaar".
# Lijf, kop, oog, snavel (Pom-Pom) en poten = beschermd (pixeldiff 0, gecontroleerd onderaan).
import sys, json, numpy as np
from collections import Counter
from palet import I, NAMEN
GEEL=sys.argv[1] if len(sys.argv)>1 else 'A'
o=np.load('r1_kls.npy').copy(); H,W=o.shape; r1=o.copy(); log={}
LINE={I['O'],I['L']}; LICHT={I['G1'],I['G2'],I['G3']}; DONKER={I['G4'],I['G5']}; GEELS={I['Y1'],I['Y2']}
PINK={I['K0'],I['K1'],I['K2'],I['K3']}
# --- beschermd: lijf/kop/oog/snavel/gele kraag achter de kop (x 19-34 vanaf rij 22), lijf onder de vleugel (x 35-40 vanaf rij 36), poten (rij >= 47)
P=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if y>=47 or (19<=x<=34 and y>=22) or (35<=x<=40 and y>=36) or o[y,x] in PINK: P[y,x]=True
P&=(o>0)
# --- zones (alleen buiten P): W vleugel (lichte vulling links x<=18 r<=37, rechts x>=35 r<=35), C kuif (x 23-33, r 9-21, licht of geel), F waaier (rest)
Z=np.full((H,W),'',object)
for y in range(H):
    for x in range(W):
        if P[y,x] or o[y,x]==0: continue
        v=o[y,x]
        if 23<=x<=33 and 9<=y<=21 and (v in LICHT or v in GEELS): Z[y,x]='C'
        elif v in LICHT and ((x<=18 and y<=37) or (x>=35 and y<=35)): Z[y,x]='W'
        elif v in LINE: Z[y,x]='-'
        else: Z[y,x]='F'
# lijnpixels krijgen de zone van de meerderheid van hun vulburen (lijnen tussen twee zones -> later grens)
def nb8(y,x):
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W: yield y+dy,x+dx
# --- 1. zones gladmaken: modusfilter 3x3 over de zonekaart (lijnen tellen niet mee), 3 rondes; kuif en vleugel worden aaneengesloten vlakken
for it in range(3):
    Z2=Z.copy()
    for y in range(H):
        for x in range(W):
            if Z[y,x] in ('','-'): continue
            c=Counter(Z[yy,xx] for yy,xx in nb8(y,x) if Z[yy,xx] not in ('','-'))
            c[Z[y,x]]+=1
            Z2[y,x]=c.most_common(1)[0][0]
    Z=Z2
for y in range(H):
    for x in range(W):
        if Z[y,x]=='-':
            c=Counter(Z[yy,xx] for yy,xx in nb8(y,x) if Z[yy,xx] not in ('','-'))
            Z[y,x]=c.most_common(1)[0][0] if c else 'F'
np.save('zones.npy',Z.astype(str))
log['zones']={k:int((Z==k).sum()) for k in 'WCF'}
# --- 2. tinten per zone: vleugel G1/G2/G3, kuif G1/G2 + geel, waaier G4/G5 (+ geel). Eerst de r1-tint naar de zonereeks, dan modusfilter 3x3 (grote vlakken)
def naar(z,v,y,x):
    if z=='W': return v if v in LICHT else I['G3']
    if z=='C': return v if v in (I['G1'],I['G2'],I['Y1']) else (I['Y1'] if v in GEELS else I['G2'])
    if z=='F':
        if v in GEELS: return I['Y1'] if v==I['Y1'] else I['Y2']
        return v if v in DONKER else (I['G4'] if v in LICHT else I['G5'])
fil=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if Z[y,x] in ('W','C','F'): fil[y,x]=naar(Z[y,x],o[y,x] if o[y,x] not in LINE else -1,y,x)
for it in range(2):
    f2=fil.copy()
    for y in range(H):
        for x in range(W):
            if not fil[y,x]: continue
            c=Counter(fil[yy,xx] for yy,xx in nb8(y,x) if Z[yy,xx]==Z[y,x] and fil[yy,xx])
            c[fil[y,x]]+=2
            f2[y,x]=c.most_common(1)[0][0]
    fil=f2
# --- 3. binnenlijnen: r1-lijnen binnen dezelfde zone (veerscheidingen) als donkergroene lijn L; fragmenten < 4 px weg
lin=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if Z[y,x] in ('W','F','C') and r1[y,x] in LINE: lin[y,x]=True
def comps(mask):
    seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for yy,xx in nb8(a,b):
                        if mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(pts)
    return out
n=0
for pts in comps(lin):
    if len(pts)<4:
        for a,b in pts: lin[a,b]=False; n+=1
log['3_lijnfragmenten_weg']=n
# --- 4. opbouwen: vulling + binnenlijnen L + zonegrenzen L (vleugel/kuif vóór de waaier: de grenslijn ligt op de waaierkant)
out=np.where(P,o,0)
for y in range(H):
    for x in range(W):
        if Z[y,x] in ('W','C','F'): out[y,x]=I['L'] if lin[y,x] else fil[y,x]
n=0
for y in range(H):
    for x in range(W):
        if Z[y,x]!='F': continue
        if any(Z[yy,xx] in ('W','C') for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=yy<H and 0<=xx<W): out[y,x]=I['L']; n+=1
log['4_grenslijn_vleugel_kuif']=n
# grens waaier/vleugel tegen het beschermde lijf: daar staat in r1 al de lijfomlijning (blijft)
# --- 5. silhouet gladmaken (alleen buiten P): uitsteeksels (<=1 dekkende 4-buur) weg, inkepingen (>=3 dekkende 4-buren) dicht
def nb4(y,x): return [(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1))]
def op(y,x): return 0<=y<H and 0<=x<W and out[y,x]>0
n1=n2=0
for it in range(3):
    for y in range(H):
        for x in range(W):
            if P[y,x] if (0<=y<H and 0<=x<W) else True: continue
            k=sum(op(a,b) for a,b in nb4(y,x))
            if out[y,x] and k<=1: out[y,x]=0; Z[y,x]=''; n1+=1
            elif not out[y,x] and k>=3:
                c=Counter(Z[a,b] for a,b in nb4(y,x) if op(a,b) and Z[a,b] in('W','C','F'))
                if c: Z[y,x]=c.most_common(1)[0][0]; out[y,x]=I['G5'] if Z[y,x]=='F' else I['G3']; n2+=1
log['5_uitsteeksels_weg']=n1; log['5_inkepingen_dicht']=n2
np.save('r2_pre.npy',out); np.save('zones.npy',Z.astype(str)); np.save('P.npy',P)
# --- 6. buitenrand: dekkende pixel buiten P naast transparant -> zwart; lichtkant (transparant boven/links, niet onder/rechts) -> selout L (groen) / Y2 (geel)
n=0; B0=[]
for y in range(H):
    for x in range(W):
        if P[y,x] or not out[y,x]: continue
        if any(not op(a,b) for a,b in nb4(y,x)): B0.append((y,x))
B=np.zeros((H,W),bool)
for y,x in B0: B[y,x]=True; out[y,x]=I['O']; n+=1
ns=0
for y in range(H):
    for x in range(W):
        if not B[y,x]: continue
        up=not op(y-1,x); lf=not op(y,x-1); dn=not op(y+1,x); rt=not op(y,x+1)
        if (up or lf) and not (dn or rt):
            inn=[out[a,b] for a,b in ((y+1,x),(y,x+1)) if op(a,b) and out[a,b] not in LINE]
            out[y,x]=I['Y2'] if inn and inn[0] in GEELS else I['L']; ns+=1
log['6_buitenrand']=n; log['6_selout']=ns
# --- 7. binnenlijnen dun (Zhang-Suen op de L-lijnen binnen de zones; buitenrand en P blijven)
m=(out==I['L'])&~P&~B
def nbv(mm,y,x): return [mm[y-1,x],mm[y-1,x+1],mm[y,x+1],mm[y+1,x+1],mm[y+1,x],mm[y+1,x-1],mm[y,x-1],mm[y-1,x-1]]
weg=[]; ch=True
while ch:
    ch=False
    for step in (0,1):
        rm=[]
        for y in range(1,H-1):
            for x in range(1,W-1):
                if not m[y,x]: continue
                Pp=[mm for mm in nbv(m|B|((out>0)&np.isin(out,list(LINE))),y,x)]
                Bc=sum(Pp); A=sum((not Pp[i]) and Pp[(i+1)%8] for i in range(8))
                if not(2<=Bc<=6 and A==1): continue
                if step==0 and (Pp[0] and Pp[2] and Pp[4] or Pp[2] and Pp[4] and Pp[6]): continue
                if step==1 and (Pp[0] and Pp[2] and Pp[6] or Pp[0] and Pp[4] and Pp[6]): continue
                rm.append((y,x))
        for y,x in rm: m[y,x]=False; out[y,x]=-2; weg.append((y,x)); ch=True
for it in range(4):
    for y,x in weg:
        if out[y,x]!=-2: continue
        c=Counter(out[a,b] for a,b in nb8(y,x) if out[a,b]>0 and out[a,b] not in LINE and Z[a,b]==Z[y,x])
        if c: out[y,x]=c.most_common(1)[0][0]
out[out==-2]=I['G5']
log['7_lijnen_verdund']=len(weg)
np.save('r2_kls.npy',out)
log['diff_in_P']=int(((out!=r1)&P).sum())
print(json.dumps(log))
