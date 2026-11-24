# Eindkeuring Dragonfly Cave: satelliet fase 1, sprite r2 (23 nov)

Gekeurd: `../sprite_r2/sprite.png` tegen `../model/model_gekozen_natief.png` (×0,787) en de kale reductie `../sprite_r1/kaal.npy`. Alleen uitvoering, geen herontwerp.
Bestanden: `voorstel.py` (reparaties op een kopie, elke pixel met een assert op de oude waarde, en een assert dat het silhouet gelijk blijft) → `voorstel.png` / `voorstel.npy`; `vel.py` → `vel.png` (8× zwartkaart van r2 met de reparaties omkaderd | voorstel; voor/na op 1× en 2× op licht en donker; 5 Gen 3-sprites op 1×), `voor_na_1x.png`, `voor_na_2x.png`, `voor_na_8x.png`.

## Eindoordeel: **BIJNA**
Trouw aan het model: blijft PASS (silhouet 0 px gewijzigd, onderdelen en oog ongemoeid). Gen 3: de omlijning heeft nog **21 overbodige zwarte pixels**: 10 aan de lichtkant of als "K D K" op één rand, 11 waar de lijn 2 px dik is (2×2-blok, L-hoeken). Na de 23 pixelreparaties hieronder (geen paletwijziging) verwacht ik **PASS**.

## Gids (letterlijk, waarop ik oordeel)
- r. 96–97: *"The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites"*
- Regel 3 (r. 112–114): *"The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."*
- r. 419–423 (revamp): *"There are also some clusters of black where the anti-aliasing was blacked out. To fix that, we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."*
- r. 427–428 en 454–455: *"lighter pixels on the inside of the outline are a far better idea"* · *"place pixels of the outline highlight color on the inside of the outline rather than the outside."*
- r. 443–444: *"the wing "shadow color" is really used where the front wing overlaps the back wing"*. Een binnenlijn waar een onderdeel over een ander valt, krijgt dus de eigen tint en geen zwart.

## Gemeten in echte Gen 3-sprites (`graphics/pokemon/*/anim_front_gba.png`)
| sprite | zwart / totaal | 2×2-blokken zwart | L-hoeken/knooppunten zwart | zwart met lucht links |
|---|---|---|---|---|
| Voltorb | 25 / 538 (4,6 %) | 0 | 0 | 1 |
| Electrode | 32 / 1012 (3,2 %) | 0 | 0 | 1 |
| Lunatone | 67 / 1327 (5,0 %) | 0 | 0 | 4 |
| Magnemite | 93 / 367 | 0 | 13 | 20 |
| Beldum | 91 / 672 | 12 (oogkas, bewust) | 37 | 10 |
| **sprite r2** | 230 / 1548 (14,9 %) | 1 (+ pupil) | 31 | 11 |
| **voorstel** | 209 / 1548 (13,5 %) | 0 (+ pupil) | 6 (alleen knooppunten van twee lijnen en de antennepunt) | 11 |

De ronde Gen 3-lijven (Voltorb, Electrode, Lunatone) hebben een zwarte lijn zonder één verdikking: op een bocht schuift de lijn diagonaal door (Electrode rechtsonder: (44,30) → (45,28–29) → (46,27)), nooit met een extra hoekpixel. Dat is de maatstaf voor P2. Gnomad r10 (goedgekeurd) zat op 13,0 % zwart; het voorstel zit daar op 13,5 %.

## Kaart van elk zwart pixel (r2, 230 px), per groep
(rij,kol); kaart in `vel.png` links: grijs stipje = zwart, kader = reparatie.
| groep | zwarte pixels | hoort hij er? |
|---|---|---|
| **Pupil** | (31–35, 8–11), 18 px | ja: pupil uit het model, mag donker |
| **Oogrand, boog onder/rechts** | (31–35,16), (36,15), (37,14–15), (38,14), (39,12–13), (40,9–11), (39,7–8), (38,7), (37,5–6) | ja: het model heeft hier zelf zwart (rechts en onder de oogring, modelrijen 48–59); Beldum heeft ook een zwarte oogkas. Alleen de 2 hoekpixels (39,7) en (37,15) maken de boog 2 px dik → **O1** |
| **Lijf rechts en onder** | kol 37–38 rij 25–44, onderrand rij 48–52 | ja: schaduwkant |
| **Lijf linksonder** | (37,2), (38–40,3), (41–42,4), (43,5), (44,6–7), (45,7), (46,7–8), (47,8), (48,9–11), (49,11–12) … | ja, volgens de goedgekeurde boog "van linksmidden via linksonder tot onder-midden" (SPRITE_KERN, Gnomini); keuring r1 akkoord (één wissel paars → zwart op rij 37). Wel 4 trapjes 2 px dik → **V4–V7** |
| **Voetje linksboven** | (13–15,22) | ja: rechterkant (schaduw), zwart in het model |
| **Voetje rechtsboven** | (17,34), (18,35), (18,36), (19–22,37), (23,36), (24,35–36), (23,29), (24,30–31), (25,32–34) | rechter- en onderkant ja. **(17,34) en (18,35) liggen bovenop (lichtkant, lucht erboven)** → **Z2** |
| **Voetje onder** | (44,31–34), (45,30), (46–49,29), (45,35), (46–47,36), (48,36), (49,35), (50,29–30), (51,30–33) | rechts en onder ja. **Bovenkant (44,31–33) en linksboven (45,30), (46,29) zijn lichtkant én binnenlijn op het lijf**; de andere twee voetjes hebben daar paars → **Z5**. (50,30) maakt een L → **V8** |
| **Antenne 1** (boven) | onderlijn (7,43) … (15,24–26) | ja (schaduwkant onder). **(15,23) is D tussen zwart: "K D K" op één rand** → **Z1**; (14,26) maakt kolom 26 2× zwart → **V3** |
| **Antenne 2** | onderlijn (8–10,60), (11,57–59), (12,55–56), (13,54–55) … (18,41–43), (19,40), (20,37–39) | ja. (12,55) maakt kolom 55 2× zwart → **V2** |
| **Antenne 3** (midden) | punt (33–34,60), (34,59), onderlijn (35,54–57), (36,49–53), (37,40–48), aanzet (34,39), (37–38,37–38), (38,39–40) | onderlijn ja. **(34,39) is bovenrand (lichtkant; de rest van de bovenrand is D)** → **Z3**; **2×2-blok (37–38,37–38) en dubbele onderlijn (37–38,40)** → **V1** |
| **Antenne 4** (onder) | (48,36–37), (49,35), onderlijn (50,34) … (57,55–57), punt (55,59), (56,58–59) | onderlijn ja. **(48,37) is bovenrand (rest D)** → **Z4**; (56,55) maakt een L → **V9**. Punthoek (56,59) laten (buitenhoek, silhouet). |

Geen losse zwarte pixels binnen een vlak: alle zwarte pixels hangen (8-buren) aan een rand of de pupil. De naad heeft geen zwart (goed). Geen lichte kleur op de buitenrand (open rand: 0, voor en na).

## Reparaties (op prioriteit; (rij,kol): oud → nieuw)
Indices: K = 1 zwart, D = 2 donkerpaars (outline base paars), P = 3, w = 6, l = 7, m = 8. Silhouet blijft exact gelijk (assert in `voorstel.py`).

**P1: zwart aan de lichtkant / zwart en paars om en om**
1. **Z1** onderlijn antenne 1, "K D K": (15,23) D → K; (15,22) K → P (de hoekpixel; de onderrand van het voetje is daar al P). Zwart netto 0.
2. **Z5** onderste voetje, bovenkant en linksboven (binnenlijn op het lijf, lichtkant): (44,31) K → D; (44,32) K → D; (44,33) K → D; (45,30) K → D; (46,29) K → D. Zwart blijft vanaf (47,29) linksmidden en vanaf (44,34) rechts: één wissel per kant.
3. **Z2** bovenkant voetje rechtsboven: (17,34) K → D; (18,35) K → D. (18,36) blijft zwart (begin van de rechterflank).
4. **Z3** bovenrand antenne 3 bij de aanzet: (34,39) K → D.
5. **Z4** bovenrand antenne 4 bij de aanzet: (48,37) K → D.

**P2: verdikte zwarte lijn (gids: "the outline is always one pixel wide")**
6. **V1** aanzet antenne 3: (37,37) K → m (2×2-blok weg); (37,40) K → P (onderlijn was daar 2 dik).
7. **V2** antenne 2: (12,55) K → P.
8. **V3** antenne 1: (14,26) K → P.
9. **V4** rand linksonder bij het einde van de naad: (42,5) K → P (naadtint, zoals (42,6)).
10. **V5–V7** trap linksonder: (44,7) K → w; (46,8) K → l; (48,11) K → m.
11. **V8** onderkant onderste voetje: (50,30) K → P.
12. **V9** antenne 4 bij de punt: (56,55) K → P.

**P3: oog (vorm blijft, uit het model)**
13. **O1** (39,7) K → w; (37,15) K → w. De zwarte boog onder het oog loopt daarna diagonaal door zonder hoekpixel; pupil, ringen en iris ongemoeid.

Totaal **23 pixels, zwart 230 → 209**, geen paletwijziging, geen randpixel verschoven.

## Controles na het voorstel
- **Bol rond** (`../sprite_r2/rond.py` op `voorstel.png`): identiek aan r2, want het silhouet is gelijk: centrum (20,6; 33,7), r = 18,26; max afwijking per kwadrant linksboven −0,64, linksonder +0,68, rechtsboven +0,64, rechtsonder +0,78 px (≤ 0,78; enige punt > 0,7 is (52,23), uit het model). Trappen ongewijzigd.
- **Open randen:** 0. **2×2 zwart buiten de pupil:** 0 (was 1). **L-hoeken/knooppunten zwart:** 31 → 6; wat overblijft zijn knooppunten waar twee lijnen samenkomen ((20,37), (24,36), (38,37), (38,38), (49,29)) en de buitenhoek van antennepunt 4 (56,59).
- **Losse tintpixels < 3 px:** geen nieuwe. Elke nieuwe P/w/l/m-pixel hangt aan hetzelfde vlak; de w-lip (43,7)/(44,8) is nu één groep met (44,7). De 1–2 px "clusters" die het 4-burenscript verder noemt zijn de diagonale lijntjes (antennes, oogring, naad) die al in r1/r2 stonden en zijn goedgekeurd.
- **Antennes:** alleen K → D (lijnkleur blijft lijnkleur) of K → P (dikker); nergens wordt een antenne dunner. De kleurdikte blijft ≥ 2 px behalve de uiterste punt (keuring r1).
- **Oog:** geen glans, geen wijziging aan pupil, iris of ringen; alleen 2 hoekpixels in de buitenboog.
- Op 1× en 2× (licht en donker, `vel.png`): geen zichtbaar verlies; de onderste voet en de aanzet van antenne 3 lezen rustiger, de bol blijft even rond.

## Ter info voor Jordi (geen reparatie)
- De ronde Gen 3-lijven Voltorb, Electrode en Lunatone hebben linksonder géén zwart (1–4 px zwart met lucht links; daar de donkerste eigen tint), en maar 3–5 % zwart in totaal. Onze regel (SPRITE_KERN, Gnomini: zwarte boog vanaf linksmidden) geeft hier 11 px zwart links. Volgens onze goedgekeurde sprites is dat goed en ik heb het niet aangeraakt. Wil Jordi de bol nog lichter van lijn, dan is dit de plek: kol 2–8 rij 37–47.
- De zwarte buitenboog van het oog (rechts en onder) komt uit het model en lijkt op Beldums oogkas. Ik heb hem laten staan.
