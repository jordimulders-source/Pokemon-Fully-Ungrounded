# Nachtaap fase 3, ronde 7 opties: vormshading lijf + staartwortel

Basis: `../ronde6/nachtaap_fase3.png` + `normal.pal` (palet ongewijzigd). Ik heb alleen de vachttinten 1–5 gebruikt, binnen de omtrek.
Bestanden:
- `opties.py`: de rijen x20–47 met de hand getekend als tekstraster, plus een kleine pixeltabel `BUIK`.
- `check.py`: het bewijs.
- `vel.py` maakt `vel_opties.png`.
- `show.py`: tekstdump.

Jordi (letterlijk):
- "ik vind nu wel met deze shading dat het bovenste been weer half uit het lichaam lijkt te steken"
- "het zit niet buiten de sprite om, maar in de sprite zelf / de shading"
- "ja een lichaam is niet bepaald 1 vlak namelijk en een staart groeit nooit volledig egaal ergens uit"
- Eerder: "alle onderdelen lijken nu los van elkaar te zitten".

## Studie (8×, kort)
- **Machamp (front en back), Hariyama:** het lijf bestaat uit meerdere massa's. Elke massa heeft een eigen lichte kern linksboven en een donkerdere rand. De overgang tussen twee massa's is een **korte plooi in de schaduwtint**. Die plooi begint bij een inham in de omtrek en loopt dood in de basistint. Een gesloten lijn rond een onderdeel komt niet voor.
- **Vigoroth, Primeape, Slaking:** het been sluit aan met een grijze plooi van 3–5 px vanaf de omtrek. Het hooglicht van het been loopt niet door in het hooglicht van het lijf: het dooft uit in de basistint van de heup. De basistint mag een groot rustig vlak zijn. De vorm komt uit de **vorm van de licht- en schaduwvlakken** (rond, niet diagonaal-recht).
- **Medicham:** het lijf is dun, maar ook hier heeft elk deel een eigen kern.
- **Staartwortel (Zangoose, Aipom, Furret, Linoone, Mightyena, Raticate):** de staart heeft een eigen lichtkant die doorloopt tot in de heup. Aan de lijfkant van de wortel zit een donkere wig of kraag (schaduw in de oksel van staart en heup). De staart komt dus nooit in dezelfde tint als de heup uit het lijf. Ambipom staat er alleen als `anim_front.png` (gen 4-stijl); dezelfde opbouw.
- **Foto 6 (muriqui-tekening):** het opgeheven been groeit uit een brede heup. De rug is een rustig vlak met een eigen ronding. Waar dij en romp elkaar raken zit een zachte schaduw, geen lijn.
- **Foto 7 (gibbon, rug):** de benen komen uit het bekken. De dij is breed in de heup. Er is schaduw in de lies en tussen bil en dij. De rug is één vlak met een lichte bovenrand.

**Diagnose van ronde 6:** de 5|4-grens van het been loopt recht door als de 5|4-grens van het lijf (van x35/r30 diagonaal naar x24/r39). Daardoor horen de linkerhelft van het been en de rug bij één licht vlak, en alleen de rechterhelft "steekt uit". De 4|3-grens is óók een rechte diagonaal. Gevolg: drie platte schijven in plaats van massa's. De staart (x45–47, r35–40) loopt egaal in 3 de heup in.

## Opties
Beide opties delen:
- **Been-aanzet:** het hooglicht van het been (5) eindigt afgerond op r31–32 en buigt daarbij iets naar rechts (naar de heup). Het raakt het licht van de rug niet meer.
- **Rug/borst:** een eigen lichte kern (x21–30, r31–37), afgerond naar onderen.
- **Heup:** een bolle massa. De 4|3-grens is een curve (x40→41→41→40→39) in plaats van een rechte diagonaal, met een kleine heupbol naar rechtsonder (r42–43, x37–39).
- **Lies:** een korte zachte plooi (3) vanaf de inham onder de buik (x36, r42–43).
- **Onderste dij:** de lichte bovenkant van het onderbeen loopt een stukje de heup in (r44 x40–44, r45 x43–44). Zo groeit ook dat been uit de heup.
- **Buik:** de schaduw (3) buigt onderaan om de buik (r41–44, x28–31).
- **Staartwortel:** de staart krijgt een eigen lichtkant die doorloopt tot r35–37 (x45–46). Aan de heupkant zit een plooi in 2 (x43–44, r35–37), en die begint precies in de inham van de omtrek. Onder de wortel gaat de staart over in de schaduw van de heup.

- **A, kern + rand (65 px):** de rustigste versie. Onder de inham tussen been en rug zit een plooi van 2 px (3). Het been eindigt als cilinder bóven op de heup, in de basistint, zoals bij Vigoroth en Primeape. Het middenvlak van de romp is één rustige basistint met ronde licht- en schaduwvlakken eromheen.
- **B, heup-massa (75 px, mijn voorkeur):** de plooi vanuit de inham is langer, 5 px in 3 als zachte boog: (29,30) (30,31) (31,32) (31,33) (32,34). Hij loopt dood in de basistint en sluit dus niets af. Rechts van de plooi loopt het hooglicht van het been door in een afgeronde heupkern (x33–36, r31–35). Dij en heup lezen zo als één massa, en die massa staat los van de rugkern. Het been groeit dus duidelijk uit de heup, en de plooi laat zien dat de dij vóór de rug langs gaat. Onder de staartwortel zit een kleine schaduwkraag (r38 x45 = 2). De buik loopt in r44 iets verder in 3.

Afgewezen tijdens het werk (niet opgeleverd):
- Een losse hooglichtvlek midden op de heup: die leest als vlek.
- Het heuplicht als diagonale voortzetting van het been, met een rechte plooi ernaast: dat leest als een diagonale streep of lint.

## Bewijs (`python3 check.py`)
- **A:** 65 px gewijzigd, **alpha-diff 0**, zone x28–46 r29–45, alleen tinten 1–5 → 1–5.
- **B:** 75 px gewijzigd, **alpha-diff 0**, zone x28–46 r29–45, alleen tinten 1–5 → 1–5.
- **Bevroren vakken: 0 px** in beide opties:
  - kop/gezicht/maan x0–19 r14–43
  - vuistarm x0–25 r14–31
  - healerhand + gloed x1–23 r44–63
  - staartspiraal x≥48
  - opgeheven voet r0–13
  - onderste voet x50–63 r48–63
- Het palet is identiek.
- **Open randen:** 0 nieuw, en 0 in de werkzone. De 27 treffers in de hele sprite zijn allemaal index 12: de turkooise gloedrand van de healerhand, gelijk aan ronde 6.

## Eigen check (vel: 3× licht en donker, 1×, 8× naast ronde 6, foto 6/7, Vigoroth/Zangoose/Aipom, Machamp-rug)
- **Ronde 6:** op 3× en 1× zie ik de lichte driehoek van been en rug.
- **A:** op 3× en 1× is de driehoek weg. Het been staat op de heup, de rug heeft een eigen licht en de staart heeft een eigen aanzet. Het lijf is rustiger dan in ronde 6, met de vorm in de ronde grenzen.
- **B:** op 1× lees ik een dij die uit een bolle heup groeit. De rug is een aparte ronde massa met een zachte plooi ertussen, en de staart komt met een donkere kraag uit de heup. Er zijn geen gesloten lijnen.
- Smaakkeuze voor Jordi: A (rustiger, GF-basistint) of B (massa's sterker). Ik zou zelf B kiezen.

## Lessen
- "Been steekt half uit het lijf" kan puur door de shading komen. Dat gebeurt als de 5|4-grens van het been als rechte lijn doorloopt in de 5|4-grens van het lijf. Breek die grens: laat het hooglicht van het been afgerond eindigen of naar de heup buigen, en geef het lijf een eigen kern.
- Een plooi tussen massa's begint in een inham van de omtrek en loopt dood in de basistint (3–5 px). Een plooi die doorloopt tot de schaduw sluit het onderdeel af en geeft "losse onderdelen".
- Een losse hooglichtvlek midden op een massa leest op 3× als vlek. De kern moet aansluiten op een rand of op het licht van een ledemaat.
- Bekijk vellen in uitsneden van ≤ 800 px breed. Grotere vellen worden verkleind getoond, en dan zie je de 1 px-plooien niet.
