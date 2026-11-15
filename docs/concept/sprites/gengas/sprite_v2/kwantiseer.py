# Model (model_64_geschrapt.png) -> indexraster met het GEMETEN palet (pal.py): elke pixel krijgt de
# dichtstbijzijnde paletkleur in Lab. Uitvoer: start-raster (geen tekenwerk).
import sys
from gemeen import *
from pal import PAL,CH
a=model(); bg=achtergrond(a)
idx,d=dichtst(a,PAL[1:]); idx=idx+1; idx[bg]=0
open(sys.argv[1],'w').write('\n'.join(''.join(CH[v] for v in r) for r in idx)+'\n')
print('gem. dE',round(d[~bg].mean(),2))
