# Keuring r4 blobfish fase 2 (verse keurder, 16 nov)
**Oordeel: FAIL, nipt.** Eén MOET van 4 px (mechanisch, terug naar r3); daarna PASS. Plaatjes: `r4_1x/2x/8x.png`, `r3_r4_1x.png`, `r3_r4_2x.png`, `model_kaal_r3_r4_4x.png`, `gen3_2x.png` (r4 | Muk | Slowpoke | Chansey), `bultje_r3_r4_16x.png`.

**Blind (1×/2×/8×):** mooie, leesbare sprite; meteen een ingezakte, chagrijnige blobfish: ronde volle koepel, twee kleine visogen, hangende neus, brede boogmond, vinnen rechts, rode + bordeaux golflagen. Staat naast Muk/Chansey als Gen 3. Alleen het linker bultje (x6–8, y41–45) valt op 8× uit de toon: de rand is daar open.

**(a) r3 → r4 (21 px, silhouet gelijk):** beter op 4 punten: schaduwrand (49,36)–(50,38) nu zwart (geen zwart/mauve om en om meer); onderrand linksonder (2,58)…(13,61) zwart; linkeroog (14,29) terug naar de reductie, oog nu 2×2 zoals het rechteroog; het bultje heeft nu de lichte vulling uit het model. **Achteruit:** r4.py nam het hele blok R[41:46, 6:9] uit `kaal.png`, ook de rand, terwijl de r3-keuring zei "rand blijft selout".
**(b) Hoofdvraag:** ja, dit wil Jordi zien; lijkt duidelijk op het model (koepel, gezicht, vinnen, lagen op dezelfde plek en verhouding).
**(c) Eis 1 accuraat:** silhouet = kale reductie, niets toegevoegd of weggelaten. **Eis 2 Gen 3:** 15 kleuren + transparant; buitenlijn 1 px, zwart rechts/onder, selout linksboven; licht linksboven; geen pillow shading of banding; behalve het bultje geen open rand.

## MOET
1. Bultje, buitenrand lichtkant: (7,41), (8,41), (6,42), (6,43) zijn nu roze 4 op de buitenrand (lichte kleur/open rand). Terug naar r3: index 9 (selout). Vulling binnenin (uit `kaal.png`) laten staan.

## MAG
- (6,44) zwart tussen selout (6,43) en (6,46) op de linkerrand: terug naar r3 (index 9); (7,45), (8,45) zwart mag blijven (onderkant = schaduwkant).
- Losse mauve pixels in het bultje (8,42) en (8,44) uit de reductie: sluiten diagonaal aan op de mondhoeklijn (x9), dus acceptabel; anders terug naar r3.
- Open punten uit keuring r3 (roze koepelstreep x39–44 y23–34, tintjes in de vin (54,38), (52–53,39), (52–53,41), (55,46)) staan nog; niet storend.

Ter info voor Jordi: geen ontwerpvragen.
