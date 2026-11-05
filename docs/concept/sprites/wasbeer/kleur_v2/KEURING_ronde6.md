# Keuring kleur ronde 6: alleen de kop (y 0–20)

Keurder: verse agent, 2 nov. Bekeken op 16x/8x/6x (raster), 2x en 1x, licht en donker, naast de koppen van zigzagoon, linoone, teddiursa, zangoose, sentret, raticate, mightyena en absol (anim_front frame 1), en naast ronde 5. Coördinaten (x,y) op de 64x64-sprite; indexen volgens `ronde6.pal`.

**Uitslag: FAIL (4 van 7 PASS).** Ronde 6 is duidelijk netter dan ronde 5 (geen oker meer in oren/snuit, schedel in rustige diagonale banden). Wat nog faalt: de neus, de wenkbrauw en de kanten van het masker. De maker noemt de punten bij 2 en 3 zelf als zwak, en volgens de norm is dat al een fail.

| # | Punt | Oordeel | Waarom |
|---|---|---|---|
| 1 | Korrel/ruis | PASS | Is rustiger dan Zigzagoon/Linoone (vachtstructuur) en zit op het niveau van Teddiursa/Mightyena. Er is geen dither of pillow shading. De losse pixels zijn de iris, de glans, de neusglans en de omlijning in 4 aan de lichtkant van de oren (bewust). Eén klodder valt wel op: de omlijning onder de neus is 2x2 dik (11–12, 18–19), zie R3. |
| 2 | Neus apart | FAIL | De crème rand (13–14,15) is onderbroken, want (12,15) is nog masker 2. Daardoor raakt de verre lob de neus (12,16). Onder de neus zit de 2x2 omlijning. Neus (4) + omlijning + lob worden op 1x/2x één donkere snuitpunt. |
| 3 | Wenkbrauw buigt | FAIL | De boog is een vlakke balk van 5 px (20–24,8) met uiteinden die 1 rij zakken. Op 1x leest hij als een rechte witte streep, zoals in ronde 5. |
| 4 | Oog leest | PASS | Het oog leest door de glans (20,11) en de iris e boven/f onder (21–22,11; 20–22,12). Het lid 1111 (19–22,10) is onzichtbaar op masker 2. Dat zit in het bevroren ontwerp en het ligt in lijn met Zigzagoon (oog in een donker masker). Het verre oog (13,11–12) leest. |
| 5 | Volume en licht | PASS | Het hooglicht 3 zit linksboven op de schedel (13–18,5–6) en loopt via 7 naar 6/5 aan de wang rechts. De snuit loopt van a via 9 naar 7, schuin naar rechtsonder. De oren zijn linksboven het lichtst. |
| 6 | Geen helm | FAIL | De schedel is goed. Het masker leest wel als vizier: de rechterkant van de nabije lob is een rechte verticale lijn van 5 px (x 24, y 9–13) met haakse hoeken, en de onderrand loopt recht door van x 11 tot 24 (y 13). De brug (x 16–19, y 10–13) is 4 rijen hoog, bijna zo hoog als de lobben. Daardoor lezen de 2 lobben op 1x als één band. |
| 7 | Krabbenetende wasbeer op 1x | PASS | Op 1x, licht en donker, zijn het masker over de ogen, de witte wenkbrauw, de witte snuitrand en de ronde lichte oren te herkennen. Leest als wasbeer. |

## Reparaties (alleen de kop, 10 px; oogontwerp, silhouet en alpha ongewijzigd)
- **R1 Wenkbrauw als boog (punt 3):** (21,7), (22,7), (23,7) worden `a` en (24,9) wordt `a`. Zo wordt het een sikkel: dik in het midden, dun aan de uiteinden (19,9) en (24–25,9). Hij blijft direct op de maskerrand liggen.
- **R2 Neus los van het masker (punt 2):** (12,15) wordt van `2` naar `9`. De crème rand loopt dan door van x 12 tot 14, tussen de verre lob en de neus.
- **R3 Klodder onder de neus (punten 1 en 2):** (12,18) wordt van `1` naar `9`. Er blijft een omlijning van 1 px over, (11,18) → (11–12,19) → (13,20), en de neus wordt een eigen donker vlak met een lichte kin eronder.
- **R4 Lobhoek rond (punt 6):** (24,13) wordt van `2` naar `6`. Samen met R1, waardoor (24,9) wit wordt, loopt de rechterkant van de lob dan als boog: y9 x23, y10–12 x24, y13–14 x23, y15 x22.
- **R5 Twee lobben (punt 6):** (17,13) en (18,13) worden van `2` naar `a`. De witte snuit steekt dan als V tussen de lobben omhoog, en de brug over de neusrug wordt y 10–12 (3 rijen, met de lichte 4 op (16–17,10)).

Ik heb de reparaties uitgeprobeerd in een kopie, zonder de bestanden te wijzigen. Daarna leest de boog op 2x en ook op 1x, en zijn de lobben en de losse neus op 2x zichtbaar. Er komt geen nieuwe ruis bij.
