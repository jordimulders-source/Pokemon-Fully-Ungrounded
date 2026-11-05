# Overdracht great potoo: prompt voor een nieuw gesprek (5 nov)

Jordi stopte het vorige gesprek ("begin maar helemaal opnieuw", "stop maar"). Het 3D-werk in `model3d/` is **afgekeurd**: niet op voortbouwen, alleen als voorbeeld van wat misging. Plak de prompt hieronder in een nieuw gesprek.

---

We beginnen opnieuw met de **great potoo** (fakemon voor Pokémon Fully Ungrounded). Lees eerst, vóór je iets maakt:
`CLAUDE.md`, `docs/lessen/SPRITE_WERKWIJZE.md`, `docs/lessen/SPRITE_NORM.md`, `docs/lessen/SPRITE_OPDRACHT.md`, `docs/lessen/FAKEMON_DESIGN.md`, en `docs/concept/sprites/potoo/SPEC.md` + `ontwerp/ONTWERP.md`. Bekijk de foto's in `docs/concept/sprites/potoo/referenties/` zelf, groot en met een raster.

**Wat vastligt (Jordi, letterlijk in SPEC.md):**
- Losse soort, één stage, **Ghost/Normal**. Basissoort *Nyctibius grandis*.
- Het wordt een **Pokémon, geen nagemaakte potoo** ("we gaan niet een potoo namaken", "we maken een pokemon").
- Pose: driekwart naar links, licht voorover hangend, **bek open** (de sprite die je het meest ziet). Op een onzichtbare tak (zoals Swellow/Noctowl), klauwen verborgen, geen tak in beeld.
- Kleur: **heel lichte vacht** als contrast; **pikzwarte ogen zonder glans, zoals Drifloon**; mond geestblauw/paars. Het geestachtige zit **alleen in de kleuren en de muil**. Een paar **schorsachtige vlekken** (sneeuwcamouflage, het Hisui-Zorua-idee).
- **De muil is echt een snavel zoals op de foto's**: klein donker haakje dat omlaag krult, dunne lichte mondrand, de onderkaak een brede schep met een **spitse punt**, de rand **golft naar de punt toe**, de mondhoeken ver naar achteren aan de zijkant van de kop. Geen lipschijf, geen eendensnavel, geen bollen.
- Geen zichtbare roep of geestslierten. De platte-kop-zijfoto (`jordi_great_potoo_vooroverhangend_bek_open.webp`) niet gebruiken voor de kop.
- **Eerst een 3D-model van de hele Pokémon** (niet alleen de kop), dan pas een silhouet. Jordi: "Voordat je een silhouet bouwt, bouw je eerst een 3d model", "de hele pokemon moet een 3d model worden", "check uit meerdere hoeken of het klopt met het origineel".

**Wat in het vorige gesprek misging (niet herhalen):**
1. Gokken in plaats van meten: lijf te dun, vleugels los van het lijf, kop generiek, oogpositie fout. Jordi: "kijk eens naar het bronmateriaal, je bent aan het speculeren", "stop met het giswerk".
2. De snavel steeds opnieuw uit bollen/formules opgebouwd: "de snavel is nog helemaal niet goed", "je maakt er een lipschijf van". Jordi moest elk detail voorkauwen ("waarom moet ik dat allemaal voorkauwen?"): kijk zelf naar vorm, punten en golving.
3. Een lijn op een 2D-plaatje tekenen is geen model: "dan is het de vraag of de verhouding nog klopt".
4. Rommelige tussenresultaten gestuurd: losse pixels, strepen en spikkels rond de snavel ("kijk wat er allemaal voor rotzooi rondom die snavel zit"). **Stuur alleen een schoon resultaat** dat je zelf groot hebt bekeken en naast de foto's hebt gelegd.
5. Te veel kleine rondes en tussenberichten. Werk door tot iets klopt.

**Aanpak die Jordi wil:**
- Een **echt 3D-model** van de hele vogel, met verhoudingen die gemeten zijn op de foto's (lijf ±1,3–1,4× zo breed als de kop; vleugels volgen het lijf van net onder de kop tot over de staart; kop zonder nek; staart lang). Kies zelf een geschikt middel (bijv. een nette mesh/SDF-opbouw in Python, of Blender als dat beschikbaar is) en zorg voor een **schone render** (gladde vormen, nette omlijning, geen voxelruis).
- Daarna de Pokémon-aanpassingen (grotere kop/ogen/snavel, lichte kleuren) als bewuste, benoemde stap bovenop het gemeten model.
- **Controle vóór je iets stuurt:** render op de hoeken van de foto's met de foto-omtrek eroverheen, plus minstens 4 andere hoeken (zij, achter, schuin). Noem zelf wat nog afwijkt; een zwak punt dat je zelf ziet = eerst repareren.
- Pas als Jordi het 3D-model goedkeurt: silhouet op 64×64 (stap 2 van de werkwijze).

Foto's (in `referenties/`): `jordi_great_potoo_bek_open_drieluik.webp` (bovenste: kop 3/4 met open bek, het beste bronbeeld voor kop en snavel), `jordi_great_potoo_tak_bek_open_volledig.png` (hele vogel 3/4, bek open), `jordi_great_potoo_nacht_voor_volledig.webp` (van voren), `jordi_great_potoo_stomp_voor.png`, `jordi_great_potoo_wit_zijaanzicht.png`, `jordi_great_potoo_illustratie_rug_staart.png` (staart/rug). Ontwerpkeuze kleuren: `ontwerp/model_c2.png`. Oogreferentie: Drifloon (`graphics/pokemon/drifloon`).

Antwoord in het Nederlands, kort. Werk op de branch die het gesprek krijgt; commit en push na elk afgerond stuk.
