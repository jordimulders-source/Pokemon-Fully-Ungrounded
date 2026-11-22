# Handreparaties r1: (rij, kolom, letter, zone, reden). Alleen wat de reductie kapotmaakte, steeds naar het model (natieve coördinaten in de reden).
HAND=[
 # hoofdband
 (8,10,'D','hoofdband','trap links: verloren trede van natieve rij 11 (kol 15-17 DDD) terug, anders gat in de traplijn'),
 (7,28,'D','hoofdband','grote trap rechts: verloren trede van natieve rij 11 (kol 36-38 DDD) terug'),
 (7,29,'D','hoofdband','idem'),
 (9,13,'l','hoofdband','losse donkere stip (natief 2 px op 13,19-20, verkleind tot 1 px ruis) weg'),
 (2,13,'l','bovenplaat','losse middentint-stip in het lichte bovenvlak (natief 3,19 M) weg'),
]
HAND+=[
 (21,22,'d','gezicht','mond: rechter hoek (natief 31,29 d) viel weg met kolom 29; terug zodat de mond een boogje d-mmmm-d is zoals het model'),
 (17,9,'d','gezicht','linker buitenrand: losse zwarte pixel tussen selout (d/r) -> selout, geen zwart/selout om en om'),
]
HAND+=[
 # linkerarm: trappen van boven- en onderrand regelmatig (schrappen van kolom 1/3/6 gaf trede 0-2-0); model = rechte diagonaal (natief 1 kol/rij)
 (31,3,'d','armen','bovenrand: trede 30-31 (2x kol 4) -> 1 per rij'),(31,4,'l','armen','idem, wordt vulling'),(32,3,'l','armen','idem'),
 (31,9,'m','armen','onderrand 1 per rij (was 9-10 dubbel)'),(32,8,'m','armen','idem'),(32,9,'K','armen','idem'),
 (33,7,'m','armen','idem'),(33,8,'K','armen','idem'),(34,6,'m','armen','idem (34-35 stonden op dezelfde kolom)'),(34,7,'K','armen','idem'),
 # rechterarm
 (26,37,'K','armen','bovenrand rechterarm/kopzijde: losse selout tussen zwart -> zwart (zoals de rest van die rand)'),
 (28,39,'K','armen','idem'),
 (36,41,'K','armen','binnenrand (onderkant) rechterarm: zwart zoals het model (natief K); was selout door de randregel'),
 (39,42,'K','armen','idem'),
 (38,42,'K','armen','idem'),
 (36,45,'l','armen','eind van de arm: losse uitstulping (37,46) kwam doordat kolom 66 wegviel; model = ronde kop over natieve rij 52-57'),
 (36,46,'K','armen','idem: rand 3 rijen op kolom 46 i.p.v. 1'),
 (33,14,'d','lijf','linker lijfrand: losse zwarte pixel in de selout-kolom -> selout'),
]
HAND+=[
 # ogen: ring overal één tint (d), streep D; model mengt M/d (op 48 px gaf dat losse grijze stipjes). Vorm = model, alleen kleur.
 (14,13,'d','gezicht','ring linkeroog boven (door het rood heen): m -> d, één ringtint'),
 (15,12,'d','gezicht','ring linkeroog: m -> d'),(15,14,'d','gezicht','idem'),(16,16,'d','gezicht','idem'),(17,10,'d','gezicht','idem'),
 (14,25,'d','gezicht','ring rechteroog boven (door het rood heen): m -> d'),(14,26,'d','gezicht','idem'),
 (15,24,'d','gezicht','ring rechteroog: m -> d'),(15,27,'d','gezicht','idem'),(15,28,'d','gezicht','idem'),
 (16,22,'d','gezicht','idem'),(17,22,'d','gezicht','idem'),(17,29,'d','gezicht','idem'),
 (19,24,'l','gezicht','onderkant rechteroog: anti-aliaspixel weg, ring = d zoals het linkeroog'),(19,27,'l','gezicht','idem'),
 (20,24,'d','gezicht','onderkant rechteroog: m/D/D/m -> dddd (zelfde ringtint, streep blijft de enige D)'),
 (20,25,'d','gezicht','idem'),(20,26,'d','gezicht','idem'),(20,27,'d','gezicht','idem'),
 # bovenplaat: bovenvlak lichtste tint (licht van boven/linksboven), links h zoals het model, rechts l
 (1,16,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,17,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,18,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,19,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,20,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,21,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (1,22,'h','bovenplaat','bovenvlak: h links (model: h links, l rechts; nu één vlak i.p.v. losse stipjes)'),
 (2,10,'h','bovenplaat','idem'),
 (2,11,'h','bovenplaat','idem'),
 (2,12,'h','bovenplaat','idem'),
 (2,13,'h','bovenplaat','idem'),
 (2,14,'h','bovenplaat','idem'),
 (2,15,'h','bovenplaat','idem'),
 (2,16,'h','bovenplaat','idem'),
 (2,17,'h','bovenplaat','idem'),
 (2,18,'h','bovenplaat','idem'),
 (2,19,'h','bovenplaat','idem'),
 (2,20,'h','bovenplaat','idem'),
 (2,21,'h','bovenplaat','idem'),
 (2,22,'h','bovenplaat','idem'),
 (5,26,'l','hoofdband','losse middentint-stip in het lichte vlak weg'),
 (7,26,'l','hoofdband','losse hooglicht-stip weg'),
 (30,24,'d','lijf','reliëf: hoek waar de verticale lijn (kol 24) de horizontale (25-29) raakt, was m'),
]
# Toegestane afwijking (Jordi): "de punt in een sprite gefixed kan worden" -> het lijf loopt onderaan taps toe naar de punt (zoals r4).
# Rijen 38-47, kolommen 14-35 (armen niet). Linkerrand 1 kol/rij (17..26), rechterrand 2-1-trap (34..28), zwart aan de onderkant;
# voorvlak l (lijfkleur), zijvlak m, ribbe D doorgetrokken tot de punt; reliëflijnen van het lijf stoppen op rij 39 (onderkant lijf
# in het model). Onderste rijen (42-47) volgen de omtrek van de modelpunt (zelfde breedtes als de kale reductie).
_R={38:'..KKdldllldldlllDmmmK.',
    39:'....KldllldldlllDmmmK.',
    40:'.....KlllllllllDmmmK..',
    41:'......KllllllllDmmK...',
    42:'.......KllllllDmmmK...',
    43:'........KlllllDmmK....',
    44:'.........KllllDmK.....',
    45:'..........KlllDmK.....',
    46:'...........KllmK......',
    47:'............KKK.......'}
PUNT=[(y,14+i,c) for y,r in _R.items() for i,c in enumerate(r)]
