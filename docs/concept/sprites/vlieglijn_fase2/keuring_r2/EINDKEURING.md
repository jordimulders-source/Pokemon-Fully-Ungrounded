# Eindkeuring mug r2 (verse keurder, Dragonfly Cave / Gen 3, 21 nov)

Gekeurd: `sprite_r2/mug_r2.png`, met het model (`maat/natief.png`, BOX naar 56×63) ernaast en Ninjask, Beedrill, Volbeat, Masquerain, Skarmory en Metang (`anim_front_gba.png`) op 8×.
Alleen de uitvoering is gekeurd (kleur, schaduw, belijning). Vorm en silhouet zijn bevroren (Jordi: "de vorm is perfect" · "niks opnieuw tekenen"). Alle wissels zijn tintwissels binnen bestaande vlakken. `wissels.py` controleert dat de alpha-diff met r2 0 is.

## Verdict: BIJNA (PASS na MOET A–C)

1. **Hoofdvraag:** ja, op 1× is dit een nette Gen 3-sprite: de pose leest, de ogen lezen als \ /, naald en poten zijn duidelijk. Drie zwakke punten: de twee ledematen onder het lijf vallen samen (Jordi), er zitten nog losse tintspikkels in (Jordi: "blurry") en het achterlijf is vlak.
2. **Volume:** koepel, naald, vleugels en borststuk zijn goed (hooglicht linksboven, schaduw rechtsonder). Poten zijn voldoende. Het achterlijf mist volume: de panelen zijn één vlak p en de schaal heeft alleen een d-randlijn → MOET C.
3. **Zwart:** 28,8 % `#`, met `k` erbij 43 % (Beedrill 25 %, Ninjask 17 %). 69 % van het `#` zit op de buitenrand. Het binnen-zwart zit vooral in het vizier (zwart in het model) en tussen de dunne poten. Daar zou een donkere vlaktint (L 48,44,66 tegen l 70,66,100) de poten laten samensmelten, dus niet omzetten. Wat de sprite te donker maakt is `k` (56,56,66) als selout aan de lichtkant van vleugels en koepel → MAG.
4. **Belijning:** de rand is overal één soort, nergens om-en-om, en er zijn geen open randen (de r1-punten zijn opgelost). Aan de lichtkant van de lichte vleugels is de selout bijna zwart → MAG.
5. **Netheid:** ≤3 tinten per groep. P (slot 6) en L (slot 9) zijn vrij. Wel losse spikkels en een d-k-d-k-streping in de nek → MOET B. Er is geen pillow shading, en buiten de achterlijfrand geen banding.

## MOET (indexen: 1 # · 2 k · 3 d · 4 g · 5 w · 6 P · 7 p · 8 q · 9 L · 10 l · 11 i)
**A. Arm/poot (Jordi: "rechterarm en linkerpoot vallen een beetje samen"), 8 px.** Op 8× gemeten: het gaat om het linker Λ-been (gele knie bij 23–24,44–46), waarvan de top bij (29–30,35–37) ligt, en de poot vanuit het borststuk met de gele schakel bij (35,36–37). Die poot loopt via x31–32 omlaag. Op y36–37 lopen ze zonder grens in elkaar over (`iilllly`). Dit is dus de lezing van de coördinator. De oplossing gebruikt geen lijn: het achterste ledemaat wordt een tint donkerder en de glans komt alleen op het voorste.
- (30,35) (29,36) (30,36) (29,37) (30,37): 11→10 (Λ-top zonder glans)
- (31,36) (31,37) (31,38): 10→11 (de lichte linkerkant van de voorste poot loopt door, zoals op y39–47)

**B. Scherp (Jordi: "hij is nog wat blurry"), 14 px.**
- Koepel (17,17) (16,18): 3→4 (d op de lichtkant)
- Linkervleugel (23,8): 4→5 (gat in de glansstrook)
- Kaak (16,27): 3→4, (17,29): 2→3
- Naaldpunt (5,41): 3→4
- Borststuk (27,29): 7→8
- Nek (27,22) (27,23) (27,24): 3→2 (d-k-d-k-strepen → d links, k rechts)
- Grote vleugel (38,14): 3→4, (54,7): 5→4 (glinster aan de schaduwkant)
- Kleine vleugel (38,22): 4→3, (52,21): 2→3

**C. Volume achterlijf, 13 px.**
- q-hooglicht: (42,36) (42,37) (44,41) (44,42) (37,37) (35,40) (36,40): 7→8
- P-schaduwsikkel: (47,45) (47,46) (38,41) (39,41): 7→6
- schaal-hooglicht: (40,33) (41,33): 2→3

## MAG
**1. Lichte selout aan de lichtkant, 72 px.** Slot 9 wordt opnieuw ingekleurd naar (92,92,108).
- k→9 langs de linkerrand van de linkervleugel (x21–24, y1–14), de bovenrand van de grote vleugel (y1–20), de bovenrand van de kleine vleugel (y17–21) en de bovenrand van de koepel (17–24,15–16)
- #→9 op (16,17) en (15,18)

De volledige lijst staat in `wissels.py` (`SELOUT`). Vergelijkbaar met de grijze vleugelomlijning van Beedrill en Volbeat. Bij de vleugels geeft dit meer lucht. Het zwart in de figuur blijft 28,7 %, maar `k` daalt van 14 naar 9 %.

## Bestanden (keuring_r2/)
- `wissels.py`: de groepen ARM, SCHERP en VOLUME (MOET) en MAG. Uit te zetten met `--geen-mag` en `--geen-moet`. De oude index wordt per pixel gecontroleerd, net als alpha-diff 0.
- `voorstel.png`, `voorstel.txt`, `voorstel_8x.png`: MOET+MAG.
- `vel.png`, rij 1: r2 | alleen MOET | MOET+MAG | model op 8×. Rij 2: de arm/poot-zone (x22–39, y30–49) op 12×, r2 | voorstel | model. Rij 3: r2 | voorstel op 1× en 2×.

## Ter info voor Jordi
- Wil je het geheel lichter, zoals de pootkleur in het model, dan kan l (slot 10) een stap lichter. Dat is een paletwijziging en geen wissel.
