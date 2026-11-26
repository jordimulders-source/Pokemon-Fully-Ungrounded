# Eindkeuring guaraná fase 1 (Dragonfly Cave: schaduw + belijning + kleurtinten), 25 nov

Getoetst: `sprite_r4/guarana_r4.png` (Psyduck-ogen) en `sprite_r4/r4_ogen_groter.png` (Weepinbell-ogen), naast `model.png` (op schaal), de maatstaf-sprites Skinguin, Dundragoon, Zapacha en Princadee en de Gen 3-sprites Bellsprout, Weepinbell, Oddish, Hoppip en Ekans (`anim_front_gba.png` + `normal_gba.pal`).
Uitvoer: `guarana_ek.png`, `guarana_ek_ogen_groter.png`, `vel.png` (ek | r4 | model op 8×, Skinguin, Dundragoon, Bellsprout en Hoppip op 8×, ek op 1× en 2× op wit/donker), `bouw.py` (leest r4 in), `vel.py`.

**Bevroren (met script bewezen, asserts in `bouw.py`):**
- alpha-diff 0 t.o.v. r4 in beide versies;
- oogwit, pupillen en alle zwarte pixels zijn ongewijzigd (diff 0 op index 1/10/11);
- hoofdversie 12 px anders dan r4, variant 10 px, plus het groene palet.

## Gids (citaten, `docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- r. 96–97: "The 'outline shadows' are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 106–107: "the relative luminosity of the shades on the original sprite should always be maintained".
- r. 109–110: "There is a reason all the shades on the main body are green, too. Don't make the highlights blue and the base color red".
- r. 112–113: "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 117: "The outlines must be reasonably dark."
- r. 145 (hue shift): "(or possibly something slightly in the blue direction from there for shadows)".
- r. 421–423: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 427: "lighter pixels on the inside of the outline are a far better idea".
- r. 452–455: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts ... place pixels of the outline highlight color on the inside of the outline rather than the outside."

## Belijning: PASS (geen wijziging nodig)
Gemeten in beide r4-versies:
- **Zwart alleen aan de lichtkant: 0 px.** Zwart binnen het silhouet buiten de ogen: 0 px. Lichte kleur op de buitenrand: 0 px.
- **Selout aan de lichtkant** in de eigen donkerste tint (lijnrood L55, lijngroen); de binnenlijnen (naden tussen de vruchten, de ranknaden) zijn niet zwart.
- **Dunne krullen 1 px in lijngroen.** Dat klopt met Gen 3: Bellsprouts 1-px-delen zijn 15 van 17 keer de donkerste eigen tint (106,65,0), gemeten.
- **Kleur direct binnen de zwarte buitenlijn:** guaraná r4 heeft daar 33 van 130 keer een donkerdere tint (lijntint) en 84 keer de schaduwvulling. Ter vergelijking, lijntint tegen schaduwvulling:

  | sprite | lijntint | schaduwvulling |
  |---|---|---|
  | Bellsprout | 35 | 35 |
  | Weepinbell | 23 | 52 |
  | Hoppip | 22 | 40 |
  | Skinguin | 40 | 133 |
  | Zapacha | 49 | 102 |

  De guaraná valt daarbinnen.
- **2-px plekken in de lijn:** er zijn er een paar die wél opvallen. Waar het een fout was, staat het onder Schaduw (de rechterrand van de tros). De rest:
  - oogranden (Psyduck/Weepinbell-oog, niet aanraken);
  - krulletjes in het bevroren silhouet;
  - (13–14,29) onder de linkervrucht: model L81/85 zou schaduw zijn, maar dan ontstaat een los vlekje van 2 px tussen de buitenlijn en de oogrand. Al in r4 gemeld; gelaten.

## Schaduw: was BIJNA, nu PASS
Grondregel: schaduw volgt de modelhelderheid (`model_op_schaal`, L), met de drempels van het bouwscript: <72 lijn, <100 schaduw, ≥140 licht.

De rank volgt het model al: licht op de linker-/binnenkant van elke buis, donker rechts en onder, en gebogen grenzen langs de spiraal. Geen wijziging.

In de tros stonden pixels in de lijntint pal naast het zwart, terwijl het model daar schaduwtoon heeft. Dat gaf een lijn van 2 px en een vrucht zonder sikkel. Ook stond er één lichte pixel in een naad. Wijzigingen, allemaal gelezen op het model:

| pixel(s) | r4 → ek | model L | reden |
|---|---|---|---|
| (27,27), (27,28), (27,29), (28,29), (28,30), (27,31) | lijn 2 → schaduw 3 | 109, 96, 90, 100, 74, 82 | Rechtsondervrucht: rechterrand was lijnrood naast de zwarte buitenlijn (lijn 2 px dik). Het model is daar schaduwtoon (de vrucht zelf heeft L 116–173). Nu loopt één gebogen sikkel van rechtsboven langs de rand naar de bestaande onderste sikkel (24–27,32). (28,31) blijft lijn (L33). |
| (25,27) | licht 5 → lijn 2 | 63 | Lichte pixel in de naad tussen twee vruchten. Het hooglicht (25–26,28–29) blijft 4 px. |
| (26,27) | lijn 2 → schaduw 3 | 96 | Bovenkant van de sikkel onder de naad. |
| (24,26), (23,27) | midden 4 → schaduw 3 | 74, 86 | Vrucht rechts van het bovenoog: korte diagonale sikkel rechtsonder, zoals de goedgekeurde sikkel van de linkervrucht. |
| (18,27), (19,27) | midden 4 → schaduw 3 | 56, 88 | Middelste vrucht had geen schaduw. Nu een sikkel onderaan, tegen de lijnkolom 20. **Alleen hoofdversie:** in de variant is (18,27) de rand van het Weepinbell-oog. Daar zijn beide overgeslagen (anders blijft 1 losse pixel over). |

Niet veranderd, ook al wijkt de modelhelderheid daar af:
- kolom 23 (y29–32) en kolom 21 (y30–33): eerdere keurdersbesluiten tegen schaduwbanden;
- (15,21–23): idem;
- (12,27): anders wordt de sikkel van de linkervrucht weer een rechte band.

Tintvlakjes kleiner dan 3 px in de ek: alleen diagonale sikkelpixels ((16,26), (24,26), (23,27); 8-verbonden horen ze bij een sikkel), 1 glanspixel (18,17) en (21,23) tussen de oogrand en de naad. Hetzelfde patroon als in de goedgekeurde r3/r4.

Geen rechte banden of pillow shading toegevoegd: elke wijziging volgt de modelhelderheid en de vruchtrand.

## Kleurtinten: rood PASS, groen was te vlak → aangepast
**Rood** (lijn/schaduw/midden/licht):

| | lijn | schaduw | midden | licht |
|---|---|---|---|---|
| L | 55 | 90 | 120 | 163 |
| hue | 357 | 3 | 8 | 14 |

- Stappen 35/30/43: vergelijkbaar met Skinguin-rood (52/74/110/154) en Hoppip (58/103/143/180).
- Hue shift: schaduw naar paarsrood, licht naar oranje.
- Ongewijzigd.

**Groen r4:**

| | lijn | schaduw | midden | licht |
|---|---|---|---|---|
| L | 82 | 109 | 136 | 163 |

- Stappen 27/27/27, verzadiging 40–45 %.
- Dat is onder de ±30–40 van SPRITE_KERN en duidelijk vlakker dan de maatstaf: Dundragoon-blauw 73/110/148/202, Skinguin 22/36/44 per stap, Bellsprout-blad 140/180/219.
- Op 8× las de rank daardoor als één effen olijfvlak.

**Groen ek:**

| index | rol | RGB | L | hue | verzadiging |
|---|---|---|---|---|---|
| 6 | lijn | (58,86,46) | 73 | 102 | 46 % |
| 7 | schaduw | (84,122,64) | 104 | 99 | 47 % |
| 8 | midden | (122,160,80) | 139 | 88 | 50 % |
| 9 | licht | (166,198,108) | 178 | 81 | 45 % |

- Stappen 31/36/38. Hue shift: schaduw koeler, licht warmer.
- Blijft olijf (gedempt t.o.v. Bellsprout), dus het karakter van het model blijft.
- De lijn blijft "reasonably dark" (Bellsprout-outline base L86).
- Dit is geen vormwijziging: SPRITE_KERN "kleur mag altijd afwijken van het model".

**Tinten per groep:** rood 3 + lijn, groen 3 + lijn, oogwit 1 (index 11 ongebruikt). Totaal 10 kleuren + transparant. In orde.

## Ter info voor Jordi (ontwerpvragen, niet uitgevoerd)
- **Pupil van de hoofdversie:** 1 px (Psyduck) tegen ±2×2 in het model. Oogkeuze blijft hoofdversie tegen variant.
- **Groene verzadiging:** de ek is iets levendiger dan het model, maar nog steeds olijf. Wil Jordi het gedempter, dan kan het contrast blijven en de verzadiging terug naar ±40 %.

## Oordeel
- **`guarana_ek.png` (Psyduck-ogen): PASS.**
  - Belijning volgens de gids en de maatstaf.
  - Schaduw volgt het model, met sikkels per vrucht.
  - Groen contrast nu op maatstafniveau.
- **`guarana_ek_ogen_groter.png` (Weepinbell-ogen): PASS.**
  - Zelfde wijzigingen, behalve de sikkel van de middelste vrucht: die plek is daar oogrand.
  - Bekend uit r4: de 2×2-pupil van het rechteroog raakt diagonaal de buitenlijn. Dat hoort bij het oog en is niet aangeraakt.
