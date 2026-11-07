# Eindkeuring poedellarve: kleuren en schaduwen (Dragonfly Cave + Gen 3, verse keurder, 7 nov)

Opdracht van Jordi: "doe toch nog maar een eindkeuring nog qua kleuren, dragonflycave en vergelijking met andere sprites, let op, dit is puur kleuren en schaduwen". Gekeurd zijn **alleen** palet, tinten, contrast, lichtrichting, schaduwvormen, banding, pillow shading, losse tintvlakjes, buitenlijn/selout, glans en de aansluiting op de poedelmot. Vorm, silhouet, pose, lijnplaatsing en ontwerp zijn niet gekeurd (goedgekeurd door Jordi).

Sprite `af/poedellarve.png`: 64×64, geïndexeerd, 10 kleuren + transparant, box x12–51 × y33–62 (40×30). Model `referenties/model_gekozen.png`, gespiegeld vergeleken.
Gelezen: SPRITE_KERN, Spriting Guide in `bronnen/` (Shading rounded surfaces, Shine, splicing-regel 4 "change the direction of the light source", Revamps p. 508), FAKEMON_CHECKLIST §E.
Vellen (scratch): `eindkeurder/vel.png` (8× + 1× licht/donker naast model, poedelmot, Wurmple, Silcoon, Altaria, Seel, Taillow), `zoom.png` (14× met raster + model), `model_kop.png`.

## Palet en helderheid
| Index | RGB | lum | px | rol |
|---|---|---|---|---|
| A | 246,244,234 | 243 | 246 | wit basis/licht |
| 7 | 230,224,212 | 224 | 91 | eerste schaduw |
| D | 218,202,184 | 205 | 47 | tan gezicht |
| 6 | 206,194,182 | 196 | 74 | schaduw |
| 8 | 194,176,162 | 180 | 10 | schaduw gezicht (kinstrook y51–52) |
| 5 | 182,162,152 | 167 | 42 | diepe schaduw, tapse naadeinden |
| 4 | 146,128,120 | 132 | 68 | naden/binnenlijn, onderkant |
| 3 | 104,88,82 | 92 | 77 | binnenlijn + selout |
| 2 | 52,40,36 | 43 | 110 | buitenlijn |
| 1 | 16,8,8 | 10 | 13 | oog, neus, oorkrul |

Stappen wit: A→7 **19**, 7→6 28, 6→5 29, 5→4 35, 4→3 40, 3→2 49. Gezicht: D→8 25.
Referenties (wit/licht, eerste stap licht→schaduw): Altaria-wolk 248→223 (25), Swablu 248→203 (45), Silcoon 238→205 (33), Seel 232→211 (21), Cascoon 226→203 (23), poedelmot 247→215 (32); Taillow 30–35.

| Punt | Oordeel | Meting / pixels |
|---|---|---|
| Kleuren kloppen met het model | voldoet | Model (gespiegeld, gekwantiseerd): wit 240,240,227; schaduw 225,212,196 / 208,195,178 / 195,177,161 / 158,147,131; lijn 111,101,90. Sprite volgt dat (A/7/6/8/5). Tan gezicht D klopt met het tan masker in het model. |
| Helderheidsstappen ±30–40 | voldoet grotendeels | 7→6, 6→5, 5→4, 4→3 = 28–40. Alleen A→7 = 19 is zacht; Seel (21) en Cascoon (23) zitten ook zo laag, dus geen afkeur. Op 1× leest de eerste schaduw nog, net. |
| ≤ 3 tinten per kleurgroep | voldoet met kanttekening | Wit: A/7/6 als vlakken, 5 en 4 vooral als taps naadeinde en onderkant (4 als vlak op y58, x32–49). Feitelijk 4 vlaktinten, zoals Altaria's wolk (248/223/203/167). Gezicht: D/8 = 2. |
| Tintafstand onderling | voldoet niet helemaal (R) | D (205) en 6 (196) liggen 9 uit elkaar, 8 (180) en 5 (167) 13, 8 en 6 16. Door de tint (D H31 S0,16 tegen 6 H29 S0,12) blijft het gezicht net onderscheidbaar; 8 is in de praktijk een vijfde wittint. Klein, alleen ter info. |
| Tintclusters < 3 px | voldoet buiten de oren | Clusterscript (8-buren): 39 clusters < 3 px. In de romp alleen tapse naadeinden ((31,45–46) 5, (35,46–47) 6, (44,50) 6: lijnen lopen taps uit, zoals bedoeld) en de oogglans (20,46). 20 van de 39 zitten in de twee oortjes (x12–28, y34–41), die 3–4 px breed zijn: daar is het onvermijdelijk, maar het linkeroor is onrustig: x13 y36–38 = 6/4/6, (14,39) 5, (15,39) 6, (15,40) 4, (15,41) 6 (wisselend om en om). |
| Glans oog | voldoet | 1 px A op (20,46) linksboven in het oog, rand 3 (19,46–47), (21,47); glans linksboven klopt met Gen 3. |
| Buitenlijn 1 px, geen lichte kleur op de rand | voldoet | Rand alleen 2 en 3 (op donker geen lichte stipjes; enkele A/7 raken de rand alleen diagonaal). |
| Zwart en selout niet om en om | voldoet | Geen 2/3-wisseling binnen één rand; 3 staat in aaneengesloten reeksen. |
| **Lichtrichting** | **voldoet niet** | Zie hieronder. |
| Schaduw als sikkel, geen banding | voldoet grotendeels | Onderkant romp: y55 7 → y56–57 6 → y58 4-lijn boven de voetjes, horizontaal over x29–50. Bij een liggende rups is dat de onderkant van een cilinder en geen banding langs de hele omtrek; de segmenten zelf blijven per stuk wit met tapse naden. Wel vlak: elk segment heeft dezelfde band, geen eigen sikkel. |
| Pillow shading | voldoet niet op één plek | Nabije voorpoot x13–17 y54–55: links 7 ((13,54), (13,55), (14,55)), midden A, rechts 7 (17,54–55), onder 6: donker rondom, licht in het midden. Elders niet. |
| Dithering | voldoet | Geen dithering, behalve het om-en-om-effect in het linkeroor (zie clusters). |
| Aansluiting op de poedelmot | voldoet | Zelfde lijnfamilie: 1 identiek (16,8,8), 2 vrijwel gelijk (52,40,36 / 56,40,32), 3/4 in dezelfde warme bruingrijs. Witten zelfde helderheid (243 / 247). Larve is grijzer (verzadiging 0,05–0,18 tegen 0,21–0,32), maar dat volgt haar model; zie ter info. |

## Lichtrichting (de hoofdzaak)
Spriting Guide p. 508: "all Pokémon sprites have their light source in the top left if they're facing left and top right if they're facing right"; bij gespiegelde delen: "change the direction of the light source". De larve kijkt naar links, dus het licht hoort **linksboven**, zoals bij de poedelmot (eindkeuring: "licht linksboven, consistent").

Gemeten na de spiegeling:
- **Selout (3) zit rechtsboven, zwart (2) links.** Rechtsgerichte randpixels in 3: 15 (o.a. (32,42), (32,43), (37,45), (47,50), (49,53)); linksgerichte in 3: 2. Alle linkerranden (kop, borst, poot: 40 px) zijn 2. Per rugbult is de linkerhelling 2 en de rechterhelling 3: (35,44) 2 | (36–37,44) 3; (40,46) 2 | (41–42,46) 3; (44,49) 2 | (45–46,48), (47,49) 3.
- **Linkerrand van kop en poot in schaduwtint 7**: (14,43), (14,44), (15,44); poot (13,54), (13,55), (14,55); linkeroor linkerrand 6 ((13,36), (13,38)).
- Wél al goed voor licht linksboven: de oogglans (20,46), de schaduwkolom 7 rechts van de kop (x30 y49–54) en de donkere achterkant (x44–50 y50–55). De binnenschaduw is dus gemengd; vooral de omlijning wijst nu naar rechtsboven.

Op 1× valt het weinig op (de schaduw komt grotendeels van boven), maar naast de poedelmot en naast echte Gen 3-sprites staat het licht verkeerd, en het is met alleen tinten te herstellen. Geen vorm hoeft te veranderen.

## Reparaties (alleen tinten; vormen en lijnplaatsing blijven)
Verplicht (lichtrichting terug naar linksboven):
1. **Selout naar de linkerkant van de rugbulten** (index 2 → 3): (35,44), (40,46), (44,49).
2. **Rechterhellingen en rechterkant naar zwart** (index 3 → 2): (32,42), (32,43), (37,45), (43,47), (47,50), (49,53), (50,54). De topjes (30–31,40), (32,41), (36–37,44), (41–42,46), (45–46,48), (47,49), (48,51), (49,52) en de kopkruin (18–21,38) blijven 3 (boven = licht). Controleer daarna dat 2 en 3 op elke rand in één overgang wisselen, niet om en om.
3. **Selout linksboven op de kop** (index 2 → 3): (14,41), (14,42), (13,43). Verder naar beneden (vanaf (13,44), snuit en kin) blijft 2.
4. **Linkerrand kop licht** (index 7 → A): (14,43), (14,44), (15,44).
5. **Pillow op de nabije voorpoot weg** (index 7 → A): (13,54), (13,55), (14,55). De 7 rechts ((17,54), (17,55)) en de 6 onderaan blijven: schaduw rechtsonder.

Aanbevolen (niet nodig voor PASS, wel netter):
6. Linkeroor rustiger, licht links: (13,36) en (13,38) 6 → 7; (14,39) 5 → 6. Dan loopt de schaduw van licht (links) naar donker (rechts, x15) in plaats van om en om.
7. Eerste schaduwstap iets steviger: paletkleur 7 van 230,224,212 naar **226,216,200** (lum ±218, A→7 = 25, 7→6 = 22, zoals Altaria/Cascoon). Raakt alle 91 px van 7 tegelijk, geen pixelwerk.

Na 1–5 opnieuw: clusterscript, randtelling (3 vooral linksboven, 2 rechts en onder) en 8× naast de poedelmot.

## Ter info voor Jordi (geen FAIL)
- De larve is grijzer en minder geel dan de poedelmot (verzadiging tot 0,18 tegen 0,32 bij de mot). Dat klopt met jouw model, dus het blijft zo; wil je dat ze als lijn warmer bij elkaar horen, dan kunnen 6/5/4 iets naar crème (bv. 6 → 208,192,170, 5 → 182,160,140, 4 → 148,126,110). Dat is een keuze, geen fout.
- Het gezicht (D) en de lichaamsschaduw (6) liggen dicht bij elkaar; in het model ook.

Oordeel: FAIL
