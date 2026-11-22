# r9 (herkeuring r8): alleen de drie benoemde punten, herkleuren op het bevroren silhouet. Coördinaten in de code (y,x).
import numpy as np, json
o=np.load('tango_r8.npy').copy(); r8=o.copy()
O,D1,D3,D4=1,3,5,6; DONK=(2,3,4,5,6)
log={}
def zet(y,x,v,k):
    if o[y,x] in DONK and o[y,x]!=v: o[y,x]=v; log[k]=log.get(k,0)+1
# 1. onderkant linkervleugel: y35 drie veerpunten D1 (x2-4, x6-8, x10-11), ertussen D3; y36 D4 alleen als inkeping onder het eind van elke punt; y37 x5-10 -> D3
for x in range(2,12): zet(35,x,D1 if x in (2,3,4,6,7,8,10,11) else D3,'1_y35_veerpunten')
for x in range(4,12): zet(36,x,D4 if x in (4,8,11) else D3,'1_y36_inkepingen')
for x in range(5,11): zet(37,x,D3,'1_y37_naar_D3')
# 2. vleugelaanzet rechts: x42-46, y15-19 egaal D4 (schaduw onder kop/knot); de schuine veerlijn rechts daarvan (x>=47) blijft
for y in range(15,20):
    for x in range(42,47): zet(y,x,D4,'2_aanzet_egaal_D4')
# 3. losse lichte pixel (x39,y23) -> D4
zet(23,39,D4,'3_losse_pixel_D4')
assert ((o>0)==(r8>0)).all()
np.save('tango_r9.npy',o); log['px_veranderd_totaal']=int((o!=r8).sum()); json.dump(log,open('log_r9.json','w'),indent=0); print(log)
