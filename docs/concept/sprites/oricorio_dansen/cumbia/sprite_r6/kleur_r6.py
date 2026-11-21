# r6 (herkeuring r5): alleen kopsikkel als doorlopende band, losse N-stompjes weg, borsthooglicht 1 px naar binnen. Coördinaten (x,y).
import numpy as np, json
from collections import Counter
o=np.load('cumbia_r5.npy').copy(); r5=o.copy(); H,W=o.shape
O,B1,B2,B3,N=1,2,3,4,5; HL=15
log={}
def nb(y,x): return [(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<H and 0<=x+dx<W]
def vlak(y,x):
    c=Counter(o[a,b] for a,b in nb(y,x) if o[a,b] not in (0,O,N,B2)); return c.most_common(1)[0][0] if c else B3
OOG={(y,x) for y in range(14,19) for x in range(25,29)}|{(14,29),(14,30),(15,29),(15,30),(16,29),(16,30),(16,31),(17,29),(17,30),(17,31),(18,29),(18,30)}   # Pom-Pom-oog + zijn schaduwpixels: bevroren
# 1. kopsikkel: per rij (y12-22) de meest rechtse B3-strook in x29-34; de pixel er direct links van wordt B2; overige B2 in de zone -> vlaktint
band=set()
for y in range(12,23):
    xs=[x for x in range(29,35) if o[y,x]==B3 and (y,x) not in OOG]
    if not xs: continue
    x=max(xs)
    while x-1>=29 and o[y,x-1]==B3 and (y,x-1) not in OOG: x-=1
    if (y,x-1) not in OOG and o[y,x-1] in (B1,B2): band.add((y,x-1))
for y in range(12,23):
    for x in range(29,35):
        if (y,x) in OOG: continue
        if (y,x) in band and o[y,x]!=B2: o[y,x]=B2; log['1_band_gezet']=log.get('1_band_gezet',0)+1
        elif (y,x) not in band and o[y,x]==B2: o[y,x]=B1; log['1_los_B2_weg']=log.get('1_los_B2_weg',0)+1
for x,y in ((30,26),(31,25),(20,26)):            # losse B2 in de halszone (keurder)
    if o[y,x]==B2: o[y,x]=vlak(y,x); log['1_los_B2_hals']=log.get('1_los_B2_hals',0)+1
# 2. losse N-stompjes -> vlaktint eromheen
for x,y in ((18,29),(21,30),(22,31),(16,32),(33,29),(35,29),(41,29),(34,9)):
    if o[y,x]==N: o[y,x]=vlak(y,x); log['2_stompjes']=log.get('2_stompjes',0)+1
# 3. borsthooglicht 1 px naar rechts (binnen op de bolling)
hl=[(y,x) for y,x in zip(*np.where(r5==HL)) if y>=21]
for y,x in hl: o[y,x]=B1
for y,x in hl: o[y,x+1]=HL
log['3_hooglicht_verschoven']=len(hl)
d=(o!=r5); log['totaal_gewijzigd']=int(d.sum())
np.save('cumbia_r6.npy',o); np.save('diff_r6.npy',d); json.dump(log,open('log_r6.json','w'),indent=0); print(log)
print('band',sorted((x,y) for y,x in band))
