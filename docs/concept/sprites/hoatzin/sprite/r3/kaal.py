# Kale reductie hoatzin r1: vlakgemiddelde per spritepixel over het model + dichtstbijzijnde modelkleurgroep.
# Geen hertekening; alleen regels per vak. Uitvoer: kaal.png + kaal.npy
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
TF=0.45   # figuur vanaf 50 % niet-achtergrond
TR=0.25   # rood wint vanaf 25 %
TB=0.30   # blauw wint vanaf 30 %
TK=0.33   # zwarte lijn wint vanaf 40 %
TY=0.35   # geelgroen wint vanaf 35 %
OOG=(270,380,260,345)   # modelvak oog: wit telt daar als glans, elders als achtergrond (antialias)
def tlijf(l): return 2 if l<30 else 3 if l<50 else 4   # l = gemiddelde modelhelderheid over zwart+lijf in het vak
def tgg(l): return 5 if l<112 else 6 if l<165 else 7
def tbl(l): return 8 if l<100 else 9
def tro(l): return 10 if l<80 else 11
def reduceer():
    a,c,L=laad()
    c=c.copy()
    oog=np.zeros(c.shape,bool); oog[OOG[2]:OOG[3],OOG[0]:OOG[1]]=True
    c[(c==W)&~oog]=0
    o=np.zeros((64,64),int); info={}
    for Yy in range(64):
        for X in range(64):
            v=vak(X,Yy,c,L)
            if v is None: continue
            cc,ll,w,_=v
            f=np.array([w[cc==k].sum() for k in range(7)])
            if 1-f[0]<TF: continue
            def lm(k): m=cc==k; return (w[m]*ll[m]).sum()/max(w[m].sum(),1e-9)
            def lkd(): m=(cc==K)|(cc==D); return (w[m]*ll[m]).sum()/max(w[m].sum(),1e-9)
            if f[W]>=0.2: o[Yy,X]=12
            elif f[R]>=TR: o[Yy,X]=tro(lm(R))
            elif f[B]>=TB: o[Yy,X]=tbl(lm(B))
            elif f[K]>=TK: o[Yy,X]=1
            elif f[Y]>=TY: o[Yy,X]=tgg(lm(Y))
            else:
                k=[D,Y,K][int(np.argmax([f[D],f[Y],f[K]]))]
                o[Yy,X]=1 if k==K else tlijf(lkd()) if k==D else tgg(lm(Y))
            info[(Yy,X)]=f
    return o,info
if __name__=='__main__':
    o,_=reduceer(); np.save(os.path.join(HIER,'kaal.npy'),o); opslaan(o,os.path.join(HIER,'kaal.png')); toon(o)
    print('kleuren',sorted(set(o.ravel())),'figuur',(o>0).sum())
