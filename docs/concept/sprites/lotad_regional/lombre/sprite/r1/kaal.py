# Kale reductie door rijen/kolommen te SCHRAPPEN (Gengas-methode: niets hertekenen, elke overgebleven pixel is een modelpixel).
# Figuur 54x74 natief -> 42x57 (12 kolommen, 17 rijen weg). Telkens de rij/kolom die het minst verschilt van een buur,
# gelijk verdeeld over de figuur, niet naast een eerder geschrapte, niet door het oog. Snavelpixels (16) tellen niet mee (die worden vervangen).
import numpy as np, sys
from gemeen import opslaan
q=np.load('kwant.npy'); ys,xs=np.where(q>0); f=q[ys.min():ys.max()+1,xs.min():xs.max()+1].copy()
OFF=(ys.min(),xs.min())
NR=int(sys.argv[1]) if len(sys.argv)>1 else 17; NK=int(sys.argv[2]) if len(sys.argv)>2 else 12
OOG_Y=range(36-OFF[0],42-OFF[0]); OOG_X=range(45-OFF[1],52-OFF[1])
def kies(f,n,besch,afstand=2):
    # gelijk verdeeld: de figuur in n even grote vakken; per vak precies één rij weg (de rij die het minst verschilt van een buur)
    idx=list(range(f.shape[0])); weg=[]; N=f.shape[0]
    vak=[(int(round(1+k*(N-2)/n)),int(round(1+(k+1)*(N-2)/n))) for k in range(n)]
    g=f.copy()
    for v0,v1 in vak:
      best=None
      for rek in (0,1,2,3):   # geen kandidaat in het vak (oog/buur): vak 1-3 rijen oprekken
        if best is not None: break
        for r in range(1,g.shape[0]-1):
            orig=idx[r]
            if not(v0-rek<=orig<v1+rek) or orig in weg: continue
            if orig in besch or any(abs(orig-w)<afstand for w in weg): continue
            m=(g[r]!=16)
            s=min(((g[r]!=g[r-1])&m).sum(),((g[r]!=g[r+1])&m).sum())
            if best is None or s<best[0]: best=(s,r)
      if best is None: continue
      s,r=best; weg.append(idx[r]); g=np.delete(g,r,0); del idx[r]
    return g,sorted(weg)
f2,wr=kies(f,NR,set(OOG_Y))
f3,wk=kies(f2.T,NK,set(OOG_X)); f3=f3.T
print('rijen weg (natief, t.o.v. figuur):',wr); print('kolommen weg:',wk); print('maat',f3.shape[1],'x',f3.shape[0])
o=np.zeros((64,64),int); h,w=f3.shape; X0=(64-w)//2; Y0=63-h; o[Y0:63,X0:X0+w]=f3
np.save('kaal.npy',o); np.save('kaal_meta.npy',np.array([OFF[0],OFF[1],Y0,X0]+[-1]+wr+[-1]+wk))
opslaan(o,'kaal.png')
