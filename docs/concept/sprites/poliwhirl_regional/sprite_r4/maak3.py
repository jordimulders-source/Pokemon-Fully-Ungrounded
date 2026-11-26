# r3: basis = r2_S2; alleen de oogzone verandert. E6/E5 = Poliwhirls eigen oog met rijen/kolommen WEGGEHAALD (niets getekend),
# EM = kale reductie van het modeloog op het spritegrid (modeloog.py-klassen), technisch opgeschoond.
import numpy as np
import maak2 as M
from modeloog import K
V=M.V; H,W=M.H,M.W
r2=np.load('../sprite_r2/r2_S2.npy')
OOGC=[(16,5.1),(29.2,4.8)]   # middens modelogen, gemeten op de witte oogring (links 15,7 -> 16: anders steekt het oog 1 kolom de lucht in)
WEG={'E6':([3],[3]),'E5':([1,3],[3,4])}   # te verwijderen rijen/kolommen (relatief in het 7x7-oog)
BOX=[(19,27,12,20),(36,46,12,20)]
def kop_uit_model(o):
    o[M.OOGZ]=V.MODELOOG[M.OOGZ]
def rest_weg(o,geplakt):
    rest=M.OOGZ&~geplakt&np.isin(o,[8,9,10,11])&~V.crys
    for _ in range(5):
        for y,x in zip(*np.where(rest)):
            nb=[o[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W and o[y+a,x+b] not in (0,8,9,10,11)]
            if nb: o[y,x]=max(set(nb),key=nb.count); rest[y,x]=False
INFO=[]
def oog_klein(o,var):
    geplakt=np.zeros((H,W),bool)
    for box,(cx,cy) in zip(BOX,OOGC):
        sub,m=M.oogmasker(*box); yy,xx=np.where(m)
        sub=sub[yy.min():yy.max()+1,xx.min():xx.max()+1]; m=m[yy.min():yy.max()+1,xx.min():xx.max()+1]
        rw,kw=WEG[var]
        rows=[j for j in range(7) if j not in rw]; cols=[i for i in range(7) if i not in kw]
        weg=[(int(i+box[0]+xx.min()),int(j+box[2]+yy.min())) for j in range(7) for i in range(7) if m[j,i] and (j in rw or i in kw)]
        s=sub[np.ix_(rows,cols)]; mm=m[np.ix_(rows,cols)]
        h,w=s.shape; dx=int(round(cx-(w-1)/2)); dy=int(round(cy-(h-1)/2))
        for j in range(h):
            for i in range(w):
                if mm[j,i]: o[j+dy,i+dx]=V.OOGMAP[s[j,i]]; geplakt[j+dy,i+dx]=True
        INFO.append((var,int(m.sum()),int(mm.sum()),weg,(dx,dx+w-1,dy,dy+h-1)))
    return geplakt
EMCEL={}
def oog_model(o):
    # per cel het meerderheidsmateriaal van het modeloog: Z zwart -> 1, W wit -> 8, G grijs -> 10; geel/lucht: kop uit het model laten staan
    geplakt=np.zeros((H,W),bool); xs,ys=V.z['xs'],V.z['ys']
    for (cx,cy) in ((16,5),(29,5)):
        for y in range(cy-3,cy+3):
            for x in range(cx-3,cx+3):
                blk=K[int(ys[y]):int(ys[y+1]),int(xs[x]):int(xs[x+1])].ravel(); u,c=np.unique(blk,return_counts=True); k=u[np.argmax(c)]
                EMCEL[(x,y)]=k
                if o[y,x]==0 or k=='Y': continue
                o[y,x]={'Z':1,'W':8,'G':10}[k]; geplakt[y,x]=True
    # technisch: wit op de silhouetrand -> omlijning 1
    rand=[]
    for y,x in zip(*np.where(geplakt&np.isin(o,[8,10]))):
        if any(not(0<=y+a<H and 0<=x+b<W) or o[y+a,x+b]==0 for a,b in ((1,0),(-1,0),(0,1),(0,-1))): o[y,x]=1; rand.append((int(x),int(y)))
    INFO.append(('EM',int(geplakt.sum()),None,rand,None))
    return geplakt
def maak(var):
    o=r2.copy(); kop_uit_model(o)
    g=oog_model(o) if var=='EM' else oog_klein(o,var)
    rest_weg(o,g); return o
