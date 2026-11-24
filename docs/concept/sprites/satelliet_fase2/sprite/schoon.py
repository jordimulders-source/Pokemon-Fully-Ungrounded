# Technische opschoning (geen vormen): 
# 1) buitenrand: lichte randpixel (paneelrand 11/15/4/2/3) waar het model buiten nog omlijning heeft (>=0,2 van dat blok)
#    -> die buitenpixel wordt omlijning (silhouet +1, gemeten); anders wordt de randpixel zelf omlijning.
# 2) losse pixels (geen 4-buur van dezelfde klasse) buiten oog/antennes/bollen -> meest voorkomende 4-buur.
#    Losse zwarte pixel zonder zwarte 8-buur idem.
import numpy as np, sys; from PIL import Image
o=np.load(sys.argv[1]).copy(); base=np.load(sys.argv[2]); UIT=sys.argv[3]
F=np.load(sys.argv[4])      # blokfracties per klasse (kaal.py)
H,W=o.shape
prot=(o!=base)               # door oog.py/antennes.py gezet
import os
ap=sys.argv[1].replace('.npy','_ant.npy')
if os.path.exists(ap): prot|=np.load(ap)
yy,xx=np.mgrid[0:H,0:W]; prot|=np.hypot(xx+.5-20,yy+.5-24)<6.3
nb4=lambda j,i:[(j+dy,i+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=j+dy<H and 0<=i+dx<W]
groei=[];zw=[]
def randpas(eye_ook):
  for j in range(H):
    for i in range(W):
        v=o[j,i]
        if v in (2,3,4,11,15,5) and (eye_ook or not prot[j,i]):
            leeg=[q for q in nb4(j,i) if o[q]==0]
            if not leeg: continue
            ok=False
            for q in leeg:
                if F[q][1]>=0.2: o[q]=1; groei.append((q[1],q[0])); ok=True
            if not ok: o[j,i]=1; zw.append((i,j))
randpas(True)
# randpixels die aan de rand van het canvas zitten (j=0, i=0, i=W-1) idem: randpixel zelf omlijning
for j in range(H):
    for i in (0,W-1):
        if o[j,i] in (2,3,4,11,15,5): o[j,i]=1; zw.append((i,j))
los=[]
for it in range(3):
    for j in range(H):
        for i in range(W):
            v=o[j,i]
            if v==0 or prot[j,i]: continue
            n=[o[q] for q in nb4(j,i)]
            if v in n: continue
            if v==1:
                d8=[o[j+dy,i+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=j+dy<H and 0<=i+dx<W]
                if 1 in d8 or 0 in n: continue
            if v in (11,15) and any(o[j+dy,i+dx]==v for dy in (-1,1) for dx in (-1,1) if 0<=j+dy<H and 0<=i+dx<W): continue
            c=[q for q in n if q!=0]
            if not c: continue
            nv=max(set(c),key=c.count); o[j,i]=nv; los.append((i,j,int(v),int(nv)))
randpas(True)
np.save(UIT,o)
print('silhouet +1 (omlijning buiten lichte rand):',len(groei),groei); print('randpixel -> omlijning:',len(zw),zw); print('losse pixels vervangen:',len(los),los)
