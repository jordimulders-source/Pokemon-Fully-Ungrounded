# Schrappen (GEMINI.md, Gengas: "Niet-gehele verkleining: schrappen, niet hertekenen"): figuur 73x72 natief -> <=64x64 door
# rijen/kolommen weg te laten. Kosten van rij i = aantal pixels dat verschilt van rij i-1, gewogen: gezicht (2 ogen + neus + afwerking),
# rode lijn, punt en de oogjes in de krans zwaar. Eén schrapping per gelijk stuk (verhoudingen blijven), goedkoopste binnen het stuk (+-1),
# nooit twee naast elkaar. Elke overgebleven pixel is een modelpixel.
import numpy as np, sys
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse
k,a=klasse()
ys,xs=np.where(k>0); Y0,Y1,X0,X1=ys.min(),ys.max(),xs.min(),xs.max()
H,W=k.shape; yy,xx=np.mgrid[0:H,0:W]
w=np.ones((H,W))
w[(xx>=25)&(xx<=59)&(yy>=33)&(yy<=50)]=12             # gezicht: 2 ogen, neus, afwerking
w[(k>=11)]=15                                          # rode lijn (kop) en rode banden (lijf/staven)
w[(xx>=41)&(xx<=52)&(yy>=12)&(yy<=26)]=5               # punt bovenop
LAAG=(k>=8)&(k<=10)                                    # streepjes/stipjes = donker binnen een licht krans-oog
licht=(k>=2)&(k<=4)
for y in range(1,H-1):
    for x in range(1,W-1):
        if LAAG[y,x] and licht[y-1:y+2,x-1:x+2].sum()>=4: w[y-1:y+2,x-1:x+2]=np.maximum(w[y-1:y+2,x-1:x+2],10)
def kosten(axis):
    A=k if axis==0 else k.T; Wt=w if axis==0 else w.T
    c=np.array([1e9]+[((A[i]!=A[i-1])*np.maximum(Wt[i],Wt[i-1])).sum() for i in range(1,len(A))]); return c
def kies(n,lo,hi,axis,speling=1):
    c=kosten(axis); seg=np.linspace(lo+1,hi,n+1); gek=[]
    for s in range(n):
        a_,b_=int(np.ceil(seg[s]))-speling,int(np.floor(seg[s+1]))+speling
        kand=[i for i in range(max(lo+1,a_),min(hi,b_)+1) if all(abs(i-j)>=2 for j in gek)]
        gek.append(min(kand,key=lambda i:(c[i],abs(i-(a_+b_)/2))))
    return sorted(gek),c
def schrap(nr,nk):
    rows,cr=kies(nr,Y0,Y1,0); cols,cc=kies(nk,X0,X1,1)
    kk=np.delete(np.delete(k,rows,0),cols,1); aa=np.delete(np.delete(a,rows,0),cols,1)
    ys,xs=np.where(kk>0); kk=kk[ys.min():ys.max()+1,xs.min():xs.max()+1]; aa=aa[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return kk,aa,rows,cols,cr,cc
if __name__=='__main__':
    nr,nk=int(sys.argv[1]),int(sys.argv[2])
    kk,aa,rows,cols,cr,cc=schrap(nr,nk)
    print(kk.shape,'rijen',rows,'kosten',[int(cr[i]) for i in rows]); print('kolommen',cols,'kosten',[int(cc[i]) for i in cols])
