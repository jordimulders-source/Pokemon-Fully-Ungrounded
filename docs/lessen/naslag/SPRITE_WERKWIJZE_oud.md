# Sprite-werkwijze: zo maken we elke nieuwe Pokémon-sprite

> **Kort: lees eerst `docs/lessen/SPRITE_KERN.md`.** Dit bestand is naslag.

**Vastgesteld door Jordi (25 okt):** "ik denk dat we de beste methode hebben gevonden om sprites te maken. Jouw way of working mag je vast leggen als de manier, uitgebreid en stap voor stap, zodat alle nieuwe gesprekken vanaf nu het zo oppakken."

Bewezen op de **kolibrie** (Ghost/Flying, eindvorm: van eerste schets tot goedgekeurde sprite in ±1 dag) en de **olinguito v2** (Dark-starter, fase 1: na 30+ mislukte rondes in de oude aanpak, nu in 5 silhouet- en 4 kleurrondes "het beste olinguito-ontwerp wat ik tot nu toe heb gezien"). Achtergrond: `RETRO_KOLIBRIE.md`, `RETRO_OLINGUITO.md`. Deze werkwijze vervangt stap 1–5 bovenaan `FAKEMON_DESIGN.md` waar ze verschillen.

## Kern in vijf zinnen
1. **De vorm wordt vastgelegd vóór er één kleurpixel bestaat**, en Jordi keurt die vorm als silhouet op ware grootte.
2. **De vorm komt van iets echts:** een foto van het dier in de juiste pose, of het 3D-poppetje dat Jordi koos; nooit van zelfgebouwde cirkels en driehoeken ("Pokémon designen is geen cirkels en driehoeken werk").
3. **Eén maker-agent per sprite die doorwerkt** (SendMessage) en **één keurder** die strenger is dan Jordi; Claude kijkt zelf eerst en stuurt terug.
4. **Goedgekeurd = bevroren**, bewezen met een pixeldiff; elke ronde raakt alleen benoemde zones.
5. **Jordi's woorden letterlijk** in `SPEC.md`; een nieuwe opmerking vult aan, vervangt niet.

## Stap 0. Voorbereiding (Claude, vóór alles)
- Lees `SPRITE_NORM.md`, `SPRITE_OPDRACHT.md`, `SPRITING.md` §0–§8 (Dragonfly Cave), `FAKEMON_DESIGN.md`, `FAKEMON_CHECKLIST.md` (bouwtype) en dit bestand.
- Maak de map `docs/concept/sprites/<naam>/` met `referenties/` en `SPEC.md` (onderdelen, bron/referentie, Jordi's woorden letterlijk, status bevroren/open, afgekeurd).
- **Types, abilities en evoluties uit de repo**, nooit uit het geheugen.
- Zet elke foto die Jordi stuurt meteen in `referenties/` (foto's in de chat zijn na de sessie weg; als een foto niet als bestand binnenkomt, punt voor punt overnemen en dat melden).

## Stap 1. Ontwerp: pose en kenmerken (met Jordi, geen pixels)
- Jordi geeft het idee, de pose (schets of foto) en referenties. **Vraag om een foto van het echte dier in de gewenste pose**; dat was beide keren de doorbraak (kolibrie: de drinkende kolibrie; olinguito: de boomfoto + kopfoto).
- **Ontwerpschetsen alleen als hulp om te praten**, niet als bron voor de sprite. Lukt een pose na 2 schetsrondes niet: stop met schetsen en ga naar een echte bron (foto of 3D-poppetje).
- **Viervoeters en lastige 3/4-poses:** het 3D-poppetje (`docs/concept/sprites/olinguito_v2/silhouet_kolibriemethode/pop3d.py` + `silhouet.py`): ellipsoïden in diercoördinaten, met **lijf-hoek, kop-hoek (kop draait meer naar de kijker dan het lijf), camerahoek en kanteling** als knoppen. Laat Jordi kiezen uit een raster van hoeken (olinguito: "B2" = lijf 40°, kop 49°, kantel 8°, Linoone-perspectief). Een te schuine hoek (52°) maakt alles samengeknepen.
- **Vogels/vliegers en dieren met een simpele bouw:** een foto in de juiste pose is genoeg (kolibrie).
- Zijaanzicht mag als het bij het dier past (Swellow, Relicanth, Seviper, Skarmory).
- **Gokken is verboden:** is een kenmerk twee keer mis (kolibrievleugels), vraag Jordi om een referentie of een krabbel. Zijn krabbels over het silhouet gaven per stuk de meeste vooruitgang.

- **Een profiel opblazen en draaien geeft geen 3/4** (kolibrie pre-evo, 3 nov): het lijf draait mee, maar de kop blijft een platte profielkop met het oog op de zijkant. Gen 3-driekwart is gesmokkeld: ronde kop als eigen bol bovenop/voor het lijf, gezicht naar de kijker, oog in het middelste derde van de kop. Bouw de kop in 3D als eigen bol; een overlapeis met een profiel geldt alleen voor het lijf. Toets elk hoekenvel vóór Jordi op 8× naast Taillow/Starly op de kop, niet alleen op de houding; plak het oog niet als plaatje (dat verbergt dat het op de zijkant zit).
- **Een 3D-render leest door schaduw; het silhouet moet dezelfde vormen tonen zonder schaduw** (kolibrie pre-evo): kop, borst, staart en bek moeten in de omtrek zelf een inham of uitsteeksel hebben. Pas het model aan tot het verkleinde silhouet alleen al leest; repareer het niet achteraf met de hand. Toets: render en silhouet op 1× naast elkaar.
- **Toon een silhouet uit een model altijd als rode omtrek óver de render** (niet alleen als losse zwarte vlek ernaast): een zwart vlak naast een belichte render lijkt een andere vorm, ook als de omtrek klopt (kolibrie pre-evo: 95% gelijk, toch "compleet verschillend"). En: niet tussen twee keuzes van Jordi het model ongevraagd veranderen; elke wijziging = nieuw voorstel naast het gekozen model.
- **Blender (bpy) werkt in de cloud** (kolibrie pre-evo): `python3.11 -m pip install bpy scikit-image` + `apt-get install libegl1 libgl1-mesa-dri`, Workbench-render; bouw de huid als smooth union van afstandsvelden (één geheel, geen losse bollen) en toon eerst een rondom-vel. Een wit gerenderd model verkleind tot 4 tonen (toonkaart) is een goede gids voor de schaduw.
- **"Slordig" meetbaar maken:** clusterscript (geen tintvlakken < 3 px), ≤ 3 tinten per kleurgroep, helderheidsstappen gemeten tegen Taillow; dat gaf de grootste sprong in netheid.
- **Twijfelt Jordi aan een silhouet, vraag eerst wat hij ziet** vóór er een kleurronde start.

## Stap 2. Silhouet op 64×64 (één kleur) → Jordi keurt
- **Bron = de foto of render, verkleind; de massa daarvan is heilig.** Twee mislukte routes, niet herhalen:
  - Een agent die het silhouet "vrij" tekent op de pose verliest de massa: te dun, "lijkt totaal niet op het origineel" (olinguito hand-rondes 1–3).
  - Een script dat poten/klauwen dikker maakt en alles automatisch verkleint klontert samen.
  - Een automatische spritegenerator (3D-poppetje of 2D-tekening → sprite via de Dragonfly Cave-methode, tak `claude/awesome-dirac-c7l6xv`, 25 okt) kwam niet tot een goed resultaat; Jordi stopte die aanpak.
- **Wat werkt:** de bron direct verkleinen (olinguito: B2-render, 1131 px; kolibrie: foto-omtrek punt voor punt), en dan **met de hand alleen de dunne delen** repareren in benoemde zones: klauwen (2 haakjes aan elkaar vast), oor, voorkant van de kop, spleet tussen poten, staartboog. Buiten die zones ±1 px, bewezen met een diff.
- **Minimale dikten:** snavel/dunne delen ≥ 2 px, poten ≥ 5–6 px, geen spleten van 1 px tussen poten die naast elkaar staan.
- **Leesbaarheid:** toets of de ruimte direct onder de buik leeg is (hangende slierten lazen als poten/mug); vier poten in vier kolommen; de kop een eigen onderdeel.
- **Formaat volgt de vorm:** het formaatdoel mag nooit winnen (olinguito werd dun door het doel van 950 px; 1100–1200 px is prima, zoals Linoone/Zigzagoon). Een eindvorm kan klein zijn als hij slank is (kolibrie ±1000 px, gelijk aan Crobat).
- **Vel voor Jordi:** onderlaag/foto | silhouet 4× | silhouet over de onderlaag | silhouet 1×, naast 3–5 echte Gen 3-silhouetten van hetzelfde bouwtype. Claude keurt eerst zelf op **pose én massa** (overlay), dan pas Jordi.
- **Goedgekeurd silhouet = bevroren** (alpha-diff 0 in alle volgende rondes). Vastleggen in SPEC.md.

## Stap 3. Kleur (maker-agent, op het bevroren silhouet)
- **Eén maker-agent**, die doorwerkt met SendMessage. In de opdracht altijd: SPRITE_NORM, SPRITE_OPDRACHT, SPRITING §0–§8 + lessen, de Dragonfly Cave-gids gericht, SPEC.md, referenties, Jordi's woorden letterlijk.
- **Eerst een Game Freak-studie** (kort, in een tabel): 4–5 echte Gen 3-sprites van hetzelfde bouwtype op 8×: tinten per kleurgroep (3–4), gekleurde selout aan de lichtkant en zwart alleen aan de schaduwkant, licht linksboven, schaduw die de vorm volgt, hoe ogen/maskers/vacht zijn opgebouwd. Daarna pas tekenen.
- **Palet uit het goedgekeurde ontwerp** (de kleuren van het poppetje of de foto), 16 kleuren met index 0 transparant; tinten per groep eromheen bouwen.
- **Met de hand** als tekstraster (één teken per paletindex), per onderdeel; geen filters of automatische shading in het eindresultaat.
- **Bekende valkuilen** (elke keer gecontroleerd):
  - Kop als **helm**: harde rechte grenzen tussen kleurvlakken → één kleurfamilie, volume via licht/schaduw, gebogen naden.
  - **Ruis**: spikkels/plukjes overal → grote rustige vlakken, hooguit 2–3 plukjes aan de rand.
  - **Plat (2D)**: bol lijf/kop met kernschaduw en een hooglicht dat de ronding volgt; cilinders (staart, poten) met een licht- en een schaduwkant.
  - **Mini-oog op een donkere kop**: zwart bovenlid + glans + lichtere iris tegenover de glans (Corviknight/Kilowattrel), geen witte stip.
  - Verre ledematen in de schaduwtint, gescheiden met de omlijningsbasis, niet met zwart.
  - Klauwen als gebogen haakjes met licht/schaduw, niet als rechte stokjes.
  - Open randen (schaduw/basis naast transparant) en losse pixels: altijd met een script nalopen.
- **Vel:** de sprite 1× en 4× op licht én donker, naast het ontwerp, de vorige ronde en 5 referenties.

## Stap 4. Controle vóór Jordi
1. **Claude kijkt zelf** (8× + 1×, naast het ontwerp). Een zelfgenoemd zwak punt van de maker = automatisch terug. Stuur terug met concrete zones en Jordi's woorden; bevries wat goed is.
2. **Onafhankelijke keurder** (een andere agent, ≥ 10 echte sprites, licht en donker, alle richtlijnen PASS/FAIL, twijfel = FAIL, smaakkeuzes apart "voor Jordi"). Dezelfde keurder mag rondes volgen; vóór "af" altijd **één verse keurder** die eerst zelf oordeelt en pas daarna de oude keuringen leest (vond bij de kolibrie nog open randen).
3. **Keurdersadvies dat een goedgekeurd ontwerp raakt** (bv. "masker dunner") is een vraag aan Jordi, geen opdracht aan de maker.
4. Pas als het door 1 en 2 komt: naar Jordi, met een vel en een korte lijst keuzes.

## Stap 5. Reparatierondes
- Alleen wat Jordi of de keurder noemt; benoemde zones, pixelbudget, diff-bewijs buiten de zones.
- **Kleine reparaties zijn klein**: Jordi vond olinguito ronde 3 al "het beste"; ronde 4 was 53 px.
- Wat Jordi goedkeurt wordt bevroren in SPEC.md; afkeuringen gaan onder "Afgekeurd".

## Stap 6. Afronden
- Eindversie in `docs/concept/sprites/<naam>/af/` + vel; SPEC.md, `CHANGELOG.md`, Stand van zaken in `CLAUDE.md` bijwerken; lessen naar het passende `docs/lessen/`-bestand.
- Daarna pas in een **latere fase voor alle soorten samen** (Jordi, 5 nov: "we bouwen eerst designs met sprites"): frame 2, rugsprite, icoon, shiny-palet (skins-regel), naam en data (incl. y-offset).

## Kosten en tempo (ter oriëntatie)
- Een maker- of keurderronde kost ±150–400k agenttokens; zuinig: één maker, één keurder, kleine vellen, geen parallelle experimenten.
- Commit en push na elke ronde (ook interne), zodat niets verloren gaat.
- **Poppetje eerst passend op de foto, dan pas cute** (kolibrie pre-evo, 2 nov; Jordi: "waarom wijkt dit zo immens veel af van het silhouet?"): nooit een handsilhouet én een los poppetje naast elkaar. Volgorde foto → poppetje → silhouet. Meet de overlap van het poppetje met de foto-omtrek (`kolibrie_pre/pop3d/pas_foto.py`, zoekt de maten van lijf/kop/staart, ≥ 85%) en doe verhoudingswijzigingen (grotere kop, korter lijf) daarna in 3D, als raster van standen voor Jordi.
- **Poppetje moet ±100% op het goedgekeurde silhouet liggen** (kolibrie pre-evo, 2 nov; Jordi: "79% overlap is waarom het fout gaat"): ellipsoïden die op 79–88% passen geven een ei/pinguïn. Werkt wel: het goedgekeurde silhouet zelf **opblazen** tot 3D (hoogteveld = wortel van de afstand tot de rand, kop/vleugel eigen bolling, delen gekleurd en belicht): `kolibrie_pre/pop3d/opblazen.py`, 98–100% overlap.
- **Keurder nooit inperken tot "alleen afwerking"** (kolibrie pre-evo r5, 3 nov; Jordi: "dit is echt niet goed gekeurd, je volgt de instructies gewoon niet"): de eindkeurder toetst altijd ook of het op 6–8× naast Gen 3-sprites leest als sprite (binnenbelijning per onderdeel, oog, contrast), niet alleen de lijst van de vorige ronde. Reparaties van een keurder gaan via de maker en daarna opnieuw langs de keurder; Claude legt het resultaat zelf op 6–8× naast 2–3 echte sprites vóór Jordi. Een open punt "nog niet zo af als X" moet expliciet afgesloten zijn.
