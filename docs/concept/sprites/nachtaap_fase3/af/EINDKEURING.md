# Eindkeuring nachtaap fase 3 (muriqui), beta-versie (onafhankelijke keurder, 5 nov)

**Definitief oordeel (5 nov, na F1): GOED.** De 2 px van F1 zijn toegepast. Ten opzichte van `rugpatroon/ronde7/stand_D.png` is het verschil alleen (5,37) 12→15 en (6,37) 11→12. De alpha-diff is 0, het palet is ongewijzigd en de transparency is 0. Het bestand is gelijk aan `eindkeuring/proef_oog.png`, die op 16× en 1× is bekeken.

*Eerste oordeel:* TERUG op 2 px (linkeroog, F1), daarna GOED. Jordi vroeg om ook het linkeroog te keuren ("kijk vooral ook naar het linkeroog nog"). Dat oog heeft geen glans, en zijn iris is donker links in plaats van donker boven. Daarmee faalt het op eis 7. De reparatie staat in §0. Buiten het oog vond ik geen harde fout. De sprite is basis `kleur/ronde7c` plus rugpatroon stand D (`rugpatroon/ronde7/stand_D.png`, pixeldiff 0). Buiten de drie banden is niets gewijzigd: 81 px diff tegen ronde 7c, alpha-diff 0, alleen in de zone x21–39, y30–42. De punten onder "Voor Jordi" zijn smaak of ontwerp. Die zijn al door Jordi gekozen of bevroren, dus het zijn geen reparaties.

Gekeurd: `nachtaap_fase3.png` + `normal.pal`. Vel: `vel.png`. Daarop staan fase 3 en fase 2 naast Primeape, Slaking, Vigoroth, Grumpig, Aipom, Ambipom, Monferno, Infernape, Furret, Dusclops, Alakazam en Medicham, op 3× en 1×, licht en donker. Uitsneden in `eindkeuring/`: `rug8_licht`/`_donker`, `rug8_basis_ronde7c` (voor), `zoom8_licht`/`_donker` en `rug_vs_furret_dusclops4`. Script: `eindkeuring/vel.py`. De sprite zelf is niet gewijzigd.

## 0. Linkeroog (op verzoek van Jordi), op 16×
Uitsnede: `eindkeuring/oog16.png`, met links de huidige stand en rechts de proef, elk op 16×, 4× en 1×. Script: `eindkeuring/oog.py`. De proef staat als kopie in `eindkeuring/proef_oog.png`.

| Onderdeel | Linkeroog (verre oog, x5–6) | Rechteroog (nabije oog, x9–11) | Oordeel |
|---|---|---|---|
| Vorm | 2×2, smaller dan het nabije oog (3×2) | 3×2 | PASS. Het verre oog is korter door het perspectief, en dat klopt. |
| Bovenlid | (5–6,36) = 1, recht op de oogrand | (9–12,36) = 1 | PASS |
| Iris | y37: C B, y38: B A, dus donker **links**, licht rechtsonder | y37: F C B, y38: B A A, dus donker boven, licht onder | **FAIL**. De verloop loopt horizontaal en niet van boven naar onder. |
| Glans | **geen** | F op (9,37), links boven | **FAIL**. Op 1× kijkt het linkeroog dof en lijkt het weg te draaien, terwijl het rechteroog fonkelt. |
| Omlijning en inbedding | Gezichtsschild 7/6 eromheen, (4,37–38) = 7 tussen oog en vachtrand | Idem | PASS |

**F1, reparatie (2 px, alpha-diff 0):**
| Pixel (x,y) | Nu | Wordt | Waarom |
|---|---|---|---|
| (5,37) | 12 (C) | 15 (F) | Glans links boven, net als bij het rechteroog. |
| (6,37) | 11 (B) | 12 (C) | Iris donker boven. Het oog wordt dan F C / B A, hetzelfde patroon als het nabije oog met één kolom minder. |

Het resultaat in de proef: beide ogen fonkelen en het verre oog is nog steeds smaller. Op 1× is de blik strak en sinister, zonder brilogen. Wil Jordi het verre oog minder fel, dan kan (5,37) A (10) worden in plaats van F. Smaak.

## 1. SPRITE_NORM, harde eisen
| # | Eis | Oordeel | Bewijs |
|---|---|---|---|
| 1 | Leest op 1× als een echte Pokémon | PASS | Naast Ambipom, Infernape en Medicham leest hij als een zwevende aap met lange ledematen, een spiraalstaart en een gloeiende hand. Hij leest meteen als de lijn van fase 2: violet, maan, lichte banden. |
| 2 | 3/4 links-voor | PASS (bevroren) | Kop vooraan links, lijf diagonaal naar achteren. |
| 3 | Ledematen tellen, met lucht ertussen | PASS (bevroren) | Twee armen, twee benen en de staart zijn op 1× te tellen en allemaal verbonden. |
| 4 | Geen Escher | PASS | De banden liggen óp de romp en lopen niet over arm, been of staart heen. |
| 5 | Curven, geen doos | PASS (bevroren) | — |
| 6 | Kop | PASS (bevroren) | — |
| 7 | Ogen geïntegreerd | **FAIL (F1)** | Het rechteroog is in orde. Het linkeroog heeft geen glans en een horizontale iris, zie §0. |
| 8 | Kenmerken op 1× leesbaar, geen harken | PASS | De drie banden lezen op 1× als drie aparte ')'-bogen, ook op de donkere achtergrond. Het ruisscript vond in de banden geen hark of dambord: elke rij is een aaneengesloten run van 1–3 px. |
| 9 | Omlijning, geen open randen | PASS | De banden grenzen nergens aan transparant. Hun buren zijn alleen 3, 4 en 5. De rand van het lijf is ongewijzigd (bevroren). |
| 10 | Geen Chernobyl | PASS | Er zijn geen losse of zwevende pixels in het patroon. Elke band is één component van 27 px. |
| P | Patroonregels | PASS (zie "Voor Jordi") | De banden hebben een eigen kleurgroep (F 252 / D 212,226,244 / E 152,170,204) en een duidelijke waardesprong ten opzichte van het violet. Ze zijn niet de hooglichttint (5) van de vacht. Breedte: 3 px in het midden, 2 px aan de punten, 1 px aan de onderpunt. Ze zijn als geheel geschaduwd: boven FDE, onder DDE, dan DE en EE. Ze buigen als ')' mee met de rug, die omhoog loopt (top y32, y31, y30). |

## 2. §0-checklist (SPRITING.md)
| # | Punt | Oordeel |
|---|---|---|
| 1 | Lijf én blik diagonaal | PASS (bevroren) |
| 2 | Ledematen, oren en ogen geteld en verbonden | PASS |
| 3 | Geen rechte lijnen | PASS. De banden zijn rond. De bovenste helft loopt 1:1 diagonaal, de onderste helft verticaal, en de overgang is geleidelijk. |
| 4 | Ogen geïntegreerd | **FAIL (F1)**. Het linkeroog heeft geen glans, zie §0. Het is geen kopie. |
| 5 | Silhouet leest als de soort | PASS (bevroren, Jordi akkoord) |
| 6 | Formaat | PASS (bevroren): 1843 px, dat is 1,26× fase 2 (1459). Hij is groot genoeg naast Infernape en Medicham. |
| 7 | Pose niet stijf | PASS |

## 3. Rugpatroon per onderdeel (op 8×, 3× en 1×)
| Onderdeel | Oordeel | Opmerking |
|---|---|---|
| Band 1 (links, x21–27, y32–42) | PASS | Het onderuiteinde (25,42) ligt tegen de schaduw 3/4 van de romp. |
| Band 2 (x27–33, y31–41) | PASS | — |
| Band 3 (rechts, x33–39, y30–40) | PASS | Er zit lucht tussen band 3 en de staartwortel (x42+), dus de staartaanzet blijft vrij. |
| Afstand | PASS | De banden staan 6 px uit elkaar, met 3–4 px violet ertussen. Ze lopen op 1× niet in elkaar over. |
| Licht | PASS | Wit staat aan de lichte kant (links boven), grijsblauw rechts en onder. Dat is dezelfde lichtrichting als het lijf. |
| Fase 2 → 3 | PASS | Fase 2 heeft lichte wiggen in F (168,196,236). Fase 3 heeft lichte banden in dezelfde koele tint. De lijn blijft herkenbaar. |

## 4. Wat ik mat
- PNG in modus P, transparency 0, PNG-palet gelijk aan ronde 7c en aan `normal.pal`. 15 kleuren plus transparant.
- Diff tegen `kleur/ronde7c/nachtaap_fase3.png`: 81 px, alleen 3/4/5 → D/E/F. Alpha-diff 0.
- Diff tegen `rugpatroon/ronde7/stand_D.png`: 0 px. Het is dus exact wat Jordi koos.
- Drie componenten van elk 27 px, met dezelfde vorm, verschoven met (+6, −1).
- D, E en F komen buiten het patroon alleen in de hand en gloed voor (x5–20, y30–59).

## 5. Voor Jordi (smaak of ontwerp, geen FAIL)
- **Shading over de breedte:** in de bovenste rijen loopt elke band F-D-E van links naar rechts. In de strikte lezing van de patroonregel ("geen bevel") is dat een klein ribbeltje. Op 1× en 3× leest het als een lichte band met de schaduw aan één kant, niet als een ribbel. Jordi heeft deze shading gezien in ronde 6 en alleen om een draai gevraagd. Als je het vlakker wilt: zet de F in de bovenste vier rijen van elke band om naar D. Dat zijn 12 px: (23,34) (24,35) (25,36) (25,37) · (29,33) (30,34) (31,35) (31,36) · (35,32) (36,33) (37,34) (37,35). Niet nodig.
- **Drie identieke banden:** ze hebben geen perspectief naar achteren toe. Op een licht gebogen romp in 3/4 zou de achterste band (rechts) iets smaller en donkerder mogen. Op 1× valt het niet op, en Furret heeft ook bijna gelijke banden.
- **De bovenpunten stoppen 2–3 px onder de rugcontour** en lopen dus niet door tot de rand. Dat volgt Jordi's krabbel: banden midden op de romp.
- **Formaat:** de norm noemt fase 3 ≈ 2,4× fase 1. Met 1843 px zit hij daar wat onder. Het silhouet is bevroren, en naast de echte eindvormen valt het niet klein uit.

## 6. Nog te doen (buiten deze keuring)
Frame 2, rug, icoon, shiny, naam en data.

## Slot (Claude, 5 nov)
Jordi koos linkeroog D (= reparatie F1: (5,37)=15, (6,37)=12). Toegepast op `nachtaap_fase3.png`, gelijk aan `eindkeuring/proef_oog.png`. Daarmee is F1 opgelost. **Eindoordeel: GOED.**
