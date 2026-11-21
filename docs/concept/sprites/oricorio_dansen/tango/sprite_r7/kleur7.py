# r7 (eindkeuring r6: FAIL op tinten/schaduw/lijn). Alleen herkleuren op het bevroren r6-silhouet (alpha-diff 0, assert).
# Nieuwe donkere reeks: hooglicht D0 / licht D1 / midden D3 / donker D4 / lijn O (idx 4 = D2 samengevoegd met D3).
import numpy as np, json
from collections import Counter
o=np.load('tango_r6.npy').copy(); r6=o.copy(); L=np.load('model_L.npy'); H,W=o.shape
_,O,D0,D1,D2,D3,D4,R1,R2,R3,K1,K2,K3,WI=range(14)
DONK=(D0,D1,D2,D3,D4); ROOD=(R1,R2,R3)
log={}
def zet(y,x,v,k):
    if o[y,x]!=v and o[y,x]!=0: o[y,x]=v; log[k]=log.get(k,0)+1
def tr(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]==0
def nb(y,x): return [(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+a<H and 0<=x+b<W]
def rand(y,x): return any(tr(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)))
# 0. vleugels (vóór de samenvoeging): r6-voorrand D2 -> D1, r6-selout (D3/D4 op de lichtrand) -> D3 (doorlopende gekleurde rand)
def vleugel(y,x): return (y<=28 and x>=47) or (19<=y<=28 and x>=39) or (26<=y<=39 and x<=23)
for y in range(H):
    for x in range(W):
        if not vleugel(y,x): continue
        if r6[y,x]==D2: zet(y,x,D1,'0_vleugel_voorrand_D1')
        elif r6[y,x] in (D3,D4) and (tr(y-1,x) or tr(y,x-1)) and not (tr(y+1,x) or tr(y,x+1)): zet(y,x,D3,'0_vleugel_selout_D3')
# 0b. linkervleugel: lichtere veerrij direct boven de modelveernaden (L<20, binnen) -> D3
for y in range(26,40):
    for x in range(0,22):
        if o[y,x]==O and not rand(y,x) and L[y,x]<20 and y>=34 and o[y-1,x]==D4: zet(y-1,x,D3,'0b_veerrij_D3_boven_modelnaad')
# 0c. vleugelpunt links (x1-7, y33-34): rand doorlopend D3, D1 alleen 1 px binnen
for y,x in ((33,5),(34,2),(34,3),(34,1)):
    if o[y,x] in DONK: zet(y,x,D3,'0c_vleugelpunt_rand_D3')
# 1. samenvoegen: overige D2 -> D3
for y in range(H):
    for x in range(W):
        if o[y,x]==D2: zet(y,x,D3,'1_D2_samengevoegd_met_D3')
# 2. jurk (rij 28-45, kol 24-41; zwart en rood blijven): hoofdvlak D3; naast de vleugelaanzet (rij 28-34) D3 tegen de D4-vleugel;
#    lichtband D1 links (rij 35-44, breedte 3-2-1 die de bolling volgt) met hooglicht D0; sikkel D4 rechts (2 px, uiteinden 1);
#    lichte plooi midden-onder (model L>=52) -> D1
for y in range(28,46):
    xs=[x for x in range(24,43) if o[y,x] in DONK]
    if not xs: continue
    for x in xs: zet(y,x,D3,'2_jurk_hoofdvlak_D3')
    x0,x1=min(xs),max(xs)
    if y>=35:   # (rij 28-34 grenst aan de donkere vleugel: jurk blijft daar D3, zo contrasteert de D4-vleugel ermee)
        bw={35:2,36:3,37:3,38:3,39:2,40:2,41:2,42:1,43:1,44:1}.get(y,0)
        for x in range(x0,x0+bw):
            if o[y,x] in DONK: zet(y,x,D1,'2_jurk_lichtband_D1')
    sw=1 if y in (28,29,44,45) else 2
    for x in range(x1-sw+1,x1+1): zet(y,x,D4,'2_jurk_sikkel_D4')
    for x in xs:
        if 38<=y and x0+3<=x<=34 and L[y,x]>=52 and o[y,x]==D3: zet(y,x,D1,'2_jurk_plooi_D1_model')
for y,x in ((36,25),(37,25),(37,26)): zet(y,x,D0,'2_jurk_hooglicht_D0')
# 2b. zwart alleen als buitenlijn: losse zwarte binnenpixels in de jurk -> D4 (sikkeltint)
for y,x in ((29,37),(44,24)):
    if o[y,x]==O and not rand(y,x): zet(y,x,D4,'2b_zwart_binnen_jurk_D4')
# 3. V-hals: V-lijn 1 px (D4) op het gemeten modelpad (L<40), binnen de V egaal D1 met hooglicht D0 links, eronder/erbuiten jurktint D3,
#    slagschaduw D4 1 px onder de V-punt.
VL=[(22,23),(23,24),(24,25),(25,26),(24,27),(23,28),(23,29),(22,30),(22,31),(21,32),(21,33),(20,34),(20,35),(19,36),(19,37)]
def vlijn_rij(x):   # rij van de V-lijn per kolom (laagste rij bij gelijke kolom)
    r=[y for y,xx in VL if xx==x]; return max(r) if r else None
for x in range(23,38):
    ry=vlijn_rij(x)
    if ry is None: continue
    for y in range(17,29):
        if o[y,x] not in DONK: continue
        if (y,x) in VL: zet(y,x,D4,'3_V_lijn_D4')
        elif y<ry and y>=19: zet(y,x,D1,'3_binnen_V_D1')
        elif y>ry and y<=27: zet(y,x,D3,'3_buiten_V_D3')
for y,x in ((26,26),(26,27)): zet(y,x,D4,'3_slagschaduw_onder_V')
for y,x in ((21,25),(21,26),(22,26)): zet(y,x,D0,'3_borst_hooglicht_D0')
# randen van de V-zone links (kol 22-23 onder de lijn) -> D3
for y in range(23,28):
    for x in (22,23):
        if o[y,x] in DONK and (y,x) not in VL: zet(y,x,D3,'3_buiten_V_D3')
# 4. franje: lichtrand (leeg boven/links, niet onder/rechts) -> donkerste rood R3; schaduwkant (leeg onder/rechts) -> zwart;
#    de pixel 1 binnen een R3-rand: R3 -> R2 zodat de rand als lijn leest
fr=[]
for y in range(44,H):
    for x in range(W):
        if o[y,x] in ROOD and rand(y,x):
            if tr(y+1,x) or tr(y,x+1): zet(y,x,O,'4_franje_schaduwrand_zwart')
            else: zet(y,x,R3,'4_franje_lichtrand_R3'); fr.append((y,x))
for y,x in fr:
    for a,b in ((y+1,x),(y,x+1)):
        if o[a,b]==R3 and not rand(a,b): zet(a,b,R2,'4_franje_binnen_licht')
assert ((o>0)==(r6>0)).all()
np.save('tango_r7.npy',o); log['px_veranderd_totaal']=int((o!=r6).sum()); json.dump(log,open('log_r7.json','w'),indent=0)
for k,v in log.items(): print(k,v)
