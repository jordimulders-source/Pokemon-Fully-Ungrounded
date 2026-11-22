# r7: gezichtszone van r6 per pixel naar het model gezet (overnemen, niet hertekenen).
# Elke wijziging t.o.v. r6 staat hieronder met de modelplek (spritepixel -> natieve modelpixels via klas.sx/sy;
# 'frac' = klasse-aandeel in het originele 1024-model, zie frac.py). Plus Jordi's toegestane afwijking: linker plaatrand ronder.
import sys,numpy as np
sys.path.insert(0,'..'); from npy2png import save
sys.path.insert(0,'../r6'); from toon_gezicht import PAL
o=np.load('../r6/sprite.npy').copy()
K,G3,A,a,b,c,L,r,R=1,3,13,7,8,9,10,11,12
W={}   # (x,y): (kleur, reden)
def z(x,y,k,why): W[(x,y)]=(k,why)

# --- 1. Linker plaatrand ronder (Jordi 22 nov, toegestane afwijking): rand volgt de bolling van de kern ---
#     rand per rij was 19,19,18,17,17,18x8,21 (recht x18 over y32-39); wordt 19,19,19,18,17,18,17,17,17,17,18,19,20,21
z(18,29,G3,'rand: rij 29 begint op x19 (was 18)')
z(17,30,G3,'rand: rij 30 begint op x18 (was 17); lidcontour links blijft (18-19,30)')
z(17,36,b,'rand: plaat onder het linkeroog bolt naar x17 (model native x64-65,y101-102: a/b, frac b3K2)')
z(18,38,K,'rand: buitenlijn diagonaal (17,37)-(20,40)')
z(18,39,G3,'rand: rij 39 begint op x20'); z(19,39,K,'rand: buitenlijn diagonaal')

# --- 2. Linkeroog (model natief x63-73, y92-102) ---
z(18,31,A,'bolling: native (67-68,89-90) AAA (frac A3-4)'); z(19,31,A,'bolling: native (69-70,89-90) A')
z(19,33,K,'lid: native (69-70,94-95) KK, gat in het lid dicht'); z(21,33,a,'plaat: frac a6K2')
z(18,34,R,'iris boven: native (67-68,96-97) RR/rr'); z(19,34,R,'iris boven: native (69-70,96-97) R+K; +1 px voor ronde vorm')
z(20,34,K,'lid rechts: native (71-72,96-97) KK'); z(18,35,r,'iris onder: native (67-68,98-100) r'); z(19,35,r,'iris onder: native (69-70,98-100) r')
z(20,35,K,'lid rechts: native (71-72,98-100) K'); z(18,36,b,'onder het oog: native (67-68,101-102) bb'); z(19,36,L,'onderlid: native (69-70,101) KK/L')
z(20,36,b,'plaat: frac b6K3'); z(20,37,b,'plaat: frac b9 (was zwart)'); z(21,36,b,'plaat: frac b9 (was zwart)')

# --- 3. Rechteroog (model natief x85-99, y89-104) ---
z(29,30,a,'crack alleen op native x90-91 (pixel 28); frac (29,30) a5K1')
z(29,31,L,'boogcontour: frac L3A2/A4K3, native (91-93,89) KKK -> boog'); z(30,31,c,'boogcontour rechts: frac c4b2')
z(32,34,b,'plaat: frac b5K2 (lid loopt tot x31, native x97-99)')
for x in range(26,32): z(x,34,K,'lid: native y97 x85-99 KKKK (zware lidlijn)')
z(26,35,K,'lid links: native x85-86'); z(31,35,K,'lid rechts: native x97-99'); z(32,35,b,'plaat: frac b5K4')
for x in range(27,31): z(x,35,R,'iris boven (donker): native y98-100 x87-96 R; notch native x90 (1 natieve px) als R gevuld')
z(26,36,K,'lid links: native (86-87,101-102) KK'); z(31,36,K,'lid rechts: native x96-98 K'); z(32,36,b,'plaat: frac b7L1')
for x in range(27,31): z(x,36,r,'iris onder (licht): native y101-102 x88-95 r; (30,36) +1/3 px')
z(26,37,L,'onderlid: native (86,103) K/c'); z(27,37,L,'onderlid: native (87-88,103-104) cc/K')
z(28,37,r,'iris onderkant: native (90-91,103) Rr'); z(29,37,r,'iris onderkant: native (92-93,103) rr')
z(30,37,L,'onderlid: native (94-95,103) LL'); z(31,37,K,'lid rechtsonder: native (96-97,103) cK')
z(28,38,L,'onderlid onder de iris: native (89-93,104) LKLLL, 1 rij omlaag door de ronde onderkant'); z(29,38,L,'idem')

# --- 4. Licht vlak boven: naar de modelvorm (frac A>=0,4: diagonale band (19-20,26)-(21-24,27)-(20-22,28)-(21-22,29)) ---
for (x,y) in [(21,26),(22,26)]: z(x,y,L,'plaattop zakt hier in: frac g0,4-0,5 + L/K 0,2-0,3 -> bruine rand')
for (x,y) in [(26,23),(25,24),(24,25)]: z(x,y,L,'bovenste punt: linkerkant bruin in het model (frac L0,40 / L0,35 / g0,42+c0,31)')
z(23,28,A,'1-px vlakje weg (frac a0,74 A0,15): sluit aan op het lichte vlak')
z(20,32,a,'onderkant bolling sluit aan op de plaat: frac a4b3')
for (x,y) in [(19,27),(20,27),(19,28),(30,27),(22,30),(23,30)]:
    z(x,y,a,'licht vlak kleiner: model frac A<0,4 hier')
for (x,y) in [(23,27),(24,27),(21,29),(22,29)]: z(x,y,A,'licht vlak: model frac A>=0,4 hier')
# barst midden-boven: model c/L op (24,28)(24,29)(22,29-31) -> één doorlopende lijn i.p.v. r6's horizontale lijn rij 29
for (x,y) in [(19,29),(20,29),(25,28)]: z(x,y,a,'geen lijn hier in het model (frac a)')
for (x,y) in [(24,28),(23,29),(22,30),(22,31)]: z(x,y,c,'barst midden-boven: model L/c (24,28),(24,29),(22,29-31)')

# --- 5. Plaat onder de ogen: glad vlak b, alleen doorlopende modellijnen ---
for y in range(36,42):
    for x in range(17,34):
        if (x,y) in W: continue
        if o[y,x] in (a,b,c,L,A) : z(x,y,b,'vlak glad (dambord weg): model frac b')
for (x,y) in [(23,35),(24,35),(25,35),(25,34)]: z(x,y,b,'plaat: frac b9/b6')
z(23,34,a,'plaat: frac a9'); z(24,34,a,'plaat: frac a9')
z(22,33,A,'neusrug lichte streep: native (76-77,94-95) AA'); z(22,34,A,'lichte streep: native (76-77,96) A')
z(21,34,a,'plaat naast de streep: frac A3b3'); z(21,35,A,'lichte streep onder: native (75,97-100) A')
for (x,y) in [(22,35),(22,36),(22,37)]: z(x,y,c,'neusruglijn: native x76 y99-103 L/c')
for (x,y) in [(23,38),(24,39),(25,40),(25,41)]: z(x,y,c,'barst neus -> onderpunt: model L (23,37),(24,38),(25,39-41)')
for (x,y) in [(21,38),(20,39)]: z(x,y,c,'barst neus -> linksonder: model L (21,37-38),(20,39)')
for (x,y) in [(29,39),(30,40)]: z(x,y,c,'barst onder rechteroog: model L (29,39),(29,40),(30,40)')

for (x,y),(k,_) in W.items(): o[y,x]=k
np.save('sprite.npy',o); save(o,'sprite.png',PAL+[(0,0,0)]*(16-len(PAL)))
r6=np.load('../r6/sprite.npy'); Z=np.zeros((64,64),bool); Z[21:47,14:37]=True
d=o!=r6; print('gewijzigd',int(d.sum()),'buiten zone',int((d&~Z).sum()))
with open('wijzigingen.txt','w') as f:
    for (x,y),(k,why) in sorted(W.items(),key=lambda t:(t[0][1],t[0][0])):
        if r6[y,x]!=k: f.write(f'({x},{y}) {r6[y,x]}->{k}: {why}\n')
