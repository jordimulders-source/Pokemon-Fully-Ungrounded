# Eindkeuring r3 (Dragonfly Cave + omlijningsronde): fruitvampier, alleen `A_geel`

Jordi koos A_geel ("A_geel naar de eindkeuring"); A0 en A zijn niet gekeurd.
Getoetst: alleen de uitvoering (trouw aan `model/model.png` + Gen 3), geen herontwerp. Maatstaf: de goedgekeurde fase 2 (`emolga_evo/af/model.png`, zelfde palet) en echte Gen 3-sprites, **gemeten** met `meet_rand.py` (kleur van elke buitenrandpixel per kant).
Vel: `vel.png` (A_geel 8× met gemarkeerde pixels + 1×/3× op licht en donker naast fase 2, Murkrow, Golbat, Sableye, Gligar, Taillow, Umbreon). Script: `vel.py`.

## Oordeel
**A_geel: BIJNA.** Hoofdvraag goed (leest op 1× meteen als het model: hangende vleermuis in gesloten zwarte vleugels met gele naad, witte kop onderaan, oren omlaag, geel voorhoofdvlekje). De omlijning is grotendeels al goed (links 2, rechts zwart, zoals fase 2). Over: 5 kleine, benoemde omlijningsreparaties (±35 px), geen silhouetwijziging.

## Gidsregels waarop geoordeeld is (letterlijk, `dragonflycave_spriting_guide.txt`)
- r. 96–98: *"The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites."*
- r. 421–423: *"we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."*
- r. 427–429 + 453–455: *"lighter pixels on the inside of the outline are a far better idea"* · *"Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts … place pixels of the outline highlight color on the inside of the outline rather than the outside."*
- r. 375–377: lichtere pixels aan de buitenkant van de lijn geven *"very visible, horrendously ugly colored "dots" around the outline"*.
- r. 405–406 (Scyther-revamp): zwart is *"for the outline and the very deepest shadows"*.
- r. 117–121 (regel 4): *"The outlines must be reasonably dark."*

## Metingen (buitenrand, links/boven = lichtkant | rechts/onder = schaduwkant)
| sprite | lichtkant | schaduwkant |
|---|---|---|
| **A_geel r3** | 2 (42): 44 · zwart: 24 · **3 (70): 26** · a (154): 5 | zwart: 83 · 2: 7 · 3: 4 · geel 5: 2 |
| fase 2 (goedgekeurd) | 2: 104 · zwart: 32 · **3: 0** | zwart: 113 · 2: 17 |
| Murkrow (zwart lijf) | darkest blauw 48: 50 · zwart: 48 · schaduwtint 69: 6 · basistint 104: 1 | zwart: 84 · 48: 20 |
| Umbreon | zwart: 92 · darkest 53: 21 | zwart: 109 |
| Honchkrow | zwart 59 · 48: 56 · 69: 22 | zwart 91 · 48: 44 |
| Zangoose / Swablu / Seel (wit) | lichtkant wit: 145 / 165 / 161 als lijn | zwart |

Conclusie: de **basistint 3** van de zwarte ramp hoort niet op de buitenrand (fase 2: 0×, Murkrow: 1×); de outline base van de zwarte ramp is **2**. Het witte gezicht met **a (154)** als lijn aan de lichtkant is wél Gen 3 (Zangoose 145, Swablu 165, Seel 161): geen fout. Zwarte binnenlijnen (vouwlijn vleugel, vingerlijnen) zijn hier goed: fase 2 en Honchkrow doen dat ook in een zwart lijf, en een lijn in 2 zou in het 2-vlak verdwijnen. Zwartaandeel 15,0 % (fase 2 16,0 %, Gen 3 ±13–26 %).

## Omlijningsronde per onderdeel
| onderdeel | outline base | lichtkant | schaduwkant | binnenlijnen | oordeel |
|---|---|---|---|---|---|
| vuisten/poten | 2 | (28,1) tint 3; rechterpoot (33,4–5) zwart, (33,6) 3 | zwart | knokkels zwart, ok | rep. 1a |
| vleugelpakket | 2 | 2, OH-tint 4 binnen de lijn (x21, r. 26–28) = goed; los 3 op (28,8), (26,11), (26,12), (20,28) | zwart, 1 px | vouwlijn zwart (ok), maar 2×2-blok + gat bij (26–28,15–16) | rep. 1b, 2 |
| gele naad | – | ligt binnen de lijn | (35,7), (35,8) geel óp de buitenrand (open rand) | – | rep. 3 |
| witte kop | a | a (154), Gen 3-conform | zwart | oogvlek binnen | ok |
| oogvlek (leigrijs) | 3 | 3 (=darkste eigen tint van de vlek), ok; maar losse lichte a op (20,46) | zwart | ogen zwart | rep. 4 |
| kruin/voorhoofdgeel | – | – | onderlijn rij 51 zwart, onderbroken door 2 op (24,51) (zwart/donker om en om) | – | rep. 5 |
| linkeroor | 2 | hele linkerrand tint 3 (lichte rand buitenop), binnenin alleen 2 | zwart | – | rep. 1c |
| rechteroor | 2 | linkerrand tint 3 | zwart | binnenoor b, lijn zwart (ok) | rep. 1d |

## Reparaties (benoemd per pixel; niet tekenen, alleen deze pixels; silhouet blijft gelijk)
**1. Outline base aan de lichtkant (gids r. 421–423; fase 2 = 2 op de hele lichtkant).**
- a. Vuisten/poten: (28,1) 3→2 · (33,4) 1→2 · (33,5) 1→2 · (33,6) 3→2. De rechterpoot wordt "2 1" zoals de linker (30–31); lost ook het 2×2-zwartblok (33–34,4–5) op (r. 421–423 "one pixel wide").
- b. Vleugel: (28,8) 3→2 · (26,11) 3→2 · (26,12) 3→2 · (20,28) 3→2. Binnenin blijft 3/4 staan, dus het licht blijft.
- c. Linkeroor: (20,54), (20,55), (20,56), (19,57), (19,58), (19,59), (19,60) 3→2. **Aanbevolen erbij** (gids r. 453–455, highlight ín de lijn): (21,54), (21,55), (21,56), (20,57), (20,58), (20,59) 2→3. Zonder dit wordt het oor één vlak 2; het verschuift alleen de bestaande lichte rand 1 px naar binnen (zoals fase 2: "241", "2441").
- d. Rechteroor: (31,52), (31,53), (31,54), (32,55), (32,56), (33,57), (33,58) 3→2. Binnenin blijft 3/b; het model heeft hier ook een donkere lijn.

**2. Binnenlijn vleugel 1 px en zonder gat (r. 421–423).** Model (16×16-blok, p10): lijn op (25–27,15) en (26–29,16).
- (26,16) 1→4: haalt het 2×2-zwartblok (26–27,15–16) weg (model hier het zwakst: gem. 49).
- (28,16) 3→1: dicht het gat tussen (27,16) en (29,17); model gem. 20, p10 1 = lijn.

**3. Open rand (r. 96–98, outline shadows zwart; zelfde als r2-reparatie (38,41)).** (35,7) 5→1 · (35,8) 5→1. De gele naad begint dan op (35,9), binnen de zwarte lijn; in het model heeft het geel hier een donkere rand.

**4. Lichte/losse pixels (r. 375–377 "colored dots"; hatun runa-les losse zwarte pixel).**
- (20,46) a→3: één lichte pixel op de buitenrand midden in de 3-lijn van de oogvlek.
- (20,35) 1→2: losse zwarte pixel (0 zwarte buren) in het 2-vlak vlak naast de 2-buitenrand: een dubbele lijn 2|1 op één plek.

**5. Kruinlijn (SPRITE_KERN: "nooit zwart en donker om en om op één rand").** (24,51) 2→1: rij 51 is de onderkant van de kruin (schaduwkant) en loopt nu 1-2-1; model rij 51 x23–26 is één donkere lijn. (26,51) blijft geel (voorhoofdvlekje van A_geel).

Na de reparaties: lichtkant alleen 2 (+ a aan het wit, 3 aan de vlek, enkele zwarte hoekpixels), schaduwkant zwart, geen geel/licht op de buitenrand, geen 2×2-zwart behalve in de pupil (Gen 3-oog) en het eindpunt van de vouwlijn (40–41,37–38) waar die de schaduwrand raakt (diepste schaduw, r. 405–406, zoals fase 2).
Controle voor de maker: diff alleen deze pixels, alpha-diff 0, `meet_rand.py` → lichtkant 3 = 0.

## FAKEMON_CHECKLIST (kort)
A1, A2 (oren + vuisten breken de omtrek), A5, B1/B3 (twee ogen, verre oog kleiner), C1 (2 oren, 2 ogen, 2 vuisten), E1, E3: ok. Tinten per groep ≤ 3 + lijn, stappen 28–51 (Taillow ±30–40): ok.

## Ter info voor Jordi (ontwerp, geen fout van de maker)
- **D1 formaat:** 1024 px, terwijl de checklist voor fase 3 1700–2600 noemt en fase 2 (1398 px) groter is. Gevolg van het gekozen smalle hangmodel (±26 px breed); het silhouet is bevroren.
- **B7 mond:** het model toont geen mond; alleen het gele kinstreepje. Zo laten tenzij Jordi iets anders wil.
- **(22,52)** losse zwarte pixel bovenin het linkeroor: het model heeft daar een donkere lijn 1 px verder rechts (x23); mag blijven, of 1→2 als Jordi hem als stip ziet.
- Kleur van de kap/V: zie keuring r2 punt 9; met A_geel is het voorhoofdgeel terug.
