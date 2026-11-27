# Staryu-koekje r5: eindkeuring Dragonfly Cave op r4 (verse keurder). Alleen uitvoering: schaduw uit de modelhelderheid,
# belijning, kleurtinten. Silhouet bevroren (alpha-diff 0), niets getekend. Elke pixel met een assert op de r4-waarde.
# Bouwen: cd staryu_regional/staryu && python3 sprite_r5/bouw.py
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap_r4'); from gemeen import *
r4=np.asarray(Image.open('sprite_r4/staryu_r4.png')).astype(int); o=r4.copy()
# (X, Y, oud, nieuw, reden). D = gemiddelde modelhelderheid van alleen de deegpixels onder deze spritepixel (r4-model, natief raster).
W=[
 # (a) sikkel uit de modelhelderheid: middendeeg (4) met D < 140 aan de schaduwkant (naast de zwarte buitenlijn) -> schaduw 3
 (12,27,4,3,'linkerarm, onderkant tip, D 128'), (12,28,4,3,'linkerarm, onderkant tip, D 126'),
 (13,29,4,3,'linkerarm onderrand, D 139'), (13,30,4,3,'linkerarm onderrand, D 139'), (14,30,4,3,'linkerarm onderrand, D 128'),
 (30,44,4,3,'rechterbeen in de inkeping, D 121'), (31,46,4,3,'rechterbeen in de inkeping, D 139'),
 (31,47,4,3,'rechterbeen onderrand links, D 109'), (32,47,4,3,'rechterbeen onderrand links, D 119'),
 (32,48,4,3,'rechterbeen onderrand links, D 118'), (33,48,4,3,'rechterbeen onderrand links, D 121'),
 (21,46,4,3,'linkerbeen rechts bij de inkeping, D 120'),
 (46,27,4,3,'rechterarm tip, sikkel, D 137'), (45,28,4,3,'rechterarm tip, sikkel, D 115'),
 (39,39,4,3,'rechterbeen rechts, sikkel loopt taps 3-2-1, D 126'),
 # (a) losse lichte pixel (1 px 4 tussen 3-en, vlekje < 3 px) in de schaduw onder de chip van het rechterbeen
 (38,47,4,3,'vlekje 1 px in de schaduw'),
 # (b) juweelring liep links om en om 10/9/10/9; model is daar licht (D 119, roze rand) -> 10, zodat 9 pas linksonder begint
 (23,32,9,10,'juweelring links, geen om-en-om'),
]
for X,Y,a,b,_ in W:
    assert r4[Y,X]==a, (X,Y,r4[Y,X],a); o[Y,X]=b
assert ((o>0)==(r4>0)).all(), 'silhouet gewijzigd'
assert int((o!=r4).sum())==len(W)
# (c) palet: juweel licht 12 van L 162 naar L 150 (stap rood->licht 52 -> 40, zoals Taillow 37-49); hue 3 graden blijft
PAL[12]=(240,112,106)
opslaan(o,'sprite_r5/staryu_r5.png')
z={}
for X,Y,a,b,r in W: z[r.split(',')[0]]=z.get(r.split(',')[0],0)+1
print('gewijzigd',len(W),'px; per zone',z)
