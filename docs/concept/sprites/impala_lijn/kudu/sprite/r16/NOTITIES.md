# Kudu r16: volume in de vacht (A subtiel, B duidelijk)
Jordi (27 nov) op r15: "ik vind hem nog erg effen qua kleur".
Uitgangspunt: `r15/kudu_r15.png`. Script: `sprite/r16.py` (vlakken met hooglicht-ellips/sikkel/pixellijst; per pixel gelogd in `pixelsA.txt`/`pixelsB.txt`), controle `sprite/r16_check.py` (`telling.txt`), vel/studie `sprite/vel16.py`.
Lever: `kudu_r16A.png`, `kudu_r16B.png` (P-modus, index 0 transparant), `_8x`, `normal.pal` (slot 15 nu gevuld), `studie.png`, `vel.png`.

## Studie (anim_front_gba + normal_gba.pal, `studie.png` met toonkaart)
| sprite | vachttinten (lum) | hooglicht | schaduw/sikkel |
|---|---|---|---|
| Stantler | 245/221/214 · 184 · 136 (+lijn 74) | ronde vlek boven-links op de dij; voorkant hals/borst | sikkel achter/onder de dij, onder de buik, gebogen spierlijn schouder→romp. Schaduw is de grootste groep (344 px tegen 311 midden) |
| Ponyta | 241 · 229 · 201 (+lijn 110) | ronde vlek boven op romp/rug, borst | buik, achterkant poten |
| Tauros | 218 · 196 · 154 · 98 | schouderbult en bil | onderkant, gebogen |
| Arcanine | 238 · 196 · 112 | bovenkant vachtplukken | onderkant |
| Girafarig | 213 · 182 · 139 | hals/borst voorkant | buik, dij achter |
| impala / viscacha | 3 tinten + licht op borst/buik | — | — |
- Een vachtvlak heeft 3 tinten, vaak met 1 extra lichte tint op de grootste bolling (Stantler 4–5). Hue schuift naar geel als het lichter wordt (Stantler 37° → 38° → 42/44° → 60°).
- Tintgrenzen zijn bogen die de bolling volgen; geen horizontale banden. Poten: lichte strook in de lengte aan de lichtkant (3–5 px), verre poten in schaduw.
- Daarom het vrije slot gebruikt voor **H = #EAC26A** (lum 196, hue 41°): tussen L (#F8D888, 216, 43°) en M (#D8A850, 172, 39°).

## Per vlak (alleen M-pixels gewisseld; bestaande L/D uit het model blijven)
| vlak | A (subtiel) | B (duidelijk) |
|---|---|---|
| kop, voorhoofd | H-ruitje 2+2 px (x13–15, y19–20) | H-ruit langs de wenkbrauwboog (y18–20) met 1 L-kern (14,19) |
| kop, snuit/wang | H 3+2 px (x14–16, y25–26) | H afgerond (y24–26) met L-kern (15,25); sikkel D aan de schaduwkant van de wang naast de manen (x19–23) |
| hals (strook x19) | H y30–32 | H y30–32 (hals leest duidelijker, Jordi r3: "dat moet duidelijker") |
| borst | H-ring om de bestaande L (x19–21, y41–43) | grotere ring + L (20,42), D onder (21–22,45) aansluitend op de verre poot |
| schouder/bovenarm | H-strook (29,44)→(30,47) gebogen; D oksel (27–28,46), D elleboog (34,44–45),(33,46) | strook (28,43)→(30,49) in de lengte de poot in; oksel (26–28,46); elleboogsikkel x34 y43–45 → (33,45–46) → (32,46), sluit aan op de bestaande D van het model |
| romp | H-ellips onder de bestaande rug-L (boog, laagste punt y37) | H-boog tot y38 in het midden, hoger aan de randen; L-kern y33–35 onder de bestaande rug-L |
| dij | H boven-links op de dij (x46–49, y34–38) tussen de strepen; D-sikkel (52,44),(51,45–46) | H + L-kern (x47–49, y35–38); D-sikkel (52,43–44),(51,45–46),(52,47–48) als verlenging van de bestaande D x52–54 |
| achterpoot nabij | H (51,50),(52,51–52) | H diagonaal (49,48)→(52,52), loopt over in de bestaande L x53 y53–55 |
| verre poten, manen, oren | niet aangeraakt (manen lezen niet effen: l/m/d met eigen opbouw) | idem |

## Controle (`telling.txt`)
- A: 61 px (53 H, 8 D); B: 121 px (84 H, 13 L, 24 D). Alle wissels zijn M → H/L/D.
- Silhouet 0 px; lijnen, strepen W, oog K4 (x15–19 y21–24), neus/mond (x8–12), manen, hoorns, oren: 0 px. Ongewijzigde pixels hebben dezelfde index als r15.
- Nieuwe rechte tintgrenzen ≥ 4 px: A 0; B 1 (lichtstrook voorpoot x30 y46–49, 4 px in de lengte van de poot, zoals Stantlers pootstrook). Geen horizontale grens ≥ 4 px.
- Losse pixels: alleen de twee L-kernen in B (binnen een H-ring, bedoeld).
- Vachtverdeling r15 → A → B: L 31/31/44 · H 0/53/84 · M 390/329/269 · D 183/191/207. Licht (L+H) is 14 % (A) en 22 % (B) van de vacht; Stantler 24 %.

## Zelf gekeken
- Eerste poging (ellipsen per vlak, automatisch) gaf een horizontale H-band over borst + schouder (10 px), een 2×4-blok op het voorhoofd en een D-band van 5 px onder de dij. Daarom borst, schouder, kop en sikkels per pixel gelegd en de romp/dij-ellipsen ronder gemaakt.
- Nog vrij vlak: het middenvlak onder de manen (x22–33, y42–45) en de onderkant van de romp boven de buikschaduw. Dat is de middentoon tussen licht en sikkel; een extra sikkel onder de borst gaf weer een rechte band, dus niet gedaan.
- De bovengrens van de buikschaduw (y44, uit het model, zie r14) is niet aangeraakt.
