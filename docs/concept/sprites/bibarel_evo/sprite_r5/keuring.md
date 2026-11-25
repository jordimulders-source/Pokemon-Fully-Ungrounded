# Keuring r5 (verse keurder, 24 nov)

Uitslag: **BIJNA**

## Eerst blind (1× en 8×, zonder model)
Leest direct als een Pokémon: een gespierde bever met potlood/stam over de schouder, tuinbroek en een gestreepte staart. Het gezicht (Bibarel-ogen, rode neus, witte tanden) is het eerste waar je naar kijkt. Wat opvalt: het borststuk en de zak lezen goed als tuinbroek. De crème broek op de benen is wel erg vlak in het midden, en langs het rechterbeen lopen drie tinten evenwijdig aan de rand. In de linkerdij zit een zwartbruine lijn die harder is dan de rest van de broek.

## Eis 1: trouw aan het model (r10_k8_64)
- Silhouet: 44 px alleen in het model en 50 px alleen in de sprite. Dat komt bijna allemaal door de staart (8 px naar achteren, toegestaan) en de ogen (toegestaan). Verder geen verschil.
- Borststuk, bandjes en zak gemeten tegen de modeltonen (rij 30–43): de vorm komt 1-op-1 overeen, alleen de onderste zoomlijn niet (zie punt 4).
- Toegestane afwijkingen zijn aanwezig en kloppen: broek doorgekleurd tot de enkels, Bibarel-ogen, witte tanden, rode neus, staart naar achteren. Pet/klep niet gekeurd.
- Broekkleur en patroon van het bovenlichaam = r1 (vergelijking `keuring/r1_r4_r5.png`).

## Eis 2: Gen 3 en de checklist uit de SPEC
- Tinten: bruin m/l/h + lijn D, crème c/L/s, oranje 2 + wit/grijs. ≤3 per groep: **OK**.
- "geen rechte lijnen": **open punt voor Jordi**. Zoom r34 (x26–33) en zak r36 (x26–33) zijn 8 px recht, maar komen recht uit het model. De broekgrenzen zelf zijn rond.
- "geen effen vlakken": **BIJNA**. Het buikvlak in r43–49 (x20–40, ±120 px) is één effen crème. Het model is daar ook vlak, maar Jordi's regel gaat vóór.
- "tuinbroekvorm, 1-op-1 uit het model": **OK** (op de dubbele zoom na).
- Kraag van r1, ogen Bibarel, tanden wit, neus rood: **OK** (diff 0 t.o.v. r4).
- Bovenlichaam: geen pixelblur. Schouder rechts heeft licht linksboven en een sikkel rechts: **OK**.

## Reparaties (belangrijkste eerst)
1. **Banding rechterbeen** x48–52, r48–58: crème → L → L → s → K loopt als evenwijdige banden langs de rand. Laat de s-band pas vanaf ±r53 beginnen en breder worden naar onder (sikkel). In r48–52 alleen L tegen de K.
2. **Lijn linkerdij** (19,45),(19,46),(19,47),(20,47),(20,48) staat nu in de donkerste bruintint B. Zet hem in de crème-ramp (s), net zoals de rechterdijlijn (37–38, r46–49) in L staat. De plek komt uit het model (dijlijn, modeltoon 2–3).
3. **Dubbele onderzoom** r42 (L, x25–30) + r43 (s, x25–30): twee evenwijdige lijnen. Het model heeft er één (r42). Houd er één over; de tailleband was een toevoeging van de maker.
4. **Effen buikvlak** r43–49, x20–40: geef het volume volgens Gen 3, met de crème-tinten die er al zijn. Een L-sikkel aan de onderkant/rechts van de buikbolling, aansluitend op de bestaande dijlijnen en de donkere boog in r50–52 (die staat ook in het model). Niet middelen of gladstrijken.
5. **Zwart en bruin om en om op de buitenlijn**: linkerarm onderrand (9,31) D, (9,32) K, (10,33) D, (10,34) K. Maak het één overgang: D tot r31, daarna K. Linkerbeen (15,53) K, (15,54) s, (15,55) K: zet (15,54) op K, of (15,53) op s.
6. **Jordi laten kiezen**: de rechte zoom- en zaklijnen r34/r36 (uit het model) houden of een lichte ronding geven ("geen rechte lijnen" tegenover "1-op-1 uit het model").

Meetplaatjes: `keuring/blind.png`, `keuring/naast.png` (Gemini, model 64, sprite), `keuring/romp.png` (romp 10×, model naast sprite), `keuring/r1_r4_r5.png`.
