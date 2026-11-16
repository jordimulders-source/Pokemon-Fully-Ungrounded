# Blobfish fase 2: Gemini-rondes
1. `r1.png` (PROMPT_r1): Jordi: "moet meer pudding, chagrijniger, overdrevener, meer gesmolten".
2. `r2.png` (PROMPT_r2): Jordi: "ogen zijn nu te menselijk en de bovenkant moet rond blijven".
3. `r3.png` (PROMPT_r3): **beste tot nu toe.** Jordi (16 nov): "dit begint ergens op te lijken, maar weet nog niet of ik het een eindvorm vind". Open: wat ontbreekt er voor een eindvorm.
4. PROMPT_r4 (nieuw gesprek, r3 als bijlage): Jordi: "ja misschien wat groter".
   Resultaat: Jordi "hij verandert niks".
5. PROMPT_r5: nieuw gesprek zonder eigen bijlage, alle feedback in de startprompt.
   Resultaat `r5.png`: vrijwel gelijk aan r3, niet groter.
6. `../lagen/`: Jordi over r5: "hij heeft nu een soort laag eronder, misschien dat we er nog 1 of twee onder kunnen zetten". Claude heeft de puddingvoet van r5 gekopieerd (`stapel.py`): +1/+2 lagen, gelijk of telkens 6% breder; overzicht `overzicht.png`.
7. Jordi: "rechtsonderin is perfect, maar dan mag elke laag een iets andere kleur, donkerder is het mooist denk ik". +2 lagen, 6% breder, per laag donkerder (×0,92 of ×0,86): `overzicht_donker.png`.
8. Jordi: "en zorg ervoor dat het niet op copy paste lijkt". `stapel2.py`: per laag anders gespiegeld, verschoven, breder/dunner en donkerder; varianten a/b/c in `overzicht_varianten.png`.
9. Jordi: "nee dit is niet goed, ik bedoel puur de kleur die anders moest" → varianten a/b/c afgekeurd; terug naar rechtsonder + per laag donkerder (`r5_plus2_breder_donker92.png` / `donker86.png`).
10. Jordi: "nee het mogen echt andere kleuren zijn ipv andere tinten". `stapel_kleur.py`: rechtsonder, laag 2 en 3 een andere kleur en donkerder; A paars/blauw, B rood/bordeaux, C karamel/chocolade, D oranje/paars (combinaties: keuze Claude) in `overzicht_kleuren.png`.
11. **Gekozen (Jordi, 16 nov): "B"** → `../referenties/model_gekozen.png` (r5 + 2 lagen, telkens 6% breder, rood en bordeaux). Dit is het model voor de frontsprite.
12. **Sprite af (r5)**: `../af/blobfish_fase2.png` (+ `_8x`, `_vel`). Maker r1–r3 (natief raster 99×99, model op natief raster herbouwd, reductie 1,5×), keuring r3 PASS + reparaties, r4/r5 per script, keuring r5 PASS.
