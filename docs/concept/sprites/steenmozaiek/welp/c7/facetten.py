# c7 rots-pass: harde facetvlakken (polygonen, elk één tint), diepere holtes (2), scherpe hooglichtranden (14) op de
# bovenrand van lichte facetten, belijning zwart aan de schaduwkant / gekleurd aan de lichtkant (rots.py).
# Volgorde telt: latere facetten liggen over eerdere. Polygonen in pixelcoordinaten (x,y), hoekpunten inclusief.
FACETTEN=[
 # hals/borst onder de kop: schaduw
 ('hals',3,[(22,30),(31,30),(29,36),(27,40),(22,40)]),
 # holte onder de kin
 ('kin',2,[(22,33),(25,33),(22,36)]),
 # elleboog van de opgeheven poot: licht vlak
 ('elleboog',5,[(21,40),(26,40),(26,42),(24,43),(21,43)]),
 # onder de elleboog tot de voorpoot: schaduw
 ('onderarm',3,[(21,44),(27,44),(27,47),(21,47)]),
 # opgeheven poot (voet): bovenvlak licht
 ('poot',5,[(9,42),(15,42),(15,43),(9,43)]),
 # voorpoot: lichte voorkant links, midden, schaduwrand rechts
 ('voorpoot_l',5,[(26,47),(29,47),(29,56),(26,56)]),
 ('voorpoot_m',4,[(30,47),(32,47),(32,56),(30,56)]),
 ('voorpoot_r',3,[(33,47),(33,56)]),
 # verre poot en ruimte tussen de poten
 ('verre_poot',3,[(35,45),(36,45),(36,56),(35,56)]),
 ('tussen',2,[(36,49),(36,56)]),
 # onder de buik
 ('buik',2,[(35,46),(39,46),(37,48),(35,48)]),
 # dij: lichte bovenrand, vlak, schaduwsikkel
 ('dij_boven',5,[(39,47),(45,47),(45,48),(39,48)]),
 ('dij_sikkel',3,[(46,47),(48,47),(48,56),(38,56),(38,55),(46,55)]),
 # achter de dij (naar de staart): holte
 ('achter_dij',2,[(48,53),(48,56)]),
 # rug achter de schouder: schaduwvlak met harde diagonale grens, rugrichel licht
 ('rug_schaduw',3,[(37,42),(46,42),(46,46),(37,46)]),
 ('rugrichel',5,[(39,38),(40,38),(44,42),(41,42)]),
 # achtervoet: bovenvlak licht
 ('achtervoet',5,[(37,58),(44,58)]),
]
# hooglichtranden (14): bovenrand van lichte facetten, met de hand gekozen (bovenkanten van de hoekige vormen)
RANDEN=[(22,40),(23,40),(24,40),          # elleboog
        (9,42),(10,42),(11,42),(12,42),(13,42),(14,42),(15,42),   # opgeheven poot
        (40,47),(41,47),(42,47),(43,47),(44,47),                  # dij
        (40,39),(41,40),(42,41),                                  # rugrichel
        (26,47),(27,47),(28,47)]                                  # voorpoot
