# Ronde 4: hoofd (kuif, brein, gezicht, mond) opnieuw uit r5 verkleind met factor 3/s (s = 1,15 / 1,25 / 1,35).
# Blokken met niet-gehele grootte (afronden van de blokgrenzen); zelfde regels als reduceer3 (lijn, gemeten helderheid).
import numpy as np; from PIL import Image
import bewerk, reduceer2, reduceer3, kleur, lijnweg, schoon, materiaal as mt
GRENS={}
for y in range(9,22): GRENS[y]=(86,118)
for y in range(22,27): GRENS[y]=(84,106)
for y in range(27,31): GRENS[y]=(77,110)
for y in range(31,35): GRENS[y]=(73,112)
for y in range(35,41): GRENS[y]=(70,115)
for y in range(41,51): GRENS[y]=(68,116)
for y in range(51,56): GRENS[y]=(69,114)
for y in range(56,59): GRENS[y]=(72,110)
for y in range(59,62): GRENS[y]=(76,104)
for y in range(62,64): GRENS[y]=(82,98)
X0,Y0,X1,Y1=66,9,120,64
def masker():
    m=np.zeros((201,201),bool)
    for y,(l,r) in GRENS.items(): m[y,l:r+1]=True
    return m
def bron(n_krul=3):
    """r5 zonder rugglas; in het brein alleen de n grootste windingen (lijnstukken) houden, de rest weghalen."""
    a=bewerk.zonder_rugglas(bewerk.R5).astype('uint8')
    z=np.zeros((201,201),bool)
    for y,(l,r) in bewerk.HOOFD.items(): z[y,l:r+1]=True
    comps=sorted(lijnweg.toon_comps(a,z),reverse=True)
    grens=comps[n_krul-1][0] if len(comps)>=n_krul else 1
    return lijnweg.weg(a,z,grens,drempel=100), comps[:n_krul]
BREIN=None
def blokken(n0,n1,f):
    k=int(np.ceil((n1-n0)/f)); return [(n0+int(round(i*f)),n0+int(round((i+1)*f))) for i in range(k)]
def reduceer(a,f,M=None,regel='midden'):
    P=reduceer2.pixlabels(a); L=reduceer3.ontspikkel(a.astype(float)@[0.299,0.587,0.114])
    M=masker() if M is None else M
    ys=blokken(Y0,Y1,f); xs=blokken(X0,X1,f); lab=np.zeros((len(ys),len(xs)),int)
    for j,(ya,yb) in enumerate(ys):
        for i,(xa,xb) in enumerate(xs):
            b=P[ya:yb,xa:xb].ravel(); l=L[ya:yb,xa:xb].ravel(); mm=M[ya:yb,xa:xb].ravel()
            n=len(b); geldig=(b!=0)&mm
            if geldig.sum()<n*0.5: continue
            k=((b==1)&mm).sum()
            if regel=='midden':     # lijn als de middelste modelpixel van het blok lijn is, of het blok voor de helft lijn
                cy,cx=(ya+yb)//2,(xa+xb)//2
                if (P[cy,cx]==1 and M[cy,cx]) or k>=0.5*n: lab[j,i]=1; continue
                if BREIN is not None and BREIN[cy,cx] and k>=2: lab[j,i]=1; continue   # brein: windingen doorlopend houden
            elif k>=max(2,0.25*n): lab[j,i]=1; continue
            sel=geldig&(b>=10)&(b<20)
            if sel.sum()==0:
                sel=geldig&(b>=20)
                if sel.sum()==0: lab[j,i]=1; continue
                v,c=np.unique(b[sel],return_counts=True); lab[j,i]=v[c==c.max()].min(); continue
            lab[j,i]=10+max(1,int(np.searchsorted(kleur.ZAND,l[sel].mean())))
    return lab
def oog_r8(f,box=(80,52,107,63)):
    """r8-oogzone verkleind met factor f (zelfde materiaalregel als ronde 1-3), uitkomst: 1 pupil, 23 wit, 10 lid, 0 leeg."""
    R8=bewerk.R8.astype(float); L=R8@[0.299,0.587,0.114]; h,s,v=mt.hsv(R8)
    x0,y0,x1,y1=box; out=[]
    for ya,yb in blokken(y0,y1,f):
        row=[]
        for xa,xb in blokken(x0,x1,f):
            l=L[ya:yb,xa:xb].ravel(); ss=s[ya:yb,xa:xb].ravel(); n=len(l)
            zw=(l<60).sum(); wi=((l>195)&(ss<0.25)).sum(); db=(l<125).sum()
            if zw>=max(1,n*0.25) and zw>=wi: row.append(1)
            elif wi>=max(1,n*0.3): row.append(23)
            elif db>=max(2,n*0.4): row.append(10)
            else: row.append(0)
        out.append(row)
    return np.array(out)
