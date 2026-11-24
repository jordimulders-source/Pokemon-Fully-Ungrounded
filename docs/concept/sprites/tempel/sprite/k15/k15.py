# k15 = k14 + bovenrand topgevels uit het model (model op sprite-schaal: sx=1+(mx-46)/15.3, sy=3+(my-57)/15.25).
# Model: linkergevel top y5.7 x39.8-41.7, rechtsflank naar (43,9); rechtergevel top (44.3,5.2), nok stijgt naar (48.5,4.1);
# tussen beide gevels een V (bij y6 1 px breed open, bij y7 sluiten de lijnen). De donkere achterplaat boven de linkergevel
# en in de V (model y3-5, x38-46) is weggelaten zodat punt, dal en schuine nok het silhouet vormen (opdracht).
# Alleen x30-46, y0-10; x>=47 (bovenlijn y3 x47-51, nok 6) blijft staan.
import sys
sys.path.insert(0,'../k1')
from gereedschap import *
a14,pal=laad('../k14/tempel.png'); a=a14.copy()
T=0
for x in range(41,47): a[3,x]=T
for x in range(40,45): a[4,x]=T
a[5,39]=T; a[5,42]=T; a[5,43]=T; a[6,43]=T
# linkergevel: punt (selout, lichtkant), rechterflank zwart (schaduwkant) naar de V-bodem
a[5,40]=7; a[5,41]=7; a[6,42]=1; a[7,43]=1
# rechtergevel: top + schuine nok in selout (licht/bovenkant); vlak eronder blijft licht (3), lijn x44 y7 -> x43 y8-9 blijft 2
a[5,44]=7; a[6,44]=7; a[4,45]=7; a[4,46]=7
bewaar(a,pal,'tempel.png')
