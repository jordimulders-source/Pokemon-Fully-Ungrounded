# Hoatzin r6 = r5 (palet, lijnen) + snavel opnieuw uit het model + kuif met verder doorlopend zuur (K1-K4 varianten).
# Diff 0 buiten de snavel- en kuifzone (bewezen onderaan).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
sys.path.insert(0,HIER+'/../r5'); import dc
R5=HIER+'/../r5/'
a,c,L=laad()
def lD(cc,ll,w): m=cc==D; return (w[m]*ll[m]).sum()/w[m].sum() if m.any() else None
def snavelzone(X,Yy): return 6<=X<=16 and 15<=Yy<=25 and not (X>=16 and Yy<=18)
def kuifzone(X,Yy): return (Yy<=8 and 10<=X<=33) or (27<=X<=33 and Yy<=17 and not (X>=33 and Yy>=15)) or (9<=X<=12 and Yy<=10)
ZONE=np.array([[snavelzone(X,Yy) or kuifzone(X,Yy) for X in range(64)] for Yy in range(64)])
C=np.array([21.0,12.0])   # kopmidden (x,y): stekels stralen hiervandaan uit
RB=5.0                     # straal van de kop; daarbuiten begint de kuif
def snavel(o):
    """silhouet: figuur vanaf 20 % modeldekking (alleen toevoegen); tint uit de modelhelderheid. In het model is de snavelkegel
       duidelijk lichter (L 54-92) dan de kop (L 38-45); met de r5-grenzen vielen kegel en kop in dezelfde middentint, waardoor
       de kegel verdween. Snavelgrenzen: >= 54 licht (kegel + rug), 44-54 midden, < 44 donker (onderkant/kaak);
       zwart waar het model >= 33 % zwart heeft."""
    o=o.copy(); n=0
    for Yy in range(64):
        for X in range(64):
            if not snavelzone(X,Yy): continue
            cc,ll,w,_=vak(X,Yy,c,L); f=np.array([w[cc==k].sum() for k in range(7)])
            if 1-f[0]<0.20 and o[Yy,X]==0: continue
            if 1-f[0]<0.20: continue
            if f[K]>=0.33 and o[Yy,X] in (0,1): o[Yy,X]=1; continue
            l=lD(cc,ll,w)
            if l is None: continue
            o[Yy,X]=4 if l>=54 else 3 if l>=44 else 2
    return o
def stekels(o):
    """geelgroene punten in de kuif (r5): per punt (8-samenhangend cluster) de verste pixel P vanaf het kopmidden = stekelpunt."""
    m=np.zeros((64,64),bool)
    for Yy in range(20):
        for X in range(64):
            if kuifzone(X,Yy) and o[Yy,X] in GG: m[Yy,X]=True
    lab,n=label(m); P=[]
    for i in range(1,n+1):
        pts=[np.array([X,Yy],float) for Yy,X in zip(*np.where(lab==i))]
        P.append(max(pts,key=lambda p:np.linalg.norm(p-C)))
    return P
def kuif(o,frac,P):
    """zuur over frac van elke stekel vanaf de punt (frac=1: hele kuif). Pixel hoort bij een stekel als hij binnen 1,7 px van de
       straal kopmidden->punt ligt en buiten de kopstraal RB. Tint per stekel naar de relatieve plek t (0 = binnenkant van het zuur,
       1 = punt): olijf < 1/3, midden < 2/3, licht; harde grenzen. Zwarte lijnen blijven zwart."""
    o=o.copy()
    for Yy in range(20):
        for X in range(64):
            if not kuifzone(X,Yy) or o[Yy,X] in (0,1) or o[Yy,X] not in LIJF|GG: continue
            q=np.array([X,Yy],float); r=np.linalg.norm(q-C)
            if r<RB: continue
            best=None
            for p in P:
                d=(p-C)/np.linalg.norm(p-C); Lp=np.linalg.norm(p-C)
                s=(q-C)@d; perp=np.linalg.norm((q-C)-s*d)
                if perp<=1.7 and s<=Lp+0.5:
                    start=Lp-frac*(Lp-RB)
                    if s>=start:
                        t=(s-start)/max(Lp-start,1e-9)
                        if best is None or t>best: best=t
            if frac>=1.0 and best is None and r>=RB+0.5:   # K1: ook de kuifmassa tussen de stekels
                best=(r-RB)/max(max(np.linalg.norm(p-C) for p in P)-RB,1e-9)
            if best is None: continue
            o[Yy,X]=5 if best<1/3 else 6 if best<2/3 else 7
    return o
def belijn(o,orig):
    """r5-belijning (dc.bewerk) opnieuw, maar alleen binnen de zones overgenomen."""
    # dc.bewerk werkt op de r4-indices (zelfde betekenis); randregel: selout licht, zwart schaduwkant, dunne zuurpunt -> midden
    b,_=dc.bewerk(o)
    out=orig.copy(); out[ZONE]=b[ZONE]
    return out
def maak(bron,doel,frac,P=None):
    im=Image.open(R5+bron); r5=np.array(im); pal=im.getpalette()
    P=P or stekels(r5)
    o=snavel(r5); o=kuif(o,frac,P); o=belijn(o,r5)
    out=Image.fromarray(o.astype('uint8'),'P'); out.putpalette(pal); out.save(HIER+'/'+doel,transparency=0)
    buiten=int((o!=r5)[~ZONE].sum())
    sn=int(sum((o!=r5)[Yy,X] for Yy in range(64) for X in range(64) if snavelzone(X,Yy)))
    ku=int(sum((o!=r5)[Yy,X] for Yy in range(64) for X in range(64) if kuifzone(X,Yy)))
    print('%-34s snavel %3d px, kuif %3d px, buiten de zones %d (moet 0), kleuren %d'%(doel,sn,ku,buiten,len(set(o.ravel())-{0})))
    return o
if __name__=='__main__':
    P=stekels(np.array(Image.open(R5+'hoatzin_r5.png')))
    print('stekelpunten',[(int(p[0]),int(p[1])) for p in P])
    maak('hoatzin_r5.png','hoatzin_r6.png',0.5,P)
    maak('hoatzin_r5_variant_teken.png','hoatzin_r6_variant_teken.png',0.5,P)
    for k,f in (('K1',1.0),('K2',1/3),('K3',0.5),('K4',2/3)): maak('hoatzin_r5.png','hoatzin_r6_%s.png'%k,f,P)
