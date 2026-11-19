# Zwaartepunten van de spikkels in het natieve model -> doelpixels (zelfde schaal/fase als bouw.py)
import numpy as np
Z=np.load('zones_nat.npy'); P=(Z=='P'); H,W=P.shape; lab=np.zeros_like(P,int); n=0; comps=[]
for y in range(H):
  for x in range(W):
    if P[y,x] and not lab[y,x]:
      n+=1; st=[(y,x)]; pts=[]
      while st:
        a,b=st.pop()
        if 0<=a<H and 0<=b<W and P[a,b] and not lab[a,b]:
          lab[a,b]=n; pts.append((a,b)); st+=[(a+dy,b+dx) for dy in (-1,0,1) for dx in (-1,0,1)]
      comps.append(pts)
s=77/40; out=[]
for pts in comps:
    cy=np.mean([p[0] for p in pts]); cx=np.mean([p[1] for p in pts])
    out.append((len(pts),int((cy-18)/s),int((cx-11)/s)))
out.sort(reverse=True); np.save('spot_c.npy',np.array(out)); print(out)
