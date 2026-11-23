# r7b.py: r7b = r7 + (1) linkerarm als gebogen arm (onderarm loopt door in de bovenarm omhoog naar de schouder),
# (2) rugrots met schuine lichte voorkant. Alles uit de meting van het model (meet6.npz); rest bevroren.
import numpy as np; from PIL import Image
r7=Image.open('r7.png'); O=np.asarray(r7).astype(int).copy(); R7=O.copy()
d=np.load('meet6.npz'); lf,hel=d['lf'],d['hel']
# (1) arm. Model: onderarm x 13-16 (rij 31-33) buigt bij x 16 omhoog in de bovenarm x 16-17 (rij 27-31) naar de schouder.
# In r7 scheidde een lijn op (16,30),(16,31) die twee; die pixels zijn in het model roze arm (de binnenhoek van de elleboog
# loopt erdoorheen) -> vlak, zodat onder- en bovenarm één gebogen vorm worden.
# Tinten (Gen 3, licht linksboven): bovenkant onderarm f, midden 8, onderkant + bovenarm (schaduwzijde, onder de baard) 7.
ARM={(14,31):15,(15,31):15,(13,32):8,(14,32):8,(15,32):8,(16,32):8,(13,33):8,(14,33):7,(15,33):7,
     (16,31):8,(16,30):8,(17,30):7,(17,29):7}
for (x,y),v in ARM.items(): O[y,x]=v
# (1b) vuist ronder en groter dan de arm, zoals in het model: dezelfde drempel 0,2 als de armboog in r7 ((14,30),(15,30)).
# Modeldekking: (7,29) 0,25 (8,29) 0,22 bovenkant; (2,34) 0,38 (2,35) 0,32 (3,36) 0,45 linksonder; (12,36) 0,23 rechteronderlob.
for (x,y),v in {(7,29):6,(8,29):6,(2,34):1,(2,35):1,(3,36):1,(12,36):1}.items(): O[y,x]=v
# oude randpixels die nu binnen de vuist liggen -> vlak (licht boven, schaduw linksonder)
for (x,y),v in {(7,30):15,(8,30):15,(3,34):8,(3,35):7}.items(): O[y,x]=v
# (1b) vuist ronder en groter dan de arm, zoals in het model: dezelfde drempel 0,2 als de armboog in r7 ((14,30),(15,30)).
# Modeldekking: (7,29) 0,25 (8,29) 0,22 bovenkant; (2,34) 0,38 (2,35) 0,32 (3,36) 0,45 linksonder; (12,36) 0,23 rechteronderlob.
for (x,y),v in {(7,29):6,(8,29):6,(2,34):1,(2,35):1,(3,36):1,(12,36):1}.items(): O[y,x]=v
# oude randpixels die nu binnen de vuist liggen -> vlak (licht boven, schaduw linksonder)
for (x,y),v in {(7,30):15,(8,30):15,(3,34):8,(3,35):7}.items(): O[y,x]=v
# (2) rugrots x 45-48, rij 9-16: tint per pixel uit de gemeten modelhelderheid (5 >= 140, 4 >= 115, anders 3); de knik
# (modellijn) alleen waar het model daar ook donker is (hel < 120), anders valt hij in de lichte voorkant.
# Gevolg: lichte wig die naar linksonder smaller wordt (rij 9-11 x 45-47, rij 12-13 x 45-46, rij 14-15 x 45) = schuin, zoals het model.
for y in range(9,17):
    for x in range(45,49):
        if R7[y,x] in (0,1): continue
        knik=lf[y,x]>=0.18 and R7[y,x]==2 and hel[y,x]<120
        if knik: O[y,x]=2; continue
        h=hel[y,x]; O[y,x]=5 if h>=140 else 4 if h>=115 else 3
# losse pixels: (45,9) blijft de linkerrandlijn van r7 (2); (47,11) gemeten 130 -> 5, sluit aan op de lichte wig;
# knik doorverbonden via (47,13) (grens licht 135 | donker 101 in het model); (3,34) -> 7, sluit aan op de schaduw linksonder.
O[9,45]=2; O[11,47]=5; O[13,47]=2; O[34,3]=7
np.save('r7b.npy',O)
p=Image.fromarray(O.astype('uint8'),'P'); p.putpalette(r7.getpalette()); p.save('gnometrotter_rock.png',transparency=0)
d=np.argwhere(O!=R7); print(len(d),'px anders dan r7:',[(x,y,R7[y,x],O[y,x]) for y,x in d])
for y in range(7,19): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in O[y,40:52]),'  ',''.join('.' if v==0 else '%x'%v for v in R7[y,40:52]))
for y in range(27,36): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in O[y,0:20]),'  ',''.join('.' if v==0 else '%x'%v for v in R7[y,0:20]))
