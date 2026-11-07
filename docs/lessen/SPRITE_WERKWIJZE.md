# Sprite-werkwijze (compact)
Regels en eisen: `SPRITE_KERN.md`. Hier alleen de stappen en de commando's. Oude uitgebreide versie: `naslag/SPRITE_WERKWIJZE_oud.md`.

## Checklist
Jordi 3 nov: "het is elke keer opnieuw dat we instructies vastleggen die je elke keer opnieuw weer overslaat" → "doe allemaal". Daarom afgedwongen, niet alleen opgeschreven:
1. **Keurslot:** `.claude/hooks/sprite_keurslot.py` blokkeert elke afbeelding uit `docs/concept/sprites/` naar Jordi zonder `<bestand>.keuring.md` (nieuwer dan de afbeelding, met `Bron:`, 8×, 1×, per onderdeel "lijkt op / wijkt af in", `Oordeel: PASS`). Uitzondering: `docs/concept/sprites/showcase/` (vellen van al goedgekeurde sprites om te tonen, Jordi 5 nov). Het slot geldt alleen voor spritewerk, niet voor andere afbeeldingen buiten die map. Niet omzeilen (geen kopie buiten die map sturen).
1. **Keurslot:** (uitzondering, Jordi 7 nov: tekenbases/vergelijkingsvellen waar Jordi zelf overheen tekent mogen door met `<bestand>.tekenbasis.md` met "Tekenbasis: <waarom>"; nooit voor iets ter beoordeling) `.claude/hooks/sprite_keurslot.py` blokkeert elke afbeelding uit `docs/concept/sprites/` naar Jordi zonder `<bestand>.keuring.md` (nieuwer dan de afbeelding, met `Bron:`, 8×, 1×, per onderdeel "lijkt op / wijkt af in", `Oordeel: PASS`). Niet omzeilen (geen kopie buiten die map sturen).
1. **Keurslot verwijderd** (Jordi, 6 nov: "die keurcontrole is echt bizar, haal die eraf"; hij blokkeerde ook referentiebeelden). Keuren blijft een werkafspraak: geen sprite naar Jordi zonder eigen controle en, bij een mijlpaal, een verse keurder.
2. **Keurvel:** `python3 tools/grounded/keurvel.py -o vel.png --werk werk.png --bron <echte sprites/foto's> --zoom x0,y0,x1,y1` → werk naast de bronnen op 8× en 1× (licht/donker) + close-ups, en een keuringssjabloon.
3. **Referentie eerst, per onderdeel** (hand, voet, kop, staart, patroon): 2–3 echte sprites of Jordi's eigen plaatje (stuurt Jordi een afbeelding, dan is díe de bron, niet de sprite van die soort uit de repo). Kenmerken zelf tellen/controleren op een close-up voor iets op een referentievel komt.
4. **Eén afwijking of twijfel = niet sturen.** Toets of het **leest** als een echte Pokémon, niet of het doet wat gevraagd werd.
5. **Onafhankelijke keurder bij elke mijlpaal** (pose akkoord, silhouet, kleur, af), vóór Jordi; zijn oordeel gaat in de keuring.
6. **Ritme:** een ronde helemaal afmaken, dan pas sturen; berichten van Jordi tijdens het werk verzamelen en samen verwerken, geen patch per bericht.
7. **Gereedschap per onderdeel:** het 3D-poppetje alleen voor massa/pose; dunne delen (handen, klauwen, vingers, oren) in de pixelstap naar een echte sprite, aangepast aan arm/maat/richting (nooit geplakt).

**Mappen:** `docs/concept/sprites/<naam>/` met `SPEC.md` (Jordi letterlijk, bevroren/open/afgekeurd), `referenties/`, `blender/`, `af/`.

| # | Stap | Wie | Klaar als |
|---|---|---|---|
| 0 | Types/evoluties uit de repo; SPEC en referenties klaarzetten | Claude | SPEC bestaat |
| 1 | Ontwerp: pose + kenmerken, foto van het echte dier | Jordi + Claude | Jordi kiest |
| 2 | Bron voor de vorm: foto in de juiste pose, óf (bij lastige 3/4) 3D-model in Blender met rondom-vel + 3 driekwart-standen | Claude | Jordi kiest |
| 3 | Silhouet uit de bron (foto-omtrek of render verkleind), dunne delen met de hand; bij een model: rode omtrek over de render | Claude/maker | Jordi keurt; bevroren |
| 4 | Kleur: studie (4–5 echte sprites op 8×) → tekstraster met de hand; toonkaart als schaduwgids | maker-agent | controlescript schoon |
| 5 | Claude 8× naast Taillow → verse keurder (blind eerst, PASS/FAIL met pixels) → reparaties via maker | Claude, keurder, maker | keurder GOED |
| 6 | Jordi ziet alleen de sprite; zijn punten → kleine benoemde rondes | Jordi | "prima" |
| 7 | `af/<naam>.png` + `normal.pal`; SPEC, CHANGELOG, Stand van zaken, lessen | Claude | gepusht |
Frame 2, rug, icoon, shiny, naam, data: later, voor alle soorten samen.

**Blender (optioneel, Jordi: "geen vereiste") in de cloud, eenmalig per container:**
```
python3.11 -m pip install bpy scikit-image
apt-get install -y libegl1 libgl1-mesa-dri
```
Voorbeeldmodel: `docs/concept/sprites/kolibrie_pre/blender/kolibrie_pre.py` (huid = smooth union van afstandsvelden, kleurvlakken per vlak, snavel/ogen/pootjes los; Workbench-render, 512 px = 8×, ortho 64 BU = spriteframe). Silhouet/vel: `kolibrie_pre/blender/A/maak.py`. Toonkaart: model met alle kleuren wit renderen, verkleinen, 4 tonen.

**Controlescript (elke ronde):** alpha-diff met het bevroren silhouet (0 of alleen in benoemde zones), open randen, losse pixels, clusters < 3 px, lijst gewijzigde pixels oud→nieuw. Voorbeeld: `kolibrie_pre/blender/A/kleur_r9/controle.py`.

**Potoo-lessen (5 nov, eerste poging afgebroken; overdracht `docs/concept/sprites/potoo/OVERDRACHT.md`):**
- Eerst een Pokémon-ontwerp, dan pas een silhouet ("we gaan niet een potoo namaken"). Wijkt het ontwerp af van het dier, dan eerst een 3D-model van de héle Pokémon.
- 3D = meten, niet verzinnen: oriëntatiepunten uit de foto's, render op de foto-hoeken mét de foto-omtrek erover + 4 andere hoeken.
- Snavel/bek nooit uit bollen ("je maakt er een lipschijf van"): omtrek punt voor punt overtrekken, zelf letten op punten en golving.
- Nooit een rommelig tussenresultaat sturen (voxelruis, losse pixels, mondkleur buiten de mond).
- Tweede potoo-gesprek (5 nov): ook een SDF-model met omtrek-fit op de foto faalde ("pacman zeehond", "stop met blender"). Een open snavel uit formules (opengeknipte kop of losse onderdelen) leest niet als snavel; na 2 mislukte rondes niet doorpatchen maar Jordi om een andere aanpak/krabbel vragen. Alleen de foto's die Jordi in dat gesprek stuurt zijn de bron.

**Opdracht aan een agent bevat altijd:** `SPRITE_KERN.md`, SPEC-pad, bevroren delen + toegestane zones, Jordi's woorden letterlijk, gewenste uitvoer (raster, png, pal, vel, NOTITIES met zwakke punten), "niet committen".

**Regional forms:** begin van de bestaande sprite van de soort; lessen (Uyuni-Silicobra, Salticonda) in `naslag/SPRITE_WERKWIJZE_oud.md`, "Regional forms".
**Silhouet naar sprite is niet 1 op 1** (Jordi, 5 nov, DJ Rotom): heeft een onderdeel in kleur meer ruimte nodig (gezicht, ogen), dan mag de sprite daar afwijken; in de sprite oplossen en de afwijking melden. **Vormen van een bestaande soort** (Rotom-vormen, regional forms): consistentie-analyse tegen alle bestaande vormen, zie naslag.
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
- Daarna (aparte taak): frame 2, rugsprite, icoon, shiny-palet (skins-regel), naam en data.

## Kosten en tempo (ter oriëntatie)
- Een maker- of keurderronde kost ±150–400k agenttokens; zuinig: één maker, één keurder, kleine vellen, geen parallelle experimenten.
- Commit en push na elke ronde (ook interne), zodat niets verloren gaat.
- **Rastervellen: elk label uniek** (hoek in de naam, niet alleen A1/B2): twee vellen met dezelfde letters gaven bij de nachtaap een verkeerde keuze (kop 65° i.p.v. 80°).
- **Tekeningen op het 3D-poppetje (maskers, manen) in bolcoördinaten rond het gezicht ontwerpen als bolkappen (punten binnen een hoek van een richting; lon/lat-cirkels knijpen bij de kruin samen tot een punt), spiegelsymmetrisch om het middenvlak**, en controleren door de kop recht van voren én van opzij te renderen. Niet in het beeldvlak 'rechttrekken' (Jordi: "kijk even goed vanuit een 3d model"); een vlakke projectie langs de kijkas gaf een kap die tot de kin liep (nachtaap fase 2).
- **Geen inham tussen kop en rug 'voor de leesbaarheid'**: een uitsparing van 2–3 px tussen kruin en rug leest op 1× als een gat (Jordi, nachtaap fase 2); de scheiding van kop en lijf komt in de kleurstap.
- **Patronen op het lijf in 3D ontwerpen en naar 64 px projecteren** (`silhouet/kene_projectie.py` bij de nachtaap): de maker volgt de geprojecteerde loop en maakt alleen dunne stukken dikker; een patroon dat in beeld wordt getekend klopt niet met de vorm (Jordi: "is het niet teveel naar ons perspectief gevormd?").
- **Retro nachtaap fase 2 (2–3 nov, 14 kleurrondes):** pose/silhouet gingen vlot (poppetje → silhouet in één dag); de meeste rondes zaten in het lijfpatroon (dunne lijntjes → meander → banden → in beeld getekend → 3D-projectie → tapse wiggen). Volgende keer: patroon eerst als 2–3 opties in 3D + 1×-preview aan Jordi, met de Game Freak-patroonregels (SPRITE_NORM) vóór de maker begint.
- **Krabbel van Jordi op een uitsnede uitlezen** door de uitsnede te matchen (schaal/offset) en de krabbelkleur per spritepixel te tellen; neem ook de pixels van de basis mee waarop hij tekende (nachtaap: 2 linkerpixels van de wig ten onrechte weggehaald).
- **Kleine, exact benoemde keurdersreparaties (pixeltabel) voert Claude zelf uit** met een assert op de oude waarde en een alpha-diff; dat scheelt een makerronde.
- **Nachtaap fase 3 (3 nov), pose:** het ellipsoïde-poppetje werkt voor gedrongen houdingen (olinguito, nachtaap fase 2), maar niet voor een dynamische pose met vier losse ledematen en een gebaar: elke snelle patch gaf een nieuwe zeester, stomp of klauw ("dit lijkt nergens op"). Stop na 2 mislukte renders en ga naar een echte bron (Jordi's krabbel als omtrek, een foto of een echte sprite als skelet). Bekijk elke render groot vóór je hem stuurt, en patch niet halsoverkop op losse opmerkingen tijdens het werk; verwerk ze samen in één doordachte ronde.
- **Handen (nachtaap fase 3):** een open sprite-hand = vingers **tegen elkaar** met alleen een omlijning ertussen, een kleine waaier en een korte duim (Mr. Mime, Machamp); gespreide vingers met gaten lezen als een gebroken hand. Keur zelf eerst een close-up én de eindvormmaat naast de referentie vóór je iets stuurt (Jordi: "waarom moet ik dit allemaal voorkauwen?"). In pop3d krijgen vingers die in hetzelfde vlak liggen geen lijn: geef ze om en om een eigen (LINED) groep.
- **Referentie van Jordi = die afbeelding** (nachtaap fase 3): stuurt Jordi een plaatje (Gen 1-Drowzee), gebruik dát en niet de sprite van dezelfde soort uit de repo; en zet nooit sprites op een referentievel zonder het kenmerk zelf te tellen/controleren op een close-up (Gholdengo als "vijf vingers").
- **Echt 3D-model in Blender (3 nov, nachtaap fase 3):** `pip install bpy` werkt in de cloud (Cycles op CPU; Workbench/EEVEE niet, geen EGL). Ellipsoïde-poppetjes gaven gokwerk (handen 'lachwekkend'); een Blender-model met vingers in kootjes (Skin + voxel-remesh) gaf meteen een leesbare hand. Romp als metaballs, met de wortels van ledematen/staart erin, + Laplace-glad = één geheel. Valkuilen: `transform_apply` vóór join (anders remesh in lokale schaal), modifiers apart toepassen, een los object rendert wit (check of alles in `delen` zit). Zuinig: per ronde één render bekijken, Jordi draait zelf in Blender, keurder alleen bij de mijlpaal.
- **Blender: kleine wijzigingen direct op de .blend (5 nov, Jordi: "waarom maak je niet telkens kleine wijzigingen?"):** `blender/pas_aan.py` opent `muriqui.blend`, wisselt kleuren/schaalt objecten en rendert in ±12 s (was ±7 min door alles te herbouwen met `muriqui.py`). `muriqui.py` alleen voor vormwijzigingen die de huid raken; vormvragen eerst met Jordi beslissen; feedback bundelen. Nooit commentaar inline in een dict-regel invoegen via replace (slokte twee keer code op).
- **Model maken voor een sprite (nachtaap fase 3, 5 nov):** controleer het model altijd verkleind naar 64 px (`model2d/model_64.png`); bij ±0,12× wordt een oog van 5 render-px 1 px en verdwijnt. Kop 1,3× in het model (Pokémon-verhouding) en gezichtsdelen ≥ 2 px op 64. Maar stuur niet alleen op maat: grote ronde ogen + twee neusgatblokken gaven meteen knikkerogen en een varkensneus; leg het gezicht na elke maatreparatie weer naast de foto. Kleine 2D-reparaties op een render (kop, voeten) gaan sneller buiten Blender (`overschilder.py`, ±1 min per run).
- **2D-overschildering op een render (nachtaap fase 3, 5 nov):** eigen schaduw (bol) naast render-schaduw geeft naden ("dat is toch niet net afgewerkt"); trek de doorsnede van de render zelf langs het nieuwe deel en vloei over in een lang verloop, gum de oude omlijning precies weg en teken de nieuwe alleen waar het deel aan lege ruimte grenst. En: de bovenste voet ging drie keer mis (bokshandschoen → bol → hand in omgekeerd perspectief) door te gokken; na twee missers stoppen en Jordi om een referentie vragen (Checklist punt "Gokken is verboden").
- **Strepen/banden op een lijf (nachtaap fase 3, 5 nov):** niet als losse rechte streepjes in beeld zetten ("willekeurige krassen"); kijk eerst naar echte sprites (fase 2, Furret, Dusclops): gelijke brede banden die evenwijdig als boog om het lijf krommen, met strakke randen. En: een patroon pas ontwerpen als het lijf af is (Jordi: "anders moet dat weer opnieuw").
- **Volg het model per pixel bij reparaties (nachtaap fase 3, 5 nov):** makers gingen de vuistarm per ronde "verbeteren" en dreven af van het model (bol → lomp streepje; Jordi: "waarom volg je het model niet?"). Leg bij elke vormreparatie eerst de helderheid/omtrek van het model per 64-pixel naast de sprite (tabel per rij) en neem breedte, verloop en lichtkant daaruit over; verander maar één ding tegelijk (spleet wél, dikte níet).
- **Eén shading-ronde over het hele dier na losse vormreparaties (nachtaap fase 3, 5 nov):** na veel rondes per onderdeel had elk deel zijn eigen lichtverdeling (en de vuistarm had zijn omlijning omgekeerd: licht onder, zwart boven). Na vormwerk altijd één ronde "alles één geheel": één lichtbron uit het model, per deel controleren of de gekleurde rand aan de lichtkant en zwart aan de schaduwkant staat; cilinder onder ±45°: lichtband schuift van boven naar links/midden naarmate hij steiler wordt.
- **Referentie van Jordi opnieuw gemist (nachtaap fase 3, 5 nov):** de Sugimori-Drowzee stond sinds 3 nov in de SPEC, maar ik pakte de repo-Drowzee ("nee ik bedoel niet die drowzee"). Lees vóór elk onderdeel de referentieregel in de SPEC opnieuw. En: voor dunne delen (handen) een echte Gen 3-sprite van dezelfde maat als opbouw nemen (Mr. Mime: vingers 2 px, middentoon-lijn, toppen op verschillende hoogte) en de vorm van Jordi's referentie; niet met formules/inkepingen gokken ("een stap vooruit en dan weer een stap achteruit").
- **Niet elke kleine stap naar Jordi (nachtaap fase 3, 5 nov):** "ga maar eerst even samen met een agent in gesprek voordat je elke minimale stap terug weer aan mij laat zien en kom met meerdere opties, en echt goede opties". Bij een onderdeel dat niet lukt: maker maakt 3–4 echt verschillende opties, Claude keurt ze (met de maker in gesprek, één verbeterronde), en pas daarna 2–3 goede opties naar Jordi.
- **Retro healerhand nachtaap fase 3 (5 nov, Jordi gaf het op):** ±15 handrondes (3D, Machamp-plak, Drowzee-repo, waaier, opties) zonder dat er een echte hand uit kwam. Oorzaken: (1) de hand kreeg in model én silhouet een te klein vak (13×13 onder de kin) en dat is nooit eerder als verhoudingsprobleem benoemd; (2) referentie van Jordi te laat/verkeerd gebruikt; (3) per opmerking een kleine patch i.p.v. eerst opties. Volgende keer: bij een gebaar dat het ontwerp draagt (hand, oog) al in de modelfase op 64 px toetsen of het vak groot genoeg is voor de vorm (vijf vingers ≈ 14×16 px), en anders het model aanpassen vóór het silhouet.
- **"Grote rustige vlakken" ≠ één plat vlak (nachtaap fase 3, 5 nov):** na "geen losse onderdelen" schoot de shading door naar één licht vlak over been + rug + borst; Jordi: "een lichaam is niet bepaald 1 vlak ... een staart groeit nooit volledig egaal ergens uit". Lijf = meerdere massa's (borstkas, buik, bekken, dijwortel) met elk een ronding en zachte plooien in de schaduwtint op de overgangen; staart met een eigen aanzet. En: bij "het steekt eruit" eerst vragen of het om omtrek of shading gaat (hier shading).
- **Plooien en massa's (maker nachtaap fase 3, ronde 7):** een "steekt eruit"-been kan puur shading zijn (lichtgrens van been loopt recht door in die van het lijf: breek die grens); een plooi begint in een inham van de omtrek en loopt in 3–5 px dood in de basistint; een losse lichtvlek midden op een massa leest als vlek; bekijk uitsneden ≤ 800 px breed (anders verkleind en zie je 1-px-plooien niet).
- **Volume meten (maker nachtaap fase 3, ronde 7b):** een massa lees je aan een schaduwband van 2 px onder de kern (1-px-lijnen in 3 lezen op 3× als krassen); 2 alleen in het diepste punt van een plooi die aan de omtrek begint (losse 2 = scheur); meet egale vlakken met een rechthoekzoeker (grootste egale rechthoek), niet met een telling van samenhangende pixels.
- **Geen sterkte-varianten als "opties" (5 nov):** "matig" en "sterk" van dezelfde ingreep zijn geen keuze ("matige en sterke hallucinaties?"); opties moeten echt verschillende oplossingen zijn. Staartwortel: geen lijn of kraag, de staartshading loopt door op het lijf (Jordi: "de staart lijkt nu net opgeplakt").
- **Banden op een lijf dat deels bedekt is (maker nachtaap fase 3, rugpatroon ronde 3):** bedekt een ledemaat de ruggengraat, laat de banden dan vanaf de rand van wat ervoor ligt over de hele hoogte doorlopen (taps vanuit het midden leest als krassen); een eigen lichte bandtint op 5/4 + eigen schaduwtint op 3 houdt de lichaamsshading leesbaar; ringen > 4 px in licht zilver lezen op een kleine romp als verband.
- **Retro nachtaap fase 3 (3–5 nov, beta zonder rugpatroon):** het duurde lang door (1) een model met te klein vak voor de hand en een been dat te hoog aansloot (pas in de kleur opgelost), (2) patchen per opmerking i.p.v. eerst opties, (3) makers die vormen gingen "verbeteren" i.p.v. het model per pixel te volgen, (4) shading die van "losse delen" doorschoot naar "één vlak". Wat wél werkte: Jordi's krabbels (arm, poten), stapjes-varianten om uit te kiezen (been +3…+11, arm 25/50/75%), en verhoudingen eerst met echte sprites (ook back sprites) vergelijken. Patronen: zonder krabbel van Jordi drie keer mis; vraag er de volgende keer meteen om. En: "afronden" betekent goed afmaken, nooit zelf een onderdeel schrappen (Jordi: "afronden betekent niet half werk").
- Krabbel van Jordi = richting, geen overtrek: haal er vorm, aantal en plek uit, en bouw het patroon uit één vaste vorm die je herhaalt (gelijke vorm/afstand); supersample-maskers geven ongelijke rijbreedtes en "chevrons" (sin-boog) — cirkelboog of handgemaakte rijtabel werkt beter.
- Bandtint op lichte vacht: het grijsblauw (14) ligt te dicht bij de lichte vachttint (5) en valt weg; zet de band één stap lichter dan wat eronder ligt, of gebruik een vaste rijopbouw licht-midden-schaduw.
- Toon Jordi geen opties die een regel breken om het rijtje te vullen (B: het verre oog even groot als het nabije). Jordi: "stop aub met dingen als B voorstellen, dat kan echt niet". Liever twee goede opties dan vier waarvan er twee fout zijn.
- **Nederlandse dubbelzinnigheid in feedback (potoo, 5 nov):** "het is geen bol hoofd" = de kop is niet bol genoeg (klacht), niet "maak hem niet bol". Bij twijfel Jordi's zin terugvertalen naar een concrete actie en die eerst kort checken; ronde 4 maakte de kop daardoor juist platter.
- **Blinde test zonder verklappende bestandsnaam:** kopieer het plaatje eerst naar de scratchpad met een neutrale naam (bijv. `test_a.png`); een pad met "potoo" erin verklapt het antwoord (potoo, 5 nov).
- **Alleen veranderen wat Jordi noemt (potoo, 6 nov: "pas gvd alleen dingen aan die je aan moet passen").** Zodra Jordi een draft goed vindt, bouw je voort op díe versie en pas je alleen zijn punten aan. Extra reparaties van de keurder leg je eerst aan hem voor; nooit stilletjes meenemen (ronde 17 veranderde de muil rechts en maakte van zijn snavelpunt een lijn). Zijn geschetste omtrek is bindend: "korter/kleiner" betekent binnen die vorm kleiner kleuren, niet de vorm weggooien. Controleer met een pixeldiff dat buiten de genoemde plekken niets veranderd is, en meld die diff.
- **Geen tak in de sprite = geen takstap in de omtrek**; "stil zitten" komt uit kleur, klauwen en houding (potoo, 6 nov).
- **Vormvarianten in vlakke kleuren altijd labelen als "alleen vorm, kleurwerk blijft"**, anders denkt Jordi dat het kleurwerk weg is.
