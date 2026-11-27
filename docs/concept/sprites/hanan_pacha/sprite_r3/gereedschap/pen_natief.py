# Stap 5a: vingerpennen op het natieve raster (zelfde as-methode als sprite_r1/gereedschap/pennen.py): goudpixels langs de as
# van elke donkere penpunt tot de witte band -> oranje (binnen) of karmijn (bij de punt). Alleen de klasse verandert; de pixel
# en zijn toon (modelhelderheid) blijven. Uit: natief2.npy (label 100+k = oranje, 200+k = karmijn, k = modelkleur).
import numpy as np, sys
sys.path.insert(0,'../sprite_r1/gereedschap'); from pennen import pennen
sys.path.insert(0,'gereedschap'); from half import GR
N=np.load('natief.npy')
code={'L':1,'T':2,'R':3,'G':4,'D':4,'W':5}
c=np.zeros(N.shape,int); m=N>=0; c[m]=[code[GR[k]] for k in N[m]]
u,assen=pennen(c)
N2=N.copy(); gold=np.isin(N,[k for k,g in GR.items() if g=='G'])
N2[(u==1)&gold]+=100; N2[(u==2)&gold]+=200
np.save('natief2.npy',N2); print('pennen',len(assen),'oranje',((N2>=100)&(N2<200)).sum(),'karmijn',(N2>=200).sum())
