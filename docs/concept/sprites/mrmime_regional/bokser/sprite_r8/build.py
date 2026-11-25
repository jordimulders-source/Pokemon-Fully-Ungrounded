# r8: basis = r7 hoofdversie; alleen kop (bovenrand terug naar r6, hoeken afgerond binnen die maat) en ogen (1-op-1 natief model)
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
a=np.load('../sprite_r7/bokser.npy'); r6=np.load('../sprite_r6/var/meer.npy')
a[2:5,31:45]=r6[2:5,31:45]          # kophoogte/breedte van r6 terug
# hoeken afronden binnen de r6-maat: bovenrand r3 x36-41, hoek r4 x35 links / x42 rechts
a[3,35]=2      # achter de afgeronde hoek valt de linkerkuif (die hier al zat: x32-34)
a[4,35]=1
a[3,42]=0
a[4,42]=1
# ogen: model natief 1-op-1 op de dichtstbijzijnde spritepixel (c=(x+.5-12)/1.397+10, r=(y+.5-5)/1.397), hele oog 1 rij omhoog
# zodat de pupil niet in de snor loopt; pupil zwart boven, donker (2) eronder zoals model (1 / 45); boog lichtgrijs 7 (model 189-222)
for x in range(31,40):
    for y in range(8,13):
        if a[y,x] in (3,4) or (y in (10,11) and x in (32,36) and a[y,x] in (1,2,3)): a[y,x]=8   # r7-oog weg
OOG={'pupil':[(33,10,1),(33,11,2),(36,10,1),(36,11,2)],
     'boog':[(33,8),(33,9),(32,11),  (36,9),(37,8),(38,8),(38,9),(38,10),(38,11)]}
for x,y,t in OOG['pupil']: a[y,x]=t
for x,y in OOG['boog']: a[y,x]=7
save(a,'bokser')
