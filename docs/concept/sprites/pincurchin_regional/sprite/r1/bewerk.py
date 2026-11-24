# Jordi's toegestane afwijkingen op het natieve raster (niets tekenen; vullen met wat het model ernaast heeft):
# 1. knobbeltje bovenop weg (natief x40-43, y27-32)  2. modelogen weg  3. modelmond weg (naadlijn loopt door)
from PIL import Image;import numpy as np
from kaart import lab,P
a=np.asarray(Image.open('natief.png').convert('RGB')).copy(); L=lab(a)
WIT=(255,255,255); M=P['m']; D=P['D']; K=P['K']
ed=np.zeros(a.shape[:2],bool)
def zet(x,y,c): a[y,x]=c; ed[y,x]=True
# 1. knobbeltje: boven de lijfrand -> wit; nieuwe lijfrand op rij 30 (zwart, zoals rechts naast de staaf rij 31); donkere knobbelvoet rij 32 -> lijf
for y in (27,28,29):
    for x in range(39,44):
        if L[y,x] not in 'RLr': zet(x,y,WIT)
for x in (41,42,43):
    if L[30,x] not in 'RLr': zet(x,30,K)
for x in (42,43): zet(x,32,M)
# 2. ogen -> lijfkleur (vakken rond de gele ringen)
for y in range(52,58):
    for x in range(26,30): zet(x,y,M)
for y in range(53,59):
    for x in range(46,52): zet(x,y,M)
# 3. mond -> lijf boven de naad; onderrand van de mond = bovenste naadlijn (loopt door)
for y in range(55,62):
    for x in range(30,45):
        if L[y,x] in 'oOyRrLKw': zet(x,y,M)
for x in range(35,44): zet(x,62,M)
for x in (32,33,34): zet(x,62,D)
for x in range(35,42): zet(x,63,D)
Image.fromarray(a).save('natief_A.png'); np.save('natief_bewerkt.npy',ed)
Image.fromarray(a).resize((800,800),Image.NEAREST).save('natief_A_8x.png'); print('natieve pixels bewerkt',ed.sum())
