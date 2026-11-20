# Hoatzin r9: Gen 3-kleurronde op r8 (vorm/silhouet bevroren, kop van r8 ongewijzigd).
# Regels per onderdeel (na studie Pidgeot/Skarmory/Swellow/Braviary/Talonflame/Staraptor, zie NOTITIES.md):
# R1 buitenlijn: zwart waar de figuur rechts/onder aan de achtergrond grenst, gekleurde selout (donkerste tint) aan de lichtkant
# R2 waaier: elke schacht (licht, bovenrand pen) krijgt links een donkere pengrens (grens van de pen erboven) -> pen = licht/midden/donker
# R3 staart: lichtkant (links) van elke staartveer één tint lichter
# R4 poten: nabije poot licht/midden, verre poot midden/donker (één stap donkerder)
# R5 lijf: sikkelschaduw (1 tint donkerder) langs de schaduwkant van lijf/hals
# R6 buik: selout aan de lichtkant in de donkerste buiktint
import numpy as np, json; from PIL import Image
SRC=Image.open('r8.png'); S0=np.array(SRC).astype(int); S=S0.copy(); PAL=[tuple(SRC.getpalette()[3*i:3*i+3]) for i in range(16)]
Z=np.full((64,64),'.',dtype='<U1'); Z[1:,6:57]=np.load('../r4/zone_t.npy')
fg=S0!=0; yy,xx=np.mgrid[:64,:64]
ok=lambda y,x:0<=y<64 and 0<=x<64
tr=lambda y,x: (not ok(y,x)) or not fg[y,x]
kop=(xx<=28)&(yy<=27)          # kop/kuif van r8: niet aanraken
log={}
def zet(y,x,v,r):
    if S[y,x]!=v and not kop[y,x]: log[r]=log.get(r,0)+1; S[y,x]=v
MAUVE=(2,3,4,5)
# ---- R2 waaier ----
fan=(xx>=36)&(xx<=56)&(yy>=2)&(yy<=19)
for y,x in zip(*np.where(fan&(S0==5))):
    q=(y,x-1)   # pen = licht (schacht, bovenrand) -> midden -> donkere grens; de grens van de vorige pen ligt links van de schacht
    if ok(*q) and S0[q] in (3,4) and not tr(y,x-2) and S0[y,x-2] not in (1,2,5): zet(q[0],q[1],2,'R2 pengrens links van de schacht (licht direct onder de grens)')
# ---- R3 staart ----
staart=(Z=='D')|((xx>=36)&(yy>=43))
for y,x in zip(*np.where(staart&(S0==2))):
    if S0[y,x-1]==1: zet(y,x,3,'R3 lichtkant staartveer')
# ---- R4 poten ----
poot=np.isin(S0,[14,15])&(yy>=49)
for y,x in zip(*np.where(poot)):
    schaduw=any(tr(y+d,x+e) or S0[y+d,x+e]==1 for d,e in ((0,1),(1,0)))
    licht=any(tr(y+d,x+e) or S0[y+d,x+e]==1 for d,e in ((0,-1),(-1,0)))
    if x>=29:   # nabije poot
        zet(y,x,14 if (schaduw and not licht) else 15,'R4 nabije poot: licht, schaduwkant midden')
    else:       # verre poot: één stap donkerder
        zet(y,x,2 if (schaduw and not licht) else 14,'R4 verre poot: midden, schaduwkant donker')
# ---- R5 lijf sikkel ----
lijf=(xx>=15)&(xx<=40)&(yy>=36)&(yy<=50)&np.isin(S0,[3,4])
for y,x in zip(*np.where(lijf)):
    if any(tr(y+d,x+e) or S0[y+d,x+e] in (1,2) for d,e in ((1,0),(1,1))): zet(y,x,S0[y,x]-1,'R5 sikkel lijf (1 tint donkerder onderaan)')
# ---- R6 buik selout ----
for y,x in zip(*np.where(np.isin(S0,[3])&(xx<=18)&(yy>=37)&(yy<=46))):
    if any(np.isin(S0[y,x+1],[11,12,13]) for _ in (0,)): zet(y,x,11,'R6 buik selout lichtkant')
# ---- R1 buitenlijn ----
# schaduwkant = achtergrond rechts, of onder zonder achtergrond links (trapjes aan de linkerrand blijven lichtkant)
for y,x in zip(*np.where(fg)):
    if kop[y,x]: continue
    tn=[(d,e) for d,e in ((1,0),(-1,0),(0,1),(0,-1)) if tr(y+d,x+e)]
    if not tn: continue
    schaduwkant=((0,1) in tn) or ((1,0) in tn and (0,-1) not in tn)
    binnen=[S[y+d,x+e] for d,e in ((1,0),(-1,0),(0,1),(0,-1)) if not tr(y+d,x+e)]
    if S[y,x]==1 and not schaduwkant and binnen and all(v in (2,3,4,5) for v in binnen): zet(y,x,2,'R1 selout lichtkant (was zwart)')
    elif S[y,x] in (3,4,5) and not schaduwkant: zet(y,x,2,'R1 selout lichtkant (mauve)')
    elif S[y,x] in (12,13) and not schaduwkant: zet(y,x,11,'R1 selout lichtkant (buik)')
    elif S[y,x] in (2,3,4,5,11,12,13) and schaduwkant: zet(y,x,1,'R1 zwart schaduwkant')
assert ((S!=0)==fg).all()
im=Image.fromarray(S.astype('uint8'),'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
im.save('hoatzin.png',transparency=0); im.convert('RGBA').resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
print(json.dumps(log,indent=1,ensure_ascii=False)); print('anders dan r8:',int((S!=S0).sum()))
