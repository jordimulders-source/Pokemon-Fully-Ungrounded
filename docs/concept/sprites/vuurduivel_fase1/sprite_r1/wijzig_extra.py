zet(17,34,'W','ver oog: oogwit onder (model Wk, oogwit loopt schuin door naast de pupil)')
zet(22,38,'p','tong: model MM/pp, tong 4 breed zoals het model')
# --- rechterhoorn: reductie liet hem opgaan in het haar; omlijning en lichtstreep naar de natieve cellen sx24-28, y21-25
zet(26,21,'R','rechterhoorn: punt (model p#/rr, donkere rand)')
zet(25,22,'R','rechterhoorn: linkerrand (model R in Rp)')
zet(26,22,'p','rechterhoorn: lichtstreep (model p)')
zet(27,22,'#','rechterhoorn: rechterrand zwart (model #r)')
zet(24,23,'R','rechterhoorn: linkerrand (model bR)')
zet(25,23,'p','rechterhoorn: lichtstreep (model rp/pp)')
zet(26,23,'r','rechterhoorn: vulling rood')
zet(27,23,'#','rechterhoorn: rechterrand zwart (model #r)')
zet(24,24,'R','rechterhoorn: linkerrand (model mR)')
zet(25,24,'p','rechterhoorn: lichtstreep (model pp)')
zet(26,24,'r','rechterhoorn: vulling rood')
zet(27,24,'#','rechterhoorn: rechterrand zwart (model r#)')
# --- linkerhoorn
zet(14,24,'R','linkerhoorn: lichtkant gekleurde selout i.p.v. zwart (model .R)')
zet(18,24,'R','donkere lijn onder de linkerhoorn in haarkleur i.p.v. mondbruin (model MM = donkerrood)')

# --- nabij oog: los wit reepje links van de pupil weg (1 natieve px), lid en oogwit naar natieve cellen sx25-28, y31-33
zet(24,33,'m','nabij oog: los wit reepje (1 natieve px) weg, leest als tand')
zet(25,31,'#','nabij oog: bovenlid loopt over de pupil (model m#)')
zet(28,31,'#','nabij oog: bovenlid rechts (model #m)')
zet(28,33,'W','nabij oog: oogwit rechtsonder (model Wl/#m, wit met lichte rand)')
# --- linkerbeen/hoef: de randregel maakte het dunne been zwart; naar natieve cellen sx20-26, y55-61
zet(20,55,'B','linkerdij: bruin (model kB/B#)')
zet(25,57,'B','linker onderbeen: bruin (model BB/BB)')
zet(26,57,'#','linker onderbeen: rechterrand (model B#)')
zet(22,58,'B','linkervoet: bruin (model #B/BB)')
zet(21,59,'b','linkervoet: lichtkant gekleurde selout (model bb/BB)')
zet(22,59,'B','linkervoet: bruin (model BB/BB)')
zet(22,60,'k','linkerhoef: lichtbruin (model kk/kk)')
# --- rechter onderbeen/hoef: naar natieve cellen sx34-38, y58-62 (bruin 3 breed zoals het model)
for y,rij in ((58,'#BBB#'),(59,'bkkB#'),(60,'bbbb#'),(61,'bkkB#'),(62,'####.')):
    for i,c in enumerate(rij): 
        if R[y][34+i]!=c: zet(34+i,y,c,'rechterbeen/hoef: naar model (rij %s, lichtkant bruin, donkere hoefband y60)'%rij)
# --- losse zwarte pixels in het haar/de hoorns naar donkerrood (zelfde plek als de modellijn)
zet(19,19,'R','haarrand linksboven: zwart (randregel) -> donkerrood zoals de rest van de vlamrand')
zet(17,24,'R','linkerhoorn: lijn rechts van de hoornpunt (model ##) in donkerrood i.p.v. losse zwarte pixel')
zet(24,25,'R','rechterhoorn: linkerrand loopt door (model m#) in donkerrood i.p.v. losse zwarte pixel')
zet(37,31,'d','rechteroor: binnenlijn (model ##/dd) in donkere vlaktint i.p.v. losse zwarte pixel')
# --- staartpunt: oude (gereduceerde) vlampunt wissen, schoppenpunt uit pijl.py erover (toegestane afwijking)
from pijl import pijl
for y in range(34,47):
    for x in range(40,54):
        if R[y][x] in 'RrOYp' : zet(x,y,'.','staartpunt: oude vlampunt gewist (wordt schoppenpunt)')
for (x,y),c in pijl().items(): zet(x,y,c,'staartpunt: schoppenpunt (toegestane afwijking Jordi)')
