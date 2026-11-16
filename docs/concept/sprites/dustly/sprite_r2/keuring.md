# Keuring Dustly r2 (verse keurder, 16 nov)

**Oordeel: FAIL (klein): 5 pixels.** Na deze reparaties PASS; een nieuwe volledige keuring is niet nodig, een pixeldiff (alleen deze 5 pixels gewijzigd) volstaat.

## Eis 1: trouw aan het model (r6_a)
- Silhouet: alpha-diff 0 met de kale reductie (`basis/kaal_64.png`, 11 px omhoog geschoven). Losse wolkjes rechtsboven/rechts en de slierten onderaan staan op hun modelplek.
- Toonverhoudingen (gemeten, model-helderheid per spritetint): idx3 78, idx4 100, idx5 134, idx6 161, oplopend zonder overlap in de mediaan; correlatie sprite↔model 0,81. Per 3×3-blok volgt de sprite het model: donkere kern rond gezicht en midden-onder, lichter linksboven, rechts en rechtsboven, lichte bult rechtsboven. Afwijkingen alleen op de buitenlijn (verwacht).
- Gezicht: beide ogen kloppen met het model (links: wit met pupil rechtsonder en een witte sliert rechts ervan; rechts: groot wit met pupil linksonder en een witte sliert links). Hoektanden binnen 1 px van het model. De mond in het model zakt in het midden ±1 rij (lichte grijns); de kale reductie zelf legt de lijn ook op rij 34, dus geen eis.
- Bultlijnen: ronde bult rechts, lijn onder de mond/kin links-onder en de bovenste bultlijn zijn aanwezig. Lichtrand roze-oranje linksboven langs de rand tot ±rij 33 (model ±rij 30–33): goed.
- Kleur variant A zoals gevraagd (minder zwart, kleurrijker); tint niet getoetst.

## Eis 2: Gen 3
- 9 kleuren + transparant; buitenlijn 1 px, donker aan de schaduwkant (links-onder), gekleurde selout (roze) aan de lichtkant, middentoon rechts waar het model licht is. Leest op 1× en 2× (licht en donker) duidelijk als wolk met gezicht.
- Gevonden fouten (clusterscan 8-conn + losse-pixelscan):

## Reparaties
1. **(14,43): idx1 → idx2.** De onderlijn links-onder loopt (14,41)=2, (14,42)=2, (14,43)=1, (15,44)=2: zwart en donkerpruim om en om op één rand (Gen 3-regel). Model daar 82, geen zwart.
2. **(41,29): idx2 → idx3.** Losse donkere pixel midden in de lichte bult rechts (eis: geen losse omlijningspixels in een vlak). Het model heeft daar een zacht vlekje (72 tegen 90 eromheen) = idx3-niveau, geen lijn.
3. **(14,22): idx8 → idx4.** Los oranje puntje (1 px) binnen de rand; model daar grijs 97, geen glans. Tintvlakje < 3 px.
4. **(12,25): idx8 → idx4.** Idem; model 129, geen oranje.
5. **(18,29): idx2 → idx3.** Losse donkere pixel tussen de ogen (ruis: rij 29 x15–20 = 1,2,4,2,3,2). Model 62 = een zacht vlekje, geen lijn; met idx3 blijft het vlekje maar verdwijnt het spikkeltje.

Niet aangeraakt laten: (13,26) en (24,26) (bovenrand van de ogen, staat in het model), (16,29) en (20,29) (ooglijnen), de onomlijnde slierten en wolkjes.
