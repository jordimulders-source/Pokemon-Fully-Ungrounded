# Party-icoon regionale Poliwag (proefrit bak A, 28 nov)

**Af:** `af/icon.png` (32×64, 2 frames, modus P, index 0 transparant), `af/icon_8x.png` (front 4× | frame 1 8× | frame 2 8×), `af/icon_anim.gif`. Naast echte iconen: `af_buren_3x.png`.

**Palet: pal3** (`.iconPalIndex = 3`). Pal3 is het enige palet met geel, goud, rood én drie ijsblauwtinten tegelijk. Kleuren die er niet in staan → dichtstbijzijnde: ijs (192,226,240) → lichtblauw 6, ijsrand → 5/4, zwart lijf (40,40,52) → donkergrijs 14 met 15 als omlijning en 1 als lichte plek (zo doen Umbreon/Murkrow het ook).

## Onmisbare kenmerken
1. Zwart lijf met gele kopband bovenop (geel links/boven, zwart rechts achter het oog).
2. IJzig buikvenster met rode hoekige spiraal.
3. Rode mond onder het oog.
4. Kristal (ijs met cinnaber) op de kop; staartvin ijsblauw met rode kern.
Oog: wit met zwarte pupil, zwarte rand (zelfde opbouw als de front; het bestaande Poliwag-oog, pixel voor pixel).

## Werkwijze
- Onderlaag = `graphics/pokemon/poliwag/icon.png`: vorm, pose en frame 2-beweging pixel voor pixel behouden.
- r1 (`r1_omkleur.py`): automatisch omkleuren per zone (kopband, oog, mond, buik, staart, voeten) → `r1_raster.txt`.
- r2–r3 (`r3_maak.py`): kopband geel i.p.v. lichtgeel, buikvenster + spiraal met de hand (venster: witte rand linksboven, ijs, donkerblauwe onderrand), kristal van 3 px op de kop (2 px binnenin: wit boven, rood onder). Frame 2 automatisch afgeleid: elke pixel van het originele frame 2 krijgt de nieuwe kleur van de bijbehorende frame 1-pixel (zelfde verschuiving als het origineel), kristal mee 1 px omhoog.
- r4: onderste omlijning in index 14 geprobeerd → voeten verdwenen in het zwarte lijf; teruggedraaid.
- r5 = af (`r5_maak.py`): roze bovenlip weg (12 → 11 kleuren), hele icoon 2 px naar links (midden x 15).
- Bouwen/vel: `bouw.py raster.txt uitmap`.

**Rondes: 5** (waarvan 2 echt tekenwerk: r2/r3). Tijd: kort; het meeste werk was het buikvenster op 7×5 px.

## Check (`icoon_check.py`): 16/17 OK
- NEE "omlijning boven donkerder dan onder" (boven 77, onder 66): terecht. Het bestaande Poliwag-icoon faalt hier zelf ook (77/65): de staart bovenaan heeft een omlijning in index 14 (Game Freak). Onderrand naar 14 omzetten (r4) laat de voeten wegvallen tegen het zwarte lijf.
- Binnenlijnen 0,249 zit dicht tegen de grens: het zwarte lijf telt als "donker".
- Losse pixels: alleen bewuste enkele pixels (oogwit uit het origineel, kristalkern, gouden 45°-rand links, voetjes).

## Wat moeite kostte
- Zwart lijf: in het icoonpalet ligt het lijf (14) dicht bij de omlijning (15); voeten en onderrand moeten in 15 blijven, anders verdwijnen ze.
- Buikvenster + spiraal op 7×5 px: de spiraal wordt een hoekig "haakje"; herkenbaar als spiraal, niet als kopie van de front.
- IJsblauw bestaat in geen enkel palet echt licht; pal3-lichtblauw (164,197,255) is iets paarser dan de front.

## Wat bak A sneller zou maken
- Standaardscript "omkleuren per zone + frame 2 automatisch afleiden" (`r1_omkleur.py` + het frame 2-deel van `r3_maak.py`) generiek maken: alleen zonegrenzen en kleurtabel per soort invullen. Frame 2 kost dan niets.
- Vooraf per soort het palet kiezen op de hoofdkleuren van de front (script: dichtstbijzijnde kleur per frontkleur, per palet de totale afstand).
- Accepteren dat checks die het vanilla-icoon zelf al niet haalt (midden, boven/onder) alleen goedkoop worden gerepareerd (verschuiven), niet hertekend.
