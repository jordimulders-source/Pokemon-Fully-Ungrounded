# Eindkeuring poesrups r4 (Dragonfly Cave + Gen 3): kleur, schaduw en belijning

Gekeurd: `kleur_r4/poesrups.png` (13 nov). Vorm, lijnplekken, ogen en kam zijn bevroren en niet gekeurd.
Vel en scripts: `keuring/` (`vel.py` → `vel_1x.png`, `vel_2x.png`, `vel_3x.png`; `meet.py` → `meet_uitvoer.txt`; `proef.py` → `proef_reparaties.png`).

## Eindoordeel: **PASS** (met 2 kleine, optionele tintreparaties)

## Eerste indruk (blind, vóór de notities van de maker)
- Op 1× (licht, donker en gras) leest hij meteen als één witte, harige bult met een staart: de kop is het lichtst, de rug loopt naar rechts en naar onder af in crème. Hij valt niet uit de toon naast Silcoon, Dewgong, Altaria en Castform en hoort zichtbaar bij de larve en de mot (zelfde warme wit, zelfde zachte bruine lijn).
- De omlijning is zachter dan bij de echte Gen 3-sprites (die hebben bijna-zwart 16), maar gelijk aan die van de larve; op een witte achtergrond blijft de kam leesbaar.
- Wat opviel: (a) een wit eilandje in het achterste segment, vlak tegen de donkere rechterrand en onder de schaduw van de kam; (b) de onderrand in het midden is lichter dan het gezicht links en het achterlijf rechts ervan; (c) de kop is één groot wit vlak, maar dat stoort op 1× niet (Dewgong en Altaria doen hetzelfde).

## Meetresultaten (`meet_uitvoer.txt`)
| Meting | Resultaat |
|---|---|
| Kleuren | 8 + transparant (max 16) |
| Vlaktinten wit (luma, px) | A 243 (406) · 7 213 (95) · 6 187 (191) · 5 157 (129); lijn 4 127 (101) · 3 92 (54) · 2 43 (77); ogen 1 (5) |
| Stappen vlaktinten | 30 · 26 · 31 (norm ±30–40; Silcoon 18–27, Dewgong 23–42, Altaria 20–25) |
| Lichtrichting (gem. luma vlak per kwadrant) | linksboven 234 · rechtsboven 216 · linksonder 209 · rechtsonder 191 |
| Verloop per kolomband (rij 38–57) | 230 · 230 · 229 · 226 · 207 · 208 · 199 · 190 · 196 · 191 · 157 (kop → staartpunt) |
| Verloop per rijband | 243 · 219 · 230 · 233 · 228 · 210 · 183 · 172 |
| Buitenrand | 147 px, alleen index 2 (72), 3 (35), 4 (40); geen lichte kleur op de rand, geen open randen |
| Buitenrand per zijde | boven: 3 (links) → 4 (kam) → 3 (staart); links: 3 tot rij 47, daarna 2; onder: overal 2 |
| Vlakclusters < 3 px | 0 buiten het benoemde lijnwerk, de pootjes en de oogglans (16,55) |
| Gem. luma hele sprite | 186 (larve 172, Silcoon 176, Dewgong 193, Castform 173) |

## Per eis
| Eis | Oordeel | Toelichting |
|---|---|---|
| Lichtrichting linksboven | PASS | Kwadranten en kolombanden lopen netjes af van linksboven naar rechtsonder. |
| Schaduw als sikkel die de vorm volgt | PASS | Per segment een schuine grens die naar de staart hoger komt; geen rechte grens meer. Zie reparatie 1 en 2 voor twee plekken waar de sikkel onderbroken is. |
| ≤ 3–4 tinten per kleurgroep + omlijning | PASS (op de grens) | 4 vlaktinten (A, 7, 6, 5); 4 alleen als lijn. Geen aparte hooglichttint, dus niet meer dan Silcoon/Dewgong. |
| Helderheidsstappen ±30–40 | PASS | 30/26/31; de 26 ligt binnen wat de echte witte sprites doen. |
| Geen banding | PASS | Eén restje: 7-kolom (6,46–49) langs de linkerrand, 4 px; op 1× niet te zien. |
| Geen pillow shading | PASS | Lichte kant heeft geen donkere binnenrand; schaduw ligt alleen rechts en onder. |
| Geen dithering, losse pixels, tintvlakjes < 3 px | PASS | 0 buiten benoemd lijnwerk en glans. |
| Buitenlijn 1 px, donker aan de schaduwkant, selout aan de lichtkant, niet om en om | PASS | De wisseling 4/3/2 aan de rechterkant hoort bij de afzonderlijke krullen (boven 4, opzij 3, onder 2), niet bij één rand. |
| Binnenlijnen in een donkere tint van het vlak, taps | PASS | Naden 6 in het wit, 5 in de schaduw; loklijnen 5/4. |
| ≤ 16 kleuren | PASS | 8. |
| Leest op 1× als één geheel met volume | PASS | Op alle drie de achtergronden. |
| Past tussen echte Gen 3-sprites en in de familie | PASS | Zelfde wit, lijnkleuren en warmte als larve en mot. |
| Toon en lichtverdeling van het model | PASS | Model: kop boven het lichtst, schaduw onder de pony, rug onderaan en staart crèmegrijs. Komt overeen. |
| Dragonfly Cave (hooglicht, vacht, wol mat) | PASS | Veel van de lichtste tint (R/S-stijl), geen glanspixel op de wol, vachtgrens gekarteld via de loklijnen. |

## De 6 zwakke punten van de maker
1. **Begin van de 7-wiggen is 1 px breed:** acceptabel. Leest op 1×/2× als een taps aanzetje van de schaduw naast de naad.
2. **Kop is een groot wit vlak:** acceptabel. Wol is mat; een extra hooglichttint zou hem plastic maken. Het volume komt van de sikkel rechts en de schaduw onder de pony.
3. **Kam ongewijzigd:** acceptabel. Een eigen schaduwkant per krul geeft vlekjes van 1–2 px.
4. **Onderrand midden (x23–37) nog het oude patroon:** klein punt, zie reparatie 2. De loklijnen zelf zijn in orde.
5. **7-kolom (6,46–49):** acceptabel, laten staan. Twee pixels eruit halen geeft een cluster van 2 px.
6. **Stap 7→6 is 25,6:** acceptabel; valt binnen de echte sprites en houdt 6 bij de larve.

## Reparaties (optioneel, alleen tint; op prioriteit)
Geproefd in `keuring/proef_reparaties.png` (r4 · R1 · R2 · R1+R2): het verschil is klein maar op 2× zichtbaar; de achterkant en de onderkant krijgen iets meer volume. Geen clusters < 3 px als gevolg.

1. **Wit eilandje in het achterste segment** (ligt onder de kamschaduw van rij 44 en tegen de donkere rechterrand; licht onder schaduw aan de schaduwkant). Van **A naar 7**: (41,45), (42,45), (42,46), (43,46), (42,47), (42,48).
2. **Onderrand midden sluit niet aan op gezicht (5) en achterlijf (5).** Van **6 naar 5**: rij 57: (24,57), (25,57), (26,57), (28,57), (29,57), (30,57), (31,57), (32,57), (35,57), (36,57); rij 58: (32,58), (33,58), (36,58), (37,58). De loklijnpixels (27,57) en (34,57) zijn al 5 en lopen daardoor aan hun onderste pixel in de schaduw uit; de lijnen in 4 blijven staan.

## Ter info voor Jordi (ontwerp)
- De omlijning van de hele familie (donkerste lijn 43, bovenrand 127) is zachter dan bij de echte Gen 3-sprites (16). Bij deze drie is dat consequent; alleen ter info.
