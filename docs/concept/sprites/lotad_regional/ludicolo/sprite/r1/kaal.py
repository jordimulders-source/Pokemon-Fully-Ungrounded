# Kale reductie door rijen/kolommen te SCHRAPPEN (Gengas-/Lombre-methode: niets hertekenen, elke overgebleven pixel is een modelpixel).
# Figuur 75x91 natief -> 51x62 (24 kolommen, 29 rijen weg; factor 0,68). Per gelijk vak één rij/kolom: die het minst verschilt
# van een buur, niet naast een eerder geschrapte, niet door de ogen (rijen 36-40, kolommen 34-37 en 44-48 natief beschermd).
import numpy as np, sys
from gemeen import opslaan
q=np.load('kwant.npy'); ys,xs=np.where(q>0); f=q[ys.min():ys.max()+1,xs.min():xs.max()+1].copy()
OFF=(ys.min(),xs.min())
NR=int(sys.argv[1]) if len(sys.argv)>1 else 29; NK=int(sys.argv[2]) if len(sys.argv)>2 else 24
OOG_Y=set(range(36-OFF[0],41-OFF[0])); OOG_X=set(range(34-OFF[1],38-OFF[1]))|set(range(44-OFF[1],49-OFF[1]))
def kies(f,n,besch,afstand=2):
    idx=list(range(f.shape[0])); weg=[]; N=f.shape[0]
    vak=[(int(round(1+k*(N-2)/n)),int(round(1+(k+1)*(N-2)/n))) for k in range(n)]
    g=f.copy()
    for v0,v1 in vak:
      best=None
      for rek in (0,1,2,3):
        if best is not None: break
        for r in range(1,g.shape[0]-1):
            orig=idx[r]
            if not(v0-rek<=orig<v1+rek) or orig in weg: continue
            if orig in besch or any(abs(orig-w)<afstand for w in weg): continue
            s=min((g[r]!=g[r-1]).sum(),(g[r]!=g[r+1]).sum())
            if best is None or s<best[0]: best=(s,r)
      if best is None: print('vak zonder kandidaat',v0,v1); continue
      s,r=best; weg.append(idx[r]); g=np.delete(g,r,0); del idx[r]
    return g,sorted(weg)
f2,wr=kies(f,NR,OOG_Y)
f3,wk=kies(f2.T,NK,OOG_X); f3=f3.T
print('rijen weg (t.o.v. figuur):',wr); print('kolommen weg:',wk); print('maat',f3.shape[1],'x',f3.shape[0])
o=np.zeros((64,64),int); h,w=f3.shape; X0=(64-w)//2; Y0=63-h; o[Y0:63,X0:X0+w]=f3
np.save('kaal.npy',o); np.save('kaal_meta.npy',np.array([OFF[0],OFF[1],Y0,X0]+[-1]+wr+[-1]+wk))
opslaan(o,'kaal.png')
