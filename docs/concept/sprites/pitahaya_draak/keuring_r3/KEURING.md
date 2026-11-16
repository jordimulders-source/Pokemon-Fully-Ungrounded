# Eindkeuring pitahaya-draak fase 1, sprite r3 (16 nov)

Volledige, strenge keuring: trouw aan het model, Gen 3-techniek en de uitvoering volgens de Dragonfly Cave-gids. Het gezicht (x 18–34, y 22–34) telt alleen ter info.
- **Vel:** `vel.png`. Daarop staan: r3 op 8× met markeringen, het natieve model op hetzelfde raster, r2/r3 en r3+MOET op 1× en 2×, en Bagon, Treecko en Larvitar op 2×.
- **Vergelijking r2/r3:** `1x2x.png` en `r2_r3_8x.png`.
- **Scripts:** `stats.py`, `rand.py`, `vlak.py`, `lijn.py` en `grens.py`, plus `keuring_r2/meet.py` en `klont.py`.
- **Simulatie:** `sim_moet.png` = r3 met de MOET-wissels hieronder.

Controle: r3 is gelijk aan `keuring_r2/sim_moet.png` (0 px verschil, 33 px ten opzichte van r2, silhouet-diff 0). Idx 3 is nu (172,56,91), lum 95.

## Oordeel: **FAIL** (6 px, alleen tintwissels)
Na deze 6 wissels voldoet de sprite op alle punten die ik heb gemeten; die metingen staan onderaan. De volgende keuring hoeft dus alleen te bevestigen dat r4 gelijk is aan `sim_moet.png`, en daarna de metingen nog één keer te draaien.

### r3 naast r2 (1×, 2×, 8×): r3 is beter
- De borst heeft geen losse zwarte streep meer.
- De linkerklauwen zijn groene vingers in plaats van een zwarte klont.
- Het linkerbeen en de voet hebben aan de lichtkant selout.
- De rechterkant van de kop is minder zwart.
- Niets is slechter geworden.

Het volume blijft: licht linksboven en een sikkel rechtsonder op kop en lijf, zoals in het model.

### Trouw aan het model
- **Silhouet:** diff 0 met de reductie van het model (≥ 5/9 modelpixels).
- **Wissels:** alle 33 volgen de modelmeting van het blok.
- **Toegevoegd of weggelaten:** niets. Schubpunten, kruinschubben, het cactuslijf met de ribbel en de witte stekeltjes, de armen met klauwen en de voeten met tenen zijn er allemaal en staan op de plek van het model.

### Gen 3 (r3 → r3+MOET)
| meting | r3 | r3+MOET | Gen 3-refs (Bagon / Treecko / Larvitar / Oddish / Cacnea) |
|---|---|---|---|
| zwart van de figuur | 17,3 % | 17,3 % | 6 / 18 / 12 / 12 / 18 |
| zwart binnen de figuur | 8,1 % | 8,1 % | 0,9 / 4,1 / 5,0 / 2,6 / 7,7 |
| losse zwarte pixels | 8 (4 gezicht) | 8 (4 gezicht) | 2 / 4 / 1 / 4 / 8 |
| 2×2 zwarte klonten | 7 (2 ogen, 3 onder de kop) | 7 | 0 / 1 / 3 / 0 / 16 |
| dambord 2×2 | 3 (alle drie diagonale lijnen) | 3 | 7 / 11 / 4 / 11 / 14 |
| zwakke tintgrenzen (RGB-afstand < 60) | 15,1 % | 15,5 % | 0,5 / 6,1 / 10,2 / 6,2 / 23,4 |
| vulvlakjes < 3 px (tinten 3–5, 9–11) buiten het gezicht | 33 | 28 | n.v.t. |

- **Tinten:** roze 3/4/5 + selout 2, groen 9/10/11 + 8, mauve kin 1, amber 2, wit 1. Voldoet.
- **Contrast** (paletwaarden; vlakpixels hebben precies deze waarden):
  - roze 62 → 95 → 133 → 168 (stappen 33 / 38 / 35)
  - groen 67 → 99 → 132 → 169 (stappen 32 / 33 / 37)

  Alle stappen liggen binnen 30–40. De "zwakke" grenzen zijn 4/5, 8/9 en 9/10, met een helderheidsverschil van 32–35, dus volgens de norm. Mauve kin naast roze 4 heeft 0 helderheidsverschil, maar raakt het roze maar op 4 plekken en verschilt van kleur (zo staat het in het model).
- **Buitenlijn:** 1 px.
  - Schaduwkant: 71/71 zwart.
  - Lichtkant: 56/68 selout. De 12 zwarte zijn overschaduwd: onder de kop (24,36), (23,37), (40,37), (41,37); bij de ooghoek (19,22)–(18,25), wat bij het gezicht hoort; en de binnenkant van de rechtervoet naast het kruis (34–35, 51–54).
  - Zwart en selout wisselen nergens om en om (0).
- **Licht en schaduw:** licht linksboven, de schaduw als sikkel. Geen pillow shading en geen banding: de tinten lopen niet evenwijdig aan de rand. Op de linkerflank van de kop ligt licht (5) direct tegen de selout.
- **Dragonfly Cave:** lijnen van 1 px, geen anti-aliasing tegen de achtergrond, geen pure zwarte (17,17,26) blokken buiten de ogen, binnenlijnen aan de lichtkant in de tint van het vlak, en een kleur per materiaal (vrucht, rank, oog). In orde.

## MOET (6 px)
1. **Losse 1-px tint-3-vlekjes in het roze basisvlak.** Ze kwamen door mijn eigen M1 van r2: het model toonde daar vulling met lum 94–111, de dichtstbijzijnde paletwaarde was 3, maar zo wordt het een los vlekje. Neem de omringende tint uit het model over, 3 → 4:
   - (35,19): het modelblok heeft 0/9 zwart en vul lum 96; alle 4 buren zijn 4.
   - (37,10): 0/9 zwart, lum 94; 3 van de 4 buren zijn 4.
   - (29,18): 0/9 zwart, lum 104; de buren zijn 4 en 5.
   - (36,15): 0/9 zwart, lum 111; de buren zijn 4 en 11 (onder de groene punt).
2. **Losse naadpixel** (41,24) 2 → 3. Het modelblok heeft 0/9 zwart en vul lum 83, maar er is geen lijnbuur; de buren zijn 4, 4, 11 en 10. Als tint 3 sluit hij diagonaal aan op de 3 bij (42,23).
3. **Losse donkere pixel midden in de rechterarm** (41,42) 8 → 10. Het modelblok heeft 0/9 zwart en vul lum 107; alle 4 buren zijn 10. Nu is het een donkergroen gaatje in het lichte vlak.

## KAN
1. **Tint-3-vlakjes van 1–2 px in de schaduwband rechts:** (43,27)–(43,28), (41,30), (38,34) en (28,35). Ze liggen tussen schubrandjes, en het model is daar donker roze (vul lum 76–90). Ze lezen als schaduw tussen de naden en niet als ruis. Mag blijven.
2. **(30,13) idx 8:** het donkere uiteinde van de groene schubpunt; het model heeft 4/9 zwart. Hij raakt de groene punt (29–30,12) diagonaal. Mag blijven.
3. **Uit r2 KAN 2–4:** ik maak er geen MOET van.
   - De naadfragmenten (33–34,16), (42,15), (40,19) en (43,23) liggen op echte modelnaden met lum 83–112.
   - Linkerbeen y 47–48 is 1 tint donkerder dan het model (alleen volume, geen techniekfout).
   - Groen-9-vlakjes (24,37) en (29,38) liggen naast stekeltjes en ribbel; (26,51) en (39,52) zijn teenlichtjes. Het zijn allemaal vormdetails.
4. **Dubbele rand rechtsboven** (x 43–45, y 8–12): staat zo in het model.

## Ter info
- **Ogen:** het verre oog is 1 px amber; het nabije oog heeft een glans op (31,25). Dit komt later apart met Jordi.
- **Mond:** zwart op (21,31), (22,32) en (31,31), in de mondlijn en bij het tandje.
- **Grootte:** 31×49, 1087 px (checklist D1 voor fase 1: 700–950; Bagon 763). Dit is de 3×-reductie van het model.
