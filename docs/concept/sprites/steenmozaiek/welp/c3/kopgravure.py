# Kopgravure (Jordi 15 nov: "doe ook een licht lijnen patroon in het hoofd, mogelijk cirkelend om de bovenkant van de ogen heen").
# Groef = 'k' (op het lichte voorhoofd tint 3, elders 2) met de gewone lichte lip onder/rechts. Coordinaten (x,y).
WENKBRAUW=[(12,24),(13,24),(14,25),(15,25),(16,25),(17,24),(18,23),(19,23),(20,23),(21,23),(22,24)]  # boog over beide ogen, dip op de neusrug
LIJNEN={
 # A: wenkbrauwboog die achter het oog omhoog doorloopt naar de oorbasis
 'A': WENKBRAUW+[(23,23),(24,22)],
 # B: wenkbrauwboog die achter het oog omlaag om het oog heen loopt en eindigt in een kort staartje naar achteren
 #    (Chavin-oog met 'staart'); het gezicht-rechthoekje (x<=23, y26-29) blijft onaangeroerd
 'B': WENKBRAUW+[(23,25),(24,26),(24,27),(24,28),(25,29)],
}
