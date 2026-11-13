# maak_r7.py (vanuit kleur_r7/): basis_F.png + KEURING.md (MOET/MAG) -> abra_r7_A.png (modeltonen) en abra_r7_B.png (huid naar regionale Kadabra)
# Jordi: "schaduw, kleuren en belijning". Bevroren: silhouet, ogen, pose, vorm. Alleen pixels uit de lijst hieronder veranderen.
# spritepixel (x,y) = natief modelblok vanaf (2x-1, 2y-14)
import sys; import numpy as np; from PIL import Image
K,L,P1,P2,P3,T,S,M,B,H,I=1,2,3,4,5,6,7,8,9,10,11
NM='.KL123TsmbhI'
src=Image.open('basis_F.png'); a0=np.array(src).astype(int); a=a0.copy()
EDITS=[
 # --- MOET 1: vulkleur op de buitenrand (model sK/sK: lijn op de rechterhelft); sluit de K-rand (25,50)-(25,52)
 ((24,51),K,'M1 vulkleur I op buitenrand -> K'),
 # --- MOET 2: m weg (bijna-dubbel met b, Δ21; huid had 4 vultinten; snuit h|b|m|s = banding). Per pixel naar modelmediaan (>=153 b, anders s);
 #     de schuine plooi (27,27)-(26,31) naar s: modelblokken zijn half b half s (123-133), de donkere helft is het streepje/de schaduwgrens.
 ((27,27),S,'M2 plooi naast rechteroog, model 175|123'),((27,28),S,'M2 plooi, model 114|175'),
 ((26,29),S,'M2 schaduwgrens snuit, model 174|132'),((27,29),S,'M2 schaduwgrens snuit, model 128|175'),
 ((26,30),S,'M2 schaduwgrens snuit, model 174|131'),((26,31),S,'M2 schaduwgrens snuit, model 174|133'),
 ((26,32),B,'M2 snuit, model 193|133 mediaan 163 (banding h|b|m|s -> h|b|b|s)'),((26,33),B,'M2 snuit, mediaan 162'),((26,34),B,'M2 snuit, mediaan 163'),
 ((26,45),B,'M2 bovenkant dij, mediaan 156'),((27,45),B,'M2 dij, mediaan 155'),((28,45),B,'M2 dij, mediaan 152 (rij gelijk houden)'),
 ((40,47),B,'M2 rechterhand, mediaan 152 (sluit aan op b)'),((41,47),S,'M2 rechterhand, mediaan 141'),((40,48),S,'M2 rechterhand, onderhelft zwart, bovenhelft 154'),
 # --- MOET 3: I is een bijna-dubbel van 3 (helderheid 90 vs 89); vlekjes/plooien krijgen 3 (zelfde toon, vibe blijft)
 ((34,27),P3,'M3 wangvlekje I->3'),((31,40),P3,'M3 buikvlekje I->3'),((11,49),P3,'M3 teenplooi I->3'),((12,49),P3,'M3 teenplooi'),((13,49),P3,'M3 teenplooi'),
 ((22,51),P3,'M3 vingerplooi links'),((22,52),P3,'M3 vingerplooi links'),((30,60),P3,'M3 staartvlekje'),
 # --- MOET 4: vingertop rechterhand: T alleen tussen twee K's; model (29,52) licht (253|100) -> lichtkant L, onderkant blijft K
 ((29,51),L,'M4 vingertop linkerrand T->L'),((29,52),L,'M4 vingertop linkerrand K->L'),
 # --- MOET 5: rand van het gat tussen arm en lijf: L K L T T op één rand; boven/oksel K, buikkant L
 ((29,39),K,'M5 gatrand: L tussen drie K, model 96/95/7/49'),((30,42),L,'M5 gatrand T->L (één lijnkleur)'),((30,43),L,'M5 gatrand T->L'),
 # --- MOET 6: onderrand vingertop; T, I en K op één rand; model KK/.. (KEURING_r3 MAG a)
 ((30,58),K,'M6 vingertop onderrand I->K'),
 # --- MAG
 ((52,52),P3,'MAG a ringstreepje staart (model 83, KEURING_r3 c)'),((53,52),S,'MAG b staartring bovenhelft donker 67/70 (r3 f)'),((52,53),S,'MAG b staartring linkerhelft 76 (r3 f)'),
 ((22,50),P3,'MAG c top vingerplooi links (model 57, r3 d), sluit aan op (22,51)'),
 ((39,40),B,'MAG d lichte streep bovenarm loopt door (model 183, r3 g)'),
 ((15,54),L,'MAG e scheen linkerrand: lichtkant -> L (selout)'),((15,55),L,'MAG e scheen linkerrand -> L'),
]
for (x,y),v,why in EDITS:
    assert a0[y,x]>0, (x,y)
    a[y,x]=v
PAL_A=[(255,0,255),(14,13,22),(60,54,80),(49,48,61),(71,68,87),(89,88,103),(104,98,126),(130,126,150),(161,158,174),(180,179,191),(209,206,219),(92,86,114)]
# B: huidreeks van de regionale Kadabra (kadabra_regional/af/kadabra_charlatan.png): licht 220, 185, schaduw 145, donker/selout 94, lijn 67
PAL_B=list(PAL_A); PAL_B[H]=(220,220,230); PAL_B[B]=(184,184,196); PAL_B[S]=(146,140,170); PAL_B[T]=(96,88,124); PAL_B[L]=(66,64,86)
def bewaar(arr,pal,naam):
    im=Image.fromarray(arr.astype('uint8'),'P'); flat=[c for p in pal for c in p]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
bewaar(a,PAL_A,'abra_r7_A.png'); bewaar(a,PAL_B,'abra_r7_B.png')
# controle
OGEN=[(22,28),(23,29),(24,30),(24,31),(30,27),(29,28),(28,29),(28,30)]
assert ((a>0)==(a0>0)).all(), 'silhouet gewijzigd'
assert all(a[y,x]==a0[y,x] for x,y in OGEN), 'ogen gewijzigd'
d=np.argwhere(a!=a0); print('gewijzigd:',len(d),'px; kleuren gebruikt:',len(np.unique(a[a>0])),sorted(NM[v] for v in np.unique(a[a>0])))
if '-v' in sys.argv:
    for (x,y),v,why in EDITS: print(f'({x},{y}) {NM[a0[y,x]]}->{NM[v]}  {why}')
