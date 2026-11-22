# Schrappen (GEMINI.md, Gengas/Alphyena: "Niet-gehele verkleining: schrappen, niet hertekenen"): natief 68x70 -> doelmaat door
# rijen/kolommen weg te laten. Kosten van een rij = aantal pixels dat verschilt van de buurrij; verschillen in beschermde zones
# (gezicht: ogen + rood patroon; hoofdband met chakana) wegen zwaar, rood (klasse 8) extra. Gekozen worden de goedkoopste rijen/kolommen,
# nooit twee naast elkaar, en zo verdeeld dat elk stuk van het lijf meekrimpt. Elke overgebleven pixel is een modelpixel.
import numpy as np, sys
sys.path.insert(0,'gereedschap'); from klassen import laad
k,rgb=laad()
H,W=k.shape
# beschermgewicht per pixel
w=np.ones((H,W))
w[5:17,13:55]=4          # hoofdband (trap/chakana)
w[18:30,15:42]=12        # gezicht: ogen, rode patroon, mond
w[k==8]=np.maximum(w[k==8],15)
def kosten(axis):
    A=k if axis==0 else k.T; Wt=w if axis==0 else w.T
    return np.array([((A[i]!=A[i+1])*np.maximum(Wt[i],Wt[i+1])).sum() for i in range(len(A)-1)])
def kies(n,axis,speling=1):
    # Gengas/Mightyena-stijl: precies één schrapping per gelijk stuk (verhoudingen blijven: hoofd, lijf, armen krimpen even hard),
    # binnen het stuk (± speling) de goedkoopste rij/kolom; nooit twee naast elkaar.
    kc=kosten(axis); N=len(kc)+1
    c=np.r_[1e9,kc]; c[-1]=1e9   # rij i schrappen kost het verschil met rij i-1
    seg=np.linspace(0,N,n+1); gek=[]
    for s in range(n):
        lo,hi=int(np.ceil(seg[s]))-speling,int(np.floor(seg[s+1]))+speling
        kand=[i for i in range(max(1,lo),min(hi,N-1)) if all(abs(i-j)>=2 for j in gek)]
        gek.append(min(kand,key=lambda i:(c[i],abs(i-(lo+hi)/2))))
    return sorted(gek),c
def schrap(nr,nk):
    rows,cr=kies(nr,0); cols,cc=kies(nk,1)
    return np.delete(np.delete(k,rows,0),cols,1),np.delete(np.delete(rgb,rows,0),cols,1),rows,cols,cr,cc
if __name__=='__main__':
    for h in (48,52,56):
        nr=H-h; nk=int(round(W-W*h/H))
        kk,rr,rows,cols,cr,cc=schrap(nr,nk)
        print(h,kk.shape,'rijen',rows,'kolommen',cols,'kosten r',int(sum(cr[rows])),'k',int(sum(cc[cols])))
