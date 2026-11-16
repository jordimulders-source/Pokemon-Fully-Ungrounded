# r18 = r17 + (1) koeienvanger met de modellijnen uit natief.png (kv.py) en (2) kop-schaduw uit de toonkaart van het model (kop.py).
# Bevroren (assert): alle groene indexen, zwarte gezichtslijnen van de grote kop, rij 0-19. Buiten kop/koeienvanger diff 0.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from kv import *
import kop as K
from collections import Counter
im=Image.open(D+'sprite_r17/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
pal=pal[:42]+list(K.LICHTBRUIN)+pal[45:]
kopm,gez,rndk=K.masks(r)
# ---------- 1. koeienvanger
a,zone,lijn,groef,vcells,roest=bouw2(r,pal)
KV=np.zeros((64,64),bool); KV[45:59,0:28]=True
# zwart tegen groen boven de V-lijn (rij>=45, buiten het kopmasker) wordt band, zoals in het model (bruine band tussen grijns en V)
vmin={}
for (y,x) in vcells: vmin[x]=min(vmin.get(x,99),y)
for y,x in zip(*np.where(zone&(r==1))):
    if (y,x) not in lijn and x in vmin and y<vmin[x] and not gez[y,x]: a[y,x]=9
# 1-px-eilandjes in de plaatvulling -> buurmodus (lijnen en roestvlekken blijven)
for it in range(2):
    b=a.copy()
    for y,x in zip(*np.where(zone)):
        if a[y,x] in (10,11,12,7) and (y,x) not in lijn and nb8(a,y,x).count(a[y,x])==0:
            n=[v for v in nb8(a,y,x) if v in (7,10,11,12)]
            if n: b[y,x]=Counter(n).most_common(1)[0][0]
    a=b
# zwart dat een bevroren gezichtslijn verbindt blijft (anders wordt (44,18) een losse stip)
for y,x in zip(*np.where(KV&(r==1)&(a!=1))):
    if any(r[y+dy,x+dx]==1 and not KV[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if ok(y+dy,x+dx)): a[y,x]=1
# eilandjes: (46,8) roest in het kleine V-dal = band 9; (54,15) middentand: lichte kolom loopt door tot rij 54 (model nx26 ny74-78 licht)
if a[46,8]==8: a[46,8]=9
if a[54,15]==8: a[54,15]=7
# middentand: punt omlaag (model: rij 81 nx25-27 zwart, smalste punt rij 80 nx26); 1 px weg zodat de punt 1 px is
if a[57,14]==1 and a[57,15]==1: a[57,14]=0
# buitenlijn lichtkant links (model nx10-11 ny66-73 = donkerroest): selout 9 in rij 45-50
for y in range(45,51):
    xs=[x for x in range(0,8) if r[y,x]!=0]
    if xs and a[y,xs[0]]==1: a[y,xs[0]]=9
# ---------- 2. kop
S_W=0.5
T=K.toonkaart(r,kopm)
sel=kopm&np.isin(r,[7,8,9,10])&~rndk&~gez&~KV
bruin=sel&np.isin(r,[8,9]); plaat=sel&np.isin(r,[7,10])
Y,X=np.mgrid[0:64,0:64]
vx=(X+.5-15)/14; vy=(Y+.5-32)/14; vz=np.sqrt(np.clip(1-vx**2-vy**2,0,1))
Lv=np.array([-0.55,-0.6,0.58]); Lv/=np.linalg.norm(Lv)
SH=vx*Lv[0]+vy*Lv[1]+vz*Lv[2]
z=lambda A:(A-np.nanmean(A[sel]))/np.nanstd(A[sel])
S=(1-S_W)*z(T)+S_W*z(SH)          # toonkaart model + bolterm (licht linksboven)
qb=np.percentile(S[bruin],(30,78)); qp=np.percentile(S[plaat],(25,65))
for y,x in zip(*np.where(bruin)): v=S[y,x]; a[y,x]=14 if v>=qb[1] else (8 if v>=qb[0] else 9)
for y,x in zip(*np.where(plaat)): v=S[y,x]; a[y,x]=7 if v>=qp[1] else (10 if v>=qp[0] else 11)
# 1-px-eilandjes in de kop binnen dezelfde familie -> buurmodus
FAM={14:(14,8,9),8:(14,8,9),9:(14,8,9),7:(7,10,11),10:(7,10,11),11:(7,10,11)}
for it in range(2):
    b=a.copy()
    for y,x in zip(*np.where(sel)):
        if nb8(a,y,x).count(a[y,x])==0:
            n=[v for v in nb8(a,y,x) if v in FAM[a[y,x]]]
            if n: b[y,x]=Counter(n).most_common(1)[0][0]
    a=b
TOON=np.where(sel,np.digitize(S,np.percentile(S[sel],(20,60,85))),-1)   # 4 tonen voor het vel (0 donker .. 3 licht)
# ---------- bewijs bevroren
GRS=[2,3,4,5,6,13]
g=np.isin(r,GRS)|np.isin(a,GRS)
assert (a[g]==r[g]).all(),'groen gewijzigd'
assert (a[gez]==r[gez]).all(),'gezichtslijnen gewijzigd'
assert (a[:20]==r[:20]).all(),'rij 0-19 gewijzigd'
buiten=~(KV|kopm)
assert (a[buiten]==r[buiten]).all(),'buiten kop/koeienvanger gewijzigd'
assert len(np.unique(a))<=16
if __name__=='__main__':
    d=(a!=r)
    print('gewijzigd: koeienvanger',int(d[KV].sum()),' kop',int(d[kopm&~KV].sum()),' elders',int(d[buiten].sum()),
          ' groen-diff',int((a[g]!=r[g]).sum()),' gezicht-diff',int((a[gez]!=r[gez]).sum()),' rij0-19-diff',int(d[:20].sum()),' kleuren',len(np.unique(a)))
    o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal)
    o.save(D+'sprite_r18/sprite.png',transparency=0)
    o.resize((512,512),Image.NEAREST).save(D+'sprite_r18/sprite_8x.png',transparency=0)
    with open(D+'sprite_r18/raster.txt','w') as f:
        for row in a: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
    np.save(D+'sprite_r18/toon.npy',TOON)
