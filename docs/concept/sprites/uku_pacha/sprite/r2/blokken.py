# Uku Pacha r2: blokjes tussen de lijnen (lijf/kronkels, niet koppen/geest/vleugels) egaal per blok
# met de oppervlak-gewogen meerderheidstoon van het model over het HELE blok (zelfde modelplek,
# geen nieuwe vorm). Grote vlakken (> MAXB px) houden hun per-pixel-tonen (schaduwverloop van het model).
import numpy as np, geom, sys
cls=np.load('cls.npy'); GH=np.load('GH.npy')
R=[list(l.rstrip('\n')) for l in open('raster.txt')][:64]
KOP=np.zeros((64,64),bool); KOP[2:28,0:23]=True; KOP[2:16,29:50]=True
LIJN=set('Kn.')
LET={6:'d',5:'d',8:'s',9:'s',11:'m',12:'b',13:'l',14:'p',15:'w',10:'B',7:'D'}
MAXB=int(sys.argv[1]) if len(sys.argv)>1 else 8
seen=np.zeros((64,64),bool)
def vrij(x,y): return R[y][x] not in LIJN and not KOP[y,x] and not GH[y,x] and R[y][x] not in 'BDhYPW'
for y in range(64):
  for x in range(64):
    if seen[y,x] or not vrij(x,y): continue
    comp=[];st=[(x,y)]
    while st:
      a,b=st.pop()
      if 0<=a<64 and 0<=b<64 and not seen[b,a] and vrij(a,b):
        seen[b,a]=True; comp.append((a,b)); st+=[(a+1,b),(a-1,b),(a,b+1),(a,b-1)]
    if len(comp)>MAXB: continue
    acc={}
    for a,b in comp:
      x0,x1,y0,y1=geom.s2n(a,b)
      for cy in range(int(y0),int(np.ceil(y1))):
        for cx in range(int(x0),int(np.ceil(x1))):
          ar=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy)); k=cls[cy,cx]
          if ar>0 and k in LET: acc[LET[k]]=acc.get(LET[k],0)+ar
    if acc:
      t=max(acc,key=acc.get)
      for a,b in comp: R[b][a]=t
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
