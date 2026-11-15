# Keuring r5 – sneeuwbolslak fase 2 (verse keurder, 15 nov)

Getoetst: `sprite/maker/r5.png` / `raster_r5.txt` / `pal5.py` tegen `sprite/r8_bol_r7.png` (via `meet/px.py`, `recht.py`, `bewaak.py`, een eigen kaart van donkere modelpixels en een telling van tintvlakjes). Ter vergelijking: Glalie, Regice, Walrein, Sealeo en Snorunt (Gen 3) en fase 1. Vel: `keurvel_r5.png` (links r5 8× met de MOET-plekken genummerd, rechts het model op hetzelfde 64-raster).

**Oordeel: FAIL, maar dichtbij.** Er zijn vier kleine MOET-punten (samen ±25 px). Alle vier vallen onder Jordi's eigen punten: aansluiting, kleur, belijning en rechte lijnen.

## (a) Eerste indruk (blind, 1× en 8×)
Op 1× leest hij als het model: ronde kop met oog en blauwe wang, een echte ronde bol met barst en ijspunten, de rode ring, de zijflap en de ijsstaart. Silhouet-diff 0, en de bol is rond: de zijkanten lopen 3–4–3, wat klopt voor een cirkel met straal 10,6. De staart is veel strakker dan in r2/r3b, met lichte linkervlakken per scherf en een zaagrand in `d`. Wat het oog nog trekt:
- De ring is lichter en rozer dan in het model: zalmrood tegenover diep wijnrood.
- Linksonder de bol staat een licht gaatje waar kop, nek, bol en ring samenkomen. Dat is precies de plek waar Jordi zei dat "de aansluiting van de bol op het lichaam niet mooi" is.
- De kopschaduw heeft een rechte horizontale grens.
- Eén staartnaad is in stippen uiteengevallen.
- De bol en de staart zijn iets lichter dan het model (gemiddelde helderheid +12 en +16). De kop en het lijf kloppen (±0 en +6).

## (b) MOET (op volgorde van belang)
1. **Aansluiting bol–lijf linksonder en open ringeinde.** De kopbovenlijn (20–21,38), de bolrand (23,38) en de ring komen niet samen. Op (22,38) en (23,39) staat `c`. In het model zijn die twee pixels donker (L 96 en 78). Het linkereinde van de ring is bovendien open: het rood op (24,40) en (25,41) grenst direct aan het lichte `c` op (23,40) en (24,41). Het model sluit de ring daar af (op (24,40) p15 45, op (25,41) p15 64).
   Gewenst: (22,38) → `d`, (23,39) → `#` en (24,40) → `#`. (25,41) wordt `#` of `r`, zodat het ringeinde een gesloten punt wordt. De lijn blijft 1 px dik. Als (22,39) `d` dan dubbel naast (23,39) komt te staan, wordt (22,39) `c` en begint de neklijn op (22,40). (23,40) en (24,41) blijven licht; dat zijn ze in het model ook.
2. **Ringtint te licht en te roze.** De mediaan van het modelrood is (138,64,73), gelijk aan `r`. Alleen de middenstrook (29–31,42) is in het model `s` (169,71,77), en `t` komt in het model nergens voor. Op r5 is het `t`-vlak (24–29,40–41) 8 px groot en de rest grotendeels `s`: (37–39,40), (34–37,41) en (39,39). Daardoor oogt de ring als zalm.
   Gewenst: grondtint `r`. `s` alleen als middenband op (27–32,42) (staat er al) en hoogstens op het belichte linkerdeel (25–29,41). (34–39,39–41) wordt `r`. `t` hoogstens als glans van 1–2 px, bijvoorbeeld (26,40), of helemaal weg.
3. **Staartnaad x 48–49 onderbroken.** De naad loopt nu (48,30)`a`, (48,31)`d`, (49,32)`d`, (49,33)`a`, (49,34)`b`, (49,35)`a`, (49,36)`d`, (48,37)`d`, en leest daardoor als stippen. Het model heeft hier een doorgaande lijn: (49,33) p15 53, (49,34) L 132 (`a`), (49,35) p15 47.
   Gewenst: (49,33) → `d`, (49,34) → `a` en (49,35) → `d`, zodat de naad ononderbroken van (48,30) tot (44,42) loopt. Dat geeft de staart de definitie waar Jordi om vroeg ("niet goed gedefinieerd"). (KEURING_r4 punt 3 liet x 49 y 33–35 weghalen; dat was een meetfout, want het model heeft die naad wel.)
4. **Kop: rechte schaduwgrens.** De grens tussen `e` en `c` loopt op y 42 recht over 7 px, van (12,42) tot (18,42). Op een ronde kop is dat de meest zichtbare rechte lijn, en Jordi noemt rechte lijnen nu voor de tweede keer. In het model is deze grens zacht (L 227 → 213), dus een bocht van 1 px blijft trouw.
   Gewenst: de bovenkant van het `c`-vlak als boog. Op rij 42 staat `c` alleen op x 14–17: (12,42), (13,42) en (18,42) worden `e`. Op rij 43 wordt (11,43) `e`. Geen rechte stukken van meer dan 4 px.

## (c) MAG
- **Bol:** de glans `w` op (32,36)–(32,37) staat niet in het model (daar is het `c`/`b`, L 205/160). Die mag naar `c`/`b`. Ook (29–31,39) `www` mag `e` worden (model L 226). De bol is +12 lichter dan het model: één of twee extra `b`-sneeuwstrepen in plaats van `e`, bijvoorbeeld op (33–36,22–23), maken de "chaotische sneeuwstorm" iets duidelijker zonder ruis. Tintvlakjes kleiner dan 3 px (8-verbonden): de bol heeft er nu 7, vrijwel alleen bij de ijspunten. Dat is goed, houd het zo.
- **Bol rechts:** op (37–40,26–28) staan `c`, `b`, `a` als drie evenwijdige kolommen van 1 px, wat lichte banding geeft. (39,27) of (39,28) mag `a` worden, zodat de sikkel daar 2 px breed is.
- **Barst, rechtertak:** (37,30)–(37,33) is 4 px recht. Het model verspringt hier tussen x 36 en x 37; één verspringing mag.
- **Staart:** +16 lichter dan het model. De onderste schaduw (y 45–48 `a`) mag iets breder.
- **Onderrand:** (23–27,57) en (28–32,58) zijn twee rechte stukken van 5 px. Het silhouet is bevroren, dus dit alleen veranderen als Claude het silhouet vrijgeeft (bijvoorbeeld 2–3–5–3).

## (d) Goed, niet aanraken
- Silhouet (diff 0) en de ronde bol (zijkanten 3–4–3, ijspunten op de plekken van het model).
- Selout: `d` links en boven, `#` rechts en onder. Er wisselen geen zwarte en blauwe pixels meer af op één rand; de zaagrand van de staart is overal `d`.
- De barst ligt op het model. Het oog en de wang zijn ongewijzigd. De mondlijn (9,47), (8,48), (7,49) staat zo in het model.
- De flap (e → c → b) klopt per pixel met het model: (30,46) `e`, (33,46) `c`, (37,46) en (32,47) `b`.
- De lijfnaad loopt als boog 3–4–3. De onderste staartnaad (48,37) → (44,42) ligt precies op de modellijn.
- Palet `pal5`: de ijstinten zijn cyaan zoals het model, met stappen van ±30–40. De kop komt qua helderheid exact overeen met het model.

## Nagaan KEURING_r4
Punten 1, 2, 4, 6, 7, 8 en 9 zijn goed opgelost.
- **Punt 3 (staart):** opgelost op de zaagrand en de eilandjes. De verwijderde naad op x 49 y 33–35 moet terug (zie MOET 3).
- **Punt 5 (ring):** de onderrand en de ruis zijn opgelost. Het lichtere rood is echter verder van het model af komen te staan (zie MOET 2).
