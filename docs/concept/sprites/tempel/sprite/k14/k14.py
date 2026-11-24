# k14 = k13 + latei in perspectief: bovenlijn trapje y44 (x13-17) -> y45 (x18-22) -> y46 (x23-26), 2 px daling,
# treden van 5 px (model: bovenkant zakt ±2 px over de lengte). Dikte gelijk (lijn + 2 rijen vlak + lijn).
# Linkerdeel blijft staan (omhoog zou tegen het linkeroog komen); midden en rechts zakken 1 rij.
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a13,pal=laad('../k13/tempel.png'); a=a13.copy()
# midden x18-21: 1 rij omlaag; boven komt muur (rij 43 erboven, met de sikkel tussen de ogen)
for x in range(18,22):
    for y in (48,47,46,45): a[y,x]=a13[y-1,x]
    a[44,x]=a13[43,x]
a[44,22]=a13[43,22]; a[45,22]=7; a[46,22]=4; a[47,22]=4; a[48,22]=2
# rechts x23-27 (incl. overstek): 1 rij omlaag; onderlijn op y49 over de bovenkant van de rechterstijl
for x in range(23,28):
    for y in (48,47,46): a[y,x]=a13[y-1,x]
    a[45,x]=a13[44,x]
    a[49,x]=2
a[46,18]=3; a[46,19]=3; a[46,20]=3; a[47,18]=5   # lichte bovenrij van het lateivlak loopt door over de trede
bewaar(a,pal,'tempel.png')
