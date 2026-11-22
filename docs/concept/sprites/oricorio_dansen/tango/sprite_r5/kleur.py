# Kleurronde op het bevroren silhouet (tango_kls.npy): alleen bestaande pixels herkleuren, alpha-diff 0 (gecontroleerd).
# Elke nieuwe tint op een gemeten modelplek (model_L.npy) of als Gen 3-selout/volume; tellingen in log_kleur.json.
import numpy as np, json
o=np.load('tango_kls.npy').copy(); k0=o.copy(); L=np.load('model_L.npy'); H,W=o.shape
_,O,D0,D1,D2,D3,D4,R1,R2,R3,K1,K2,K3,WI=range(14)
DONK=(D0,D1,D2,D3,D4); ROOD=(R1,R2,R3)
log={}
def tel(k): log[k]=log.get(k,0)+1
def tr(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]==0
def zet(y,x,v,k):
    if o[y,x]!=v: o[y,x]=v; tel(k)
# 1. franje: tinten op de modelhelderheid van het 2x2-natieve blok i.p.v. de ene geschrapte cel (veernaden lopen zo beter door):
#    L<64 -> R3 (naad), L>=79 -> R1 (lichtste veerstroken), anders R2
for y in range(40,H):
    for x in range(W):
        if o[y,x] in ROOD:
            v=R3 if L[y,x]<64 else (R1 if L[y,x]>=79 else R2)
            zet(y,x,v,'1_franje_tint_op_model_L')
# 1b. R1 alleen als vlak: losse R1-pixel zonder R1-buur terug naar R2 (geen korrel)
for y in range(H):
    for x in range(W):
        if o[y,x]==R1 and not any(0<=y+a<H and 0<=x+b<W and o[y+a,x+b]==R1 for a,b in((-1,0),(1,0),(0,-1),(0,1))): o[y,x]=R2; tel('1b_losse_R1_terug')
# 2. jurk-volume (model is hier één vlak, L±31): lichtband aan de lichtkant (links), breedte 3->1 van boven naar onder, in D3;
#    1 px verder naar binnen bovenaan (borst) D2. Alleen D4-pixels in de jurkzone (rij 28-44, kol 24-46).
for y in range(28,45):
    xs=[x for x in range(23,47) if o[y,x]==D4]
    if not xs: continue
    x0=min(xs)
    if o[y,x0-1] not in (O,D2,D3): continue        # alleen waar de jurk aan de buitenlijn/vleugelnaad grenst
    bw={28:2,29:2,30:3,31:3,32:3,33:3,34:2,35:2,36:1,37:1,38:1}.get(y,0)   # lichtsikkel die de borstbolling volgt
    for x in range(x0,x0+bw):
        if o[y,x]==D4: zet(y,x,D3,'2_jurk_lichtband_D3')
for y,x in ((29,27),(30,27),(29,28)):
    if o[y,x] in (D3,D4): zet(y,x,D2,'2_borst_hooglicht_D2')
# 2c. binnenlijnen in kop/hals (zwart zonder transparante buur, rij 17-27, buiten oog/snavel) -> D4: de kop/halsnaad van het model
#     las als een mondje; in Gen 3 is een binnenlijn een donkere tint van het vlak
for y in range(17,28):
    for x in range(18,46):
        if o[y,x]==O and not any(tr(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1))) and not (y<=19 and x<=30):
            zet(y,x,D4,'2c_binnenlijn_kop_hals_D4')
# 3. selout: omlijning aan de lichtkant (transparant boven of links, niet onder/rechts) -> donkere tint van het vlak erachter
SEL={D0:D4,D1:D4,D2:D4,D3:D4,D4:D4,R1:R3,R2:R3,R3:R3}
for y in range(H):
    for x in range(W):
        if o[y,x]!=O: continue
        up=tr(y-1,x); lf=tr(y,x-1); dn=tr(y+1,x); rt=tr(y,x+1)
        if not (up or lf) or dn or rt: continue
        if 10<=y<=22 and 22<=x<=36: continue        # oog/snavel bevroren
        inn=[o[y+1,x] if up else None, o[y,x+1] if lf else None]
        g=[SEL[v] for v in inn if v in SEL]
        if g: zet(y,x,g[0],'3_selout')
assert ((o>0)==(k0>0)).all()
np.save('tango_r5.npy',o); json.dump(log,open('log_kleur.json','w'),indent=0); print(log,'herkleurd',int((o!=k0).sum()))
