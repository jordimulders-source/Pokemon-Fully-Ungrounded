# Controles: aantal kleuren, losse pixels (geen enkele 8-buur in dezelfde kleur), kleine tintvlakjes (<3 px, 4-samenhang).
import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
im=Image.open(sys.argv[1] if len(sys.argv)>1 else 'kecleon_evo_r1.png'); a=np.array(im)
ORDE='.krABCDEFGHpqswm'
print('modus',im.mode,'grootte',im.size,'gebruikte kleuren',len(np.unique(a)),'(incl. transparant)')
H,W=a.shape; los=[]
for y in range(H):
  for x in range(W):
    v=a[y,x]
    if v==0: continue
    n=[a[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
    if v not in n: los.append((x,y-1,ORDE[v]))
print('losse pixels (x,y sprite-63, kleur):',los)
klein=[]
for v in np.unique(a):
  if v==0 or ORDE[v] in 'kw': continue
  lab,n=nd.label(a==v)
  for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(ys)<3: klein.append((ORDE[v],[(int(x),int(y)-1) for x,y in zip(xs,ys)]))
print('vlakjes <3 px:',len(klein))
for k in klein: print('  ',k)
