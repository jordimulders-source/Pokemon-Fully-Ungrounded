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
w[k>=8]=np.maximum(w[k>=8],15)
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
# Zones (natieve rijen/kolommen) met het aantal schrappingen per zone. Verdeling = evenredig met de zonemaat, behalve dat gezicht en
# hoofdband er minder inleveren en lijf/bovenplaat/punt dat opvangen (de punt wordt daarna toch aangesloten). Binnen een zone één
# schrapping per gelijk stuk (goedkoopste rij/kolom), zodat de zone gelijkmatig krimpt.
# 48: gezicht met de hand: rijen 22,24,26 (26 i.p.v. 27: rij 27 houdt de punt van de rode V) (rechte zijkanten van de oogringen; streep blijft in het midden), kolommen 20 en 34
# (midden van elk oog: beide ogen 7 breed), 29 (V-punt houdt 1 px ruimte aan beide kanten), 39 (rode band rechts; niet 40: dat is op het lijf
# de donkere ribbe tussen voorvlak en zijvlak).
# Rij 16 (lichte onderrand band) i.p.v. 17: de zwarte schaduwlijn onder de overhangende band blijft.
# Kin: rij 30 (leeg) i.p.v. 31: rij 31-32 is de mond (kleine boog 'dMMMMd' onder het midden).
RZ={48:[(0,5,2),(5,16,3),(16,18,[16]),(18,30,[22,24,26]),(30,34,[30]),(34,37,1),(37,58,7),(58,70,4)],
    52:[(0,5,2),(5,16,2),(16,18,0),(18,30,2),(30,34,1),(34,37,1),(37,58,7),(58,70,3)],
    56:[(0,5,1),(5,16,2),(16,18,0),(18,30,1),(30,34,1),(34,37,1),(37,58,5),(58,70,3)]}
KZ={48:[(0,15,6),(15,42,[20,29,34,39]),(42,55,5),(55,68,6)],
    52:[(0,15,4),(15,42,5),(42,55,3),(55,68,5)],
    56:[(0,15,3),(15,42,4),(42,55,3),(55,68,4)]}
def kies_zones(zones,axis):
    kc=kosten(axis); N=len(kc)+1; c=np.r_[1e9,kc]; c[-1]=1e9; gek=[]
    for a,b,n in zones:
        if isinstance(n,list): gek+=n; continue   # met de hand vastgezet (gezicht: ogen even breed, V-punt met 1 px ruimte)
        if n==0: continue
        seg=np.linspace(a,b,n+1)
        for s in range(n):
            lo,hi=int(round(seg[s])),int(round(seg[s+1]))
            kand=[i for i in range(max(1,lo),min(hi,N-1)) if all(abs(i-j)>=2 for j in gek)]
            if not kand: kand=[i for i in range(max(1,a),min(b,N-1)) if all(abs(i-j)>=2 for j in gek)]
            if not kand: kand=[i for i in range(max(1,lo),min(hi,N-1)) if i not in gek]
            gek.append(min(kand,key=lambda i:(c[i],abs(i-(lo+hi)/2))))
    return sorted(gek),c
def schrap_zones(h):
    rows,cr=kies_zones(RZ[h],0); cols,cc=kies_zones(KZ[h],1)
    return np.delete(np.delete(k,rows,0),cols,1),np.delete(np.delete(rgb,rows,0),cols,1),rows,cols,cr,cc
if __name__=='__main__':
    for h in (48,52,56):
        nr=H-h; nk=int(round(W-W*h/H))
        kk,rr,rows,cols,cr,cc=schrap_zones(h)
        print(h,kk.shape,'rijen',rows,'kolommen',cols,'kosten r',int(sum(cr[rows])),'k',int(sum(cc[cols])))
