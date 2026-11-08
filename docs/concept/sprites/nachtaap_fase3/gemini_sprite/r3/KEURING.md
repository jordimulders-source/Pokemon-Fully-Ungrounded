# Keuring muriqui r3 (onafhankelijke keurder, 8 nov)

**Oordeel: FAIL**

Getoetst: (1) trouw aan `gemini/gekozen_r4.png` (ogen en rugsikkels mogen afwijken), (2) Gen 3-techniek.
Methode: model BOX-verkleind op exact het spriteraster (16 model-px per spritepixel, offset −2/−1 zoals `sub.py`), 8× naast de sprite; close-ups per onderdeel; meting met `sub.py` (4×4 submonsters per spritecel); maskervergelijking; vergeleken met aipom, ambipom en medicham.

## Afvinken per onderdeel
| Onderdeel | Oordeel |
|---|---|
| Silhouet/massa | OK. Maskervergelijking: 43 px alleen in de sprite (allemaal buitenlijn), 2 px alleen in het model |
| Kopvorm | OK |
| Maansikkel (hoorns, binnenovaal, onderrand) | OK, binnen een halve pixel |
| Masker | OK |
| Ogen | Mogen afwijken, niet getoetst |
| Snuit, neusgaten, mond | OK. Klein punt: het filtrum ontbreekt (punt 8) |
| Hand linksboven | Vorm en vingers OK. Bovenrand en vingerscheiding wijken af in kleur (punten 3 en 7) |
| Hand boven | Vorm, 3 vingers + duim en manchet OK. Toppen wijken af in kleur (punt 3) |
| **Gloedhand** | **FAIL**: lijnwerk en vingerposities (punten 1 en 2) |
| Turkooise gloedvorm | OK, op 1 pixel na (punt 6) |
| Armen en benen | OK. De linkerrand van de bovenarm wijkt af in kleur (punt 3) |
| Voet en tenen | Vorm OK. De naad tussen been en voet is fout (punt 5) |
| **Staartspiraal** | **FAIL**: het witte spiraalpad is op twee plekken onderbroken (punt 4) |
| Kleuren romp, staart en kop | OK |
| Rugpatroon | Mag afwijken, niet getoetst |

## Techniek
- 15 kleuren + transparant ✓; licht linksboven ✓; 1 px buitenlijn ✓; tinten per vlak ✓.
- ✗ **Gloedhand rij 51–53**: de vingerlijnen schuiven elke rij 1 px op. Daardoor ontstaat een dambordpatroon (`dbdbd`/`dcdcd`). In het model staan deze lijnen daar recht.
- ✗ **Binnenlijnen van de gloedhand** zijn `d` (110,116,150). Dat is nauwelijks donkerder dan de vulling `c`/`b`, dus de hand leest op 1× als een grijze vlek. Het model heeft daar zwarte lijnen.
- ✗ **Losse pixel**: (21,47) `e` steekt buiten de teal rand uit en raakt de romp zonder lijn.
- ✗ **Voetnaad**: `5` en `d` wisselen elkaar af op één lijn ("nooit zwart en donkerlila om en om").
- Gekleurde selout aan de lichtkant: het model doet dit consequent, de sprite alleen op de maanhoorn (punt 3).

## Reparaties (coördinaten x,y; letters = `tools.py`-palet)
1. **Gloedhand, lijnkleur.** Het model heeft zwarte contour- en vingerlijnen; de bovenkant van de vingertoppen en de duim is donkerlila (`4`/`5`).
   - Rechtercontour x21, rij 51–59: `d` → `1`.
   - Ondercontour (9,57), (10,58), (11,58), (13,59) en (14..21,60): `d` → `1`. Zet ook (12,58) `b` → `1`: daar zit nu een gat in de contour.
   - Vingertoppen (14,47), (15,47): `d` → `4`.
   - Duimbovenkant (9,55), (10,55), (11,55): `d` → `4`.
   - Knik tussen duim en palm (12,56): `d` → `4`.
2. **Gloedhand, vingerpositie rij 48–54.** Vinger 1 en de lijnen 1 en 2 staan in rij 49–52 1 px te ver naar links. Model: vinger 1 wit op x12, lijn 1 op x13 → x14 → x15, lijn 2 op x16 → x17, lijn 3 recht op x19, palmrand x13. Doelrijen voor x9..x23 (bij rij 60 vanaf x9), afgeleid met `sub.py`:
   ```
   47 fffee44eeeef133
   48 fee4199144eef43
   49 fe491bb1994eef3
   50 fe4bc1b1b914eef
   51 fee5c1cc1b191af
   52 feee1c1c1c1b1af
   53 eeee1c1c1c1c1af
   54 eeee1ccccc4c1af
   55 444e1ccccccc1af
   56 99b4bccccccc1af
   57 1bbbbbccbbbb1af
   58 e111bbbcbbbb1af
   59 feee1bbcbbbb1af
   60 .feee11111111ef
   ```
   Hierdoor verdwijnt ook het dambord. De vingerlijnen mogen `5` zijn in plaats van `1` als selout, maar niet `d`. (15,54) en (16,54) worden `c`: het model heeft daar `2`/`c`, de sprite een lichtere `b`-vlek.
3. **Gekleurde selout aan de lichtkant**, zoals het model:
   - Hand boven: (34,4), (36,4), (37,4), (33,5), (35,5) en duimtop (40,7): `1` → `4`. Zet (32,6) `1` → `5`.
   - Hand linksboven, bovenrand (4..8,14): `1` → `4`. (3,14) mag weg; het model is daar leeg.
   - Staart linksboven (49,23), (47,24), (46,25), (46,26): `1` → `4`.
   - Linkerrand van de bovenarm (32,18), (32,19), (31,20), (31,21), (31,22), (31,23): `1` → `5`.
4. **Staartspiraal.** In het model loopt het witte pad ononderbroken van buiten tot een J-haak in het midden. De sprite onderbreekt het twee keer:
   - **Midden:** (54,32) `1` → transparant. Het model is wit op x53,5–54,5 van rij 30,5 tot 34. Zet daarbij (53,32) `5` → `1`.
   - **Rechtsboven, rij 29:** (57,29) en (58,29) zijn allebei `1`. Het model heeft daar wit op x57,5–58,5. Voorstel: (57,29) → transparant en (56,29) `c` → `1`.
5. **Voetnaad.** (56,49), (55,51) en (54,53): `d` → `5`. Het model heeft een doorlopende zwarte naad tussen het been en de grijze voet.
6. **Gloedrand rechtsboven.** (21,47) `e` → `1` en (21,46) `3` → `1`. Het model heeft daar de donkere romplijn tussen de gloed en het lijf (x21 `1133`/`9911`).
7. Hand linksboven: de vingerscheiding (3,16) `d` → `1` en (4,16) `d` → `4`. Het model is zwart/donkerlila op rij 16,5. Duimknik (5,20) `d` → `1`.
8. *(klein)* Filtrum: (7,42) en (7,43) `7` → `8`. Het model heeft een mauve lijntje van het linkerneusgat naar de mond (x7,5–8).

Daarbuiten niets veranderen; diff 0 buiten deze pixels.
