# controle: losse pixels (geen enkele 4-buur met dezelfde index, niet omlijning/paars/koper/glans), omlijning (1) midden in een vlak
import numpy as np, sys
CH='.#kdgGLcChWwvpor'
f=np.loadtxt(sys.argv[1],dtype=int); H,W=f.shape; los=[]; binnen=[]
for r in range(1,H-1):
    for c in range(1,W-1):
        v=f[r,c]
        if v==0: continue
        nb=[f[r-1,c],f[r+1,c],f[r,c-1],f[r,c+1]]
        if v not in (1,9,13,14,15) and v not in nb: los.append((c,r,CH[v],''.join(CH[x] for x in nb)))
        if v==1 and 0 not in [f[r+a,c+b] for a in (-1,0,1) for b in (-1,0,1)] and sum(x==1 for x in nb)<=1: binnen.append((c,r))
print('losse pixels',len(los)); [print(' ',x) for x in los]
print('omlijning zonder buren in vlak',binnen)
