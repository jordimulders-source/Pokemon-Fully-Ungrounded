# Eindkeuring Nocticue r3: kleur, schaduw, Dragonfly Cave-uitvoering (19 nov)
Vergeleken op 8× met Teddiursa, Aipom, Pichu, Smoochum, Plusle, de oude sprite en het model (`naast_gen3_8x.png`, `contrast_1x_2x.png`, `sprite_12x_raster.png`, `onderkant_sprite_vs_model.png`). Coördinaten (x,y) in frame 1; indexen van `normal.pal` (1 zwart, 2/3/4/5 lila 64/100/137/180, 6/7 crème 199/237, 9 oogring, A iris, B roze, C wit, D bruin, E pupil). Voorstel toegepast als preview (niet in de sprite): `voorstel_reparaties_8x.png`, 56 px, vorm en lijnloop ongewijzigd.

Goed: lila-stappen ±37–43 (Taillow/Teddiursa-niveau), hooglichtkap 5 linksboven op de kop, gekleurde selout 3→2→1 over de kopbovenrand, geen lichte kleur op de buitenrand, zwartaandeel 0,21 (binnen de band), leest op 1× op licht en donker.

| # | Prio | Zone, pixels | Probleem | Reparatie (tint per pixel) |
|---|---|---|---|---|
| 1 | hoog | armen: rechterarm x32 y42–48; linkerarm (23,42),(23,43),(22,44–46),(21,47–48), (23,44),(22,47) | Licht omgekeerd: de arm aan de schaduwkant heeft een volle kolom hooglicht 5, de nabije arm aan de lichtkant geen; samen met de zwarte lijnen geeft x31–37 banding (1-5-4-1-3-3-1). Oude sprite had het andersom. | x32 y42–48: 5→4. Linkerarm: genoemde 4→5, (23,44),(22,47) 3→4. Kniehooglicht (31–32,49–50) blijft. |
| 2 | hoog | voetstrook (21–24,54) | Onderkant (grondcontact) in hooglicht 5; model en oude sprite: donker lila. | 5→3. |
| 3 | midden | staartkrul rechts (49,35–38) | Hooglicht 5 rondom de krul (links, boven én rechts) = pillow shading. | 5→4 (oude sprite: 4/3 rechts). |
| 4 | midden | binnenlijnen romp x34 y43–48, x31 y43–47 | Drie volle zwarte verticale lijnen op het lijf (kooi-effect); binnenlijn tussen lila delen hoort in de omlijningsbasis, taps. | 1→2; uiteinden (y42, y48/49) zwart laten. |
| 5 | midden | verre oog x17–18 y31–34 | Roze B los verspreid om en om met 9: (17,31),(18,33),(17,34) leest als ruis. | (17,31) B→E, (17,32) 9→E, (17,33) 9→A, (18,33) B→A, (18,34) 9→B: pupil-iris-reflectie zoals het nabije oog. |
| 6 | midden | linkerkoprand (14,30),(15,31),(16,32) | Zwart blokje midden in de gekleurde selout aan de lichtkant (2-2-2-1-1-1-2-2), plus 2 px zwartklont (15–16,31). | 1→2 (oogleden (16,30),(16,31) blijven zwart). |
| 7 | midden | rechterwang 6-rand y25–35 | 1 px brede diagonaal 6 evenwijdig aan de lila rand = banding; sikkel wordt niet breder naar de kaak. | (33,32),(32,33),(29,36),(28,37) 7→6. |
| 8 | laag | nabije oog (27,31) | Losse roze B direct onder de glans, tussen glans en pupil. | B→E. |
| 9 | laag | rompzijde (35,47–48); kin rechts (32,38),(29,38),(28,39) | Basis 4 als vlakje in schaduwzone. | 4→3. |
| 10 | laag | streep (24,28); arm (22,48); wangrand (17,35) | Streep springt 1 px; dubbele zwarte pixel; oogring 9 op de buitenrand. | (24,28) 4→3; (22,48) 1→3; (17,35) 9→2. |

Ter info voor Jordi (geen reparatie): het verre oor heeft één bruine D-pixel als binnenkant (16,27), passend als verre/donkere kant; crème heeft geen bruikbaar hooglicht (8 is 14 lichter dan 7 en wordt niet meer gebruikt).

**Eindoordeel:** nu goed maar niet uitstekend, door punt 1–2 (omgekeerd licht op de armen en de voet). Na reparaties 1–7 is het een uitstekende Gen 3-sprite: consistente lichtbron linksboven, sikkels die de vorm volgen, nette selout en ogen op Gen 3-niveau, naast Teddiursa/Aipom niet te onderscheiden in uitvoering.
