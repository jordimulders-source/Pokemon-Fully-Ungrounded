# Kopgravure (Jordi 15 nov: "doe ook een licht lijnen patroon in het hoofd, mogelijk cirkelend om de bovenkant van de ogen heen").
# Groef = 'k' (op het lichte voorhoofd tint 3, elders 2) met de gewone lichte lip onder/rechts. Coordinaten (x,y).
WENKBRAUW=[(12,24),(13,24),(14,25),(15,25),(16,25),(17,24),(18,23),(19,23),(20,23),(21,23),(22,24)]  # boog over beide ogen, dip op de neusrug
# c4 (Jordi: "doe nog een lijn erbij naar de bovenkant van het hoofd tussen de oren in, 2 bijvoorbeeld"):
# twee kerflijnen vanaf de oogboog omhoog naar de kruin, licht naar achteren hellend (de kop is 3/4 gedraaid).
KRUIN=[(15,24),(15,23),(16,22),(16,21), (19,22),(19,21),(20,20)]
LIJNEN={
 # A: wenkbrauwboog die achter het oog omhoog doorloopt naar de oorbasis
 'A': WENKBRAUW+KRUIN+[(23,23),(24,22)],
 # B: wenkbrauwboog die achter het oog omlaag om het oog heen loopt en eindigt in een kort staartje naar achteren
 #    (Chavin-oog met 'staart'); het gezicht-rechthoekje (x<=23, y26-29) blijft onaangeroerd
 'B': WENKBRAUW+KRUIN+[(23,25),(24,26),(24,27),(24,28),(25,29)],
}
