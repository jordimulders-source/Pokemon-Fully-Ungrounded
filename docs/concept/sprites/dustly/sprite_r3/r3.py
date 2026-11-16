# r3 = r2, met de mondzone (x11-25, y33-37) terug naar de kale automatische reductie (sprite_r1/auto.py), niets getekend.
# Rijen 31-32 horen bij de ogen en blijven r2. Alleen de buitenlijnpixels op de silhouetrand blijven r2 (technische buitenlijn).
import numpy as np
a=np.load('sprite_r1/auto_idx.npy'); r2=np.load('sprite_r2/r2_idx.npy'); o=r2.copy()
keep={(11,33),(11,36),(11,37)}   # buitenlijn (roze selout / donker), geen mond
for y in range(33,38):
    for x in range(11,26):
        if (x,y) not in keep: o[y,x]=a[y,x]
# hoektanden: vorm van Gastly Gen 3 (punt = wit dat 1 px onder de bovenrij doorloopt; rechtertand bovenrij wit+lichtgrijs,
# punt onder het grijs, zoals Gastly's rechtertand (38-39,41-42)), op de plek van de modeltanden (kale reductie: wit (22,35),
# tandsleuf (14,35) tussen donker (13,35)/(15,35); de donkere tandpunt eronder (14,36)/(22,36) wordt de witte punt).
TAND={(14,35):9,(14,36):9,(21,35):9,(22,35):10,(22,36):9}
for (x,y),v in TAND.items(): o[y,x]=v
np.save('sprite_r3/r3_idx.npy',o)
z=np.zeros((64,64),bool); z[33:38,11:26]=True
print('diff r3-r2 totaal',(o!=r2).sum(),'buiten zone',((o!=r2)&~z).sum())
print('diff mondzone t.o.v. kale reductie',((o!=a)&z).sum(),[(x,y,int(o[y,x]),int(a[y,x])) for y,x in zip(*np.where((o!=a)&z))])
