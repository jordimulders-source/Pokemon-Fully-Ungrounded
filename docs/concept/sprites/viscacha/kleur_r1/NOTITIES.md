# Viscacha frontsprite, kleur ronde 1 (maker-agent)

## Wat ik deed
- **Silhouet** (`silhouet/`): masker uit `referenties/gemini_gekozen_ronde6.png` (niet-wit, gaten gevuld), grijze snorharen weg met een opening van 7×7 px (gekleurde dunne delen komen terug), verkleind met BOX naar 62×53 (schaal 1:9,97), voeten op rij 62, 1 px marge links/rechts. Vel: `silhouet/vel.png` (bron, 8× met de bronomtrek in rood, 1× en 2×).
- **Handwerk aan het silhouet (alleen dunne delen):** pluimpunten (59,10), (56,11) en (59,16); top van het nabije oor (21,12) en (22,12); spleet tussen de achterpoten dicht op (34,51) en (35,52) (de spleet bij (35–36,53) blijft als kruis tussen de poten); keelinkeping onder de kin dicht op (8,37) en (9,37). De rest is de automatische massa (`silhouet_auto.txt`).
- **Studie:** Pachirisu, Emolga, Dedenne, Sandshrew en Taillow op 8×. Dedenne is hetzelfde bouwtype en dezelfde kleurfamilie (oranje knager, bruine selout, zwart aan de schaduwkant).
- **Kleur:** met de hand als tekstraster (`raster_bron_r1.txt`, groepen van 10 kolommen; `bouw.py` maakt er `raster.txt` van, `render.py` de png en `normal.pal`). Palet in `palet.py`: 1 zwartbruin (schaduwkant), 2 donkerterracotta (selout aan de lichtkant, binnenlijnen), 3/4/5 terracotta, oker en zand, 6/7 crème, 8/9/A geel (8 = gele selout en binnenlijn), B/C bruin (staart, oorbinnenkant), D/E oog, F crème-selout.
- **Oog:** Emolga's rechteroog (anim_front, x25–28, rij 22–26) pixel voor pixel overgenomen en alleen herkleurd (3→E, 4→1, 2→B, 8→D, 6→F), op x10–13, rij 25–29.
- **Wangpluk:** sikkel van geel met de hoorn rechtsboven die buiten de kop uitsteekt en een onderpunt richting schouder. Op rij 31–33 ligt het geel zonder lijn tegen de wangvacht (vast); boven (rij 27–30) en rond de punten krijgt hij een gele selout (8) of een zwarte lijn aan de schaduwkant. Het kleine gele plukje links naast de snuit (uit de bron) zit ook zonder lijn aan de wang vast.
- **Staart:** zoals in de bron tweekleurig (bruin aan de binnenkant, oker buiten) met de schaduw (3) aan de rechterrand; gele pluim met drie punten en een binnenlijn tussen de linkervlam en de hoofdvlam, overgang van geel naar bruin gekarteld.
- Snorharen weggelaten (in de bron dun en grijs; op 64 px werden ze rommelig). Geen vonken, geen ondergrond.

## Controle (`controle.py`, uitvoer in `controle_uitvoer.txt`)
Alpha-diff met het silhouet 0; open randen 0; losse pixels 0; clusters < 3 px alleen het oog (E, D = glans); 15 kleuren + transparant = 16; png = raster.

## Waar ik van de bron afweek
- Snorharen weg (zie boven).
- Keelinkeping onder de kin dichtgemaakt: in het masker was het een restje van de snorharen, en met de inkeping leek de kin een open mond.
- Het lichaam heeft een gerichte belichting (licht linksboven, schaduwsikkel onder en rechts, eigen hooglicht op de dij); de bron is vlakker.

## Eerlijke zwakke punten (voor de keurder)
1. **Formaat:** het dier vult de breedte (62 px); Pachirisu en Dedenne zijn kleiner in hun frame. Dat is volgens de opdracht ("zo groot als past"), maar naast echte sprites oogt hij groot.
2. **Wangsikkel** kan op 1× nog als een schuine gele kraag lezen in plaats van een wangpluk; het vaste deel (rij 31–33) is maar 3 rijen.
3. **Hooglicht op de dij** (5) is een vrij los eiland naast de lichte rugband; het leest als dij, maar het kan rustiger.
4. **Voorpoot dichtbij:** de binnenlijnen op x18 (2) en x23 (1) lopen recht en verticaal over ±8 rijen; stijf, niet taps.
5. **Snuit:** neus (3,31) en mond (5,33) zijn elk één pixel; de snuit is minder uitgesproken dan in de bron.
6. De onderrand van de crème buikvlek (rij 48) loopt recht en horizontaal.
Niets gecommit.
