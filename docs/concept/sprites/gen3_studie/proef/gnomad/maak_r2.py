# Gnomad ronde 2: bouwt op na.png (r1). Alleen gerichte pixellijsten + paletkleuren buiten het gezicht.
from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(D,'na.png')); px = im.load()
opx = im.copy().load()
def rij(y, x0, x1, c): return [((x,y),c) for x in range(x0, x1+1)]
edits = {
 # MUTS: 4-band rechts onder de muts (rij 24-27) opgenomen in de schaduwzone
 'muts_onderrand': rij(24,27,28,3)+rij(25,23,34,3)+rij(26,26,34,3)+rij(27,28,31,3),
 # ROMP: slagschaduw van de snor als één zone (7) direct onder de snor
 'romp_snorschaduw': rij(39,16,21,7)+rij(40,14,31,7)+rij(34,30,33,7)+rij(35,30,34,7),
 # ROMP: schaduw rechts in twee harde zones: 7 en daarbuiten een diepe 6-zone
 'romp_rechts': rij(35,39,40,6)+rij(36,38,39,6)+rij(37,38,40,6)+rij(38,38,42,6)+rij(39,38,41,6)+[((38,40),6)],
 # HANDEN: diepste schaduw (6) in de hoek rechtsonder van de schaduwsikkel
 'handen': [((9,44),6),((8,45),6),((9,45),6),((8,46),6),((48,45),6),((46,46),6),((47,46),6)],
 # BROEK: lichtzone linksboven op de bolling, schaduwzone rechts, losse vlekjes weg
 'broek': rij(49,23,26,'b')+rij(50,23,25,'b')+rij(51,22,24,'b')+rij(48,30,32,'a')+rij(48,34,37,9)+[((37,47),9)]
          +rij(49,33,35,9)+rij(50,32,33,9)+rij(51,30,31,9),
 # BEEN LINKS (dichtbij): licht aan de voorkant, schaduw achter/onder
 'been_links': [((20,53),'a'),((21,53),9),((15,54),'b'),((16,54),'b'),((20,54),9),((19,55),'a'),((20,55),9),
                ((16,56),'a'),((17,56),'a'),((18,56),'a'),((19,56),9),((20,56),9)]+rij(57,16,20,9)+rij(58,16,20,9),
 # BEEN RECHTS (veraf): donkerder, grondtint 9 met licht (a) aan de voorkant
 'been_rechts': [((36,54),'a'),((37,54),'a'),((38,54),9),((39,54),9),((38,55),9),((39,55),9),
                 ((35,56),'a'),((36,56),'a'),((37,56),'a'),((38,56),9),((39,56),9),
                 ((34,57),'a'),((35,57),'a'),((36,57),'a'),((37,57),9),((38,57),9),((39,57),9)]+rij(58,35,38,9),
}
H = {'a':10,'b':11}
for zone, lst in edits.items():
    n = 0
    for (x,y),c in lst:
        c = H.get(c,c); assert px[x,y] != 0, (zone,x,y)
        if px[x,y] != c: n += 1
        px[x,y] = c
    print(zone, n)
pal = im.getpalette()
for i,rgb in {3:(122,92,182), 4:(180,148,230), 5:(218,198,255),   # lila: diepere schaduw, grotere stappen
              9:(44,92,140), 11:(140,204,244)}.items():               # blauw: donkerder schaduw, helderder licht
    pal[i*3:i*3+3] = list(rgb)
im.putpalette(pal); im.save(os.path.join(D,'na_r2.png'))
