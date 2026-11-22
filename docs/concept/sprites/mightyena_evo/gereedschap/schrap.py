# Schrappen (GEMINI.md, Gengas: "Niet-gehele verkleining: schrappen, niet hertekenen"): 74x70 natief -> 64x61 door 10 kolommen en
# 9 rijen weg te laten. Eén schrapping per gelijk stuk (verhoudingen blijven), binnen het stuk de rij/kolom die het meest op zijn buur lijkt.
# Verschil met gezichtsklassen (oog, bek, tand) weegt 10x. Elke overgebleven pixel is een modelpixel.
import numpy as np
def kosten(c,axis):
    A=c if axis==0 else c.T
    w=np.where(np.isin(A,(6,7,8,9,10)),10,1)
    return np.array([((A[i]!=A[i+1])*np.maximum(w[i],w[i+1])).sum() for i in range(len(A)-1)])
def kies(c,n,axis,verboden=()):
    k=kosten(c,axis); N=c.shape[axis]; grenzen=np.linspace(0,N,n+1)
    gek=[]
    for s in range(n):
        lo,hi=int(np.ceil(grenzen[s])),int(np.floor(grenzen[s+1]))
        r=0
        while True:
            kand=[i for i in range(max(1,lo-r),min(hi+r,N-1)) if i not in verboden and all(abs(i-j)>=3 for j in gek)]
            if kand: break
            r+=1
        gek.append(min(kand,key=lambda i:(k[i],abs(i-(lo+hi)/2))))
    return gek,k
# Gezicht heilig: oogrijen/bekrijen en ogen/snuit/bek-kolommen worden nooit geschrapt; ook de klauwrijen van de poten niet.
VR=set(range(13,29))|set(range(62,70)); VK=set(range(0,15))
def schrap(c,nr=9,nk=10):
    rows,kr=kies(c,nr,0,VR); cols,kk=kies(c,nk,1,VK)
    return np.delete(np.delete(c,rows,0),cols,1),rows,cols,kr,kk
