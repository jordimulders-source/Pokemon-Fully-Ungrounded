# Sprite-werkwijze: zo maken we elke nieuwe Pokémon-sprite

> **Kort: lees eerst `docs/lessen/SPRITE_KERN.md`.** Dit bestand is naslag.

**Vastgesteld door Jordi (25 okt):** "ik denk dat we de beste methode hebben gevonden om sprites te maken. Jouw way of working mag je vast leggen als de manier, uitgebreid en stap voor stap, zodat alle nieuwe gesprekken vanaf nu het zo oppakken."

Bewezen op de **kolibrie** (Ghost/Flying, eindvorm: van eerste schets tot goedgekeurde sprite in ±1 dag) en de **olinguito v2** (Dark-starter, fase 1: na 30+ mislukte rondes in de oude aanpak, nu in 5 silhouet- en 4 kleurrondes "het beste olinguito-ontwerp wat ik tot nu toe heb gezien"). Achtergrond: `RETRO_KOLIBRIE.md`, `RETRO_OLINGUITO.md`. Deze werkwijze vervangt stap 1–5 bovenaan `FAKEMON_DESIGN.md` waar ze verschillen.

## Verplicht (Jordi, 2 nov, na de wasbeer)
- **Coathief is het voorbeeld.** Claude tekent zelf geen silhouetten of kleuren: geen buizen/ellipsen, geen geknipte stukken van bestaande sprites, geen scriptkleuring. Claude maakt de bron klaar (foto's, poppetje, SPEC), de **maker-agent** tekent met de hand, Claude controleert tegen de bronfoto's, een keurder keurt, dan pas Jordi.
- Elke opmerking van Jordi gaat met zijn letterlijke woorden naar de maker; nooit één punt los repareren zonder het geheel naast de bron te leggen.
- Twee rondes zonder voortgang = stoppen en de stap terug benoemen.
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
- **Ontwerpfase met het poppetje als praatplaat werkt uitstekend (lama, 2 nov; Jordi: "ik vind dit echt geweldig werk [...] noteer dat deze manier van werken tot nu toe uitstekend werkt").** Van idee tot goedgekeurd ontwerp van fase 2 én 3 in 5 korte rondes, zonder één pixel:
  1. Jordi's foto's meteen in `referenties/`, zijn woorden letterlijk in SPEC.md.
  2. Poppetje (`lama/ontwerp/pop3d_lama.py`, op basis van het Coathief-poppetje) in de hoek van Jordi's posefoto, **mét kleding en kenmerken**, gekleurd: Jordi wil het ontwerp "vooral ook in design zien".
  3. Eén vel met een klein raster van keuzes die er echt toe doen (verhouding A/B/C met het kop-% erbij, vachtkleuren), naast de foto en de vorige fase; één aanbeveling van Claude.
  4. **Hele lijn op schaal naast elkaar** (fase 1 sprite + fase 2 + fase 3, hoogte naar het D1-formaat), zodat Jordi de evolutie beoordeelt, niet één losse vorm.
  5. Onderscheid tussen fasen maken via **silhouet: bouw + pose** (slungelige tiener in dekking ↔ zware, gewortelde kampioen); gezicht en kleur volgen in de kleurronde. Leitmotif (halsband) door de hele lijn.
  6. Elke ronde: SPEC + changelog + commit/push; het vel via SendUserFile. Daarna de bron voor het silhouet (`fase2/silhouet/bron.py`: goedgekeurd poppetje direct verkleind) en pas dan de maker-agent.
- **Het poppetje faalt bij slanke dieren op de achterpoten** (wasbeer, 2 nov: 3 rondes, "veel te dikke reet", pose niet zoals de foto): overlappende ellipsoïden van heup en dijen maken de achterkant te dik en een staande houding wordt een ton. Heeft Jordi een foto van de pose: **trek die direct over** (kolibriemethode) en stop na 2 mislukte poppetjerondes. Vraag foto's als bestand; foto's die alleen in de chat staan kunnen niet als onderlaag dienen.
- **Slanke dieren op de achterpoten: het poppetje in lama-stijl** (`docs/concept/sprites/wasbeer/ontwerp/pop3d_v2.py`, wasbeer 3 nov: pose in 4 rondes goedgekeurd, na 3 mislukte rondes met het oude poppetje: "veel te dikke reet"). Lijf als één doorlopende getaperde buis (geen losse heup-/dijbollen), dijen slank, kop ±33% van de hoogte; ingekleurd en omlijnd, met per cel een 1x-voorbeeld, naast de foto's en 2 echte sprites (houding en beenlengte). Elke Jordi-opmerking wordt een knop in het script (romphoek, lijfdikte, stap, crouch, armstand) en een nieuwe rij varianten, zodat hij kiest in plaats van beschrijft.
- **Poten nooit in dezelfde stand** (Jordi: "dit is niet hoe dieren/mensen bewegen met poten precies in dezelfde pose"): één been geplant, het andere duidelijk anders (stap, op de tenen).
- **Een Gen 3-sprite als skelet + eigen buizen = verzonnen vormen** (wasbeer ronde 4–6, 2 nov): houding goed, maar het dier werd een fret (rechte rug, wigkop, stompjes). Neem de vormen altijd van een foto; een skeletsprite alleen voor de houding, en vergelijk elke ronde zelf eerlijk met alle foto's vóór Jordi.
- **Geen collage en geen scriptkleuring** (wasbeer, 2 nov: "erbarmelijk slecht", "helemaal geen pokemon sprite"): een romp uit een bestaande sprite knippen en er buizen en pixelsjablonen aan plakken, en dan per script inkleuren, geeft blokken en vlakken zonder samenhang. Elke opmerking van Jordi los repareren maakt het erger. Het silhouet wordt als één geheel getekend (bron overtrekken of een maker-agent met de hand), kleur altijd met de hand na een Game Freak-studie. Na ±5 rondes zonder voortgang: stoppen, de stand eerlijk benoemen en terug naar de werkwijze.
- **Vogels/vliegers en dieren met een simpele bouw:** een foto in de juiste pose is genoeg (kolibrie).
- Zijaanzicht mag als het bij het dier past (Swellow, Relicanth, Seviper, Skarmory).
- **Lastig klein onderdeel (klauw, gereedschap, oor): los in 3D tekenen, in 3 standen** (recht van voren, driekwart, opzij), en Jordi laten kiezen vóór het in de sprite gaat (wasbeer: de koevoetklauw kostte 12 silhouetrondes met beschrijvingen; de losse 3D-klauw was in 1 ronde "prima, driekwart in de sprite"). Opzij gezien vallen 2 klauwen achter elkaar en is elke inkeping onzichtbaar: kies een stand waarin het kenmerk in het silhouet staat.
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
- **Na het verkleinen nalopen wat de render belangrijk maakt:** neusknop, lucht in een staarthaak, de inkeping van een klauw. Die sneuvelen bij het verkleinen (wasbeer: neus werd een uitsteeksel van 1 px, "een raar uit stekend streepje"; de haak werd een knots) en horen hier met de hand hersteld te worden; in de kleurronde is het te laat en kost het een silhouetwijziging achteraf.
- **Minimale dikten:** snavel/dunne delen ≥ 2 px, poten ≥ 5–6 px, geen spleten van 1 px tussen poten die naast elkaar staan.
- **Leesbaarheid:** toets of de ruimte direct onder de buik leeg is (hangende slierten lazen als poten/mug); vier poten in vier kolommen; de kop een eigen onderdeel.
- **Formaat volgt de vorm:** het formaatdoel mag nooit winnen (olinguito werd dun door het doel van 950 px; 1100–1200 px is prima, zoals Linoone/Zigzagoon). Een eindvorm kan klein zijn als hij slank is (kolibrie ±1000 px, gelijk aan Crobat).
- **Vel voor Jordi:** onderlaag/foto | silhouet 4× | silhouet over de onderlaag | silhouet 1×, naast 3–5 echte Gen 3-silhouetten van hetzelfde bouwtype. Claude keurt eerst zelf op **pose én massa** (overlay), dan pas Jordi.
- **Goedgekeurd silhouet = bevroren** (alpha-diff 0 in alle volgende rondes). Vastleggen in SPEC.md.
- **Maar: silhouet naar sprite is niet 1 op 1** (Jordi, 5 nov, DJ Rotom): heeft een onderdeel in kleur meer ruimte nodig (gezicht, ogen), dan mag de sprite daar van het silhouet afwijken; geen nieuwe silhouetronde voor Jordi, gewoon in de sprite oplossen en de afwijking melden.

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
   - **Ook advies dat een harde eis van Jordi raakt** (wasbeer, 2 nov: de keurder liet de gespleten koevoetpunt dichtmaken tot een 3x3-blok, Jordi: "linkerklauw mist de hele koevoetvorm nu opeens"; "er gaat wel veel mis telkens"). Leg elk reparatieadvies vóór het naar de maker gaat naast Jordi's woorden in SPEC.md; strijdig = niet uitvoeren, en een kenmerk dat Jordi eist mag in geen enkele ronde verdwijnen (Claude toetst dat zelf op 8x en 1x vóór Jordi).
4. Pas als het door 1 en 2 komt: naar Jordi, met een vel en een korte lijst keuzes.

- **Vormen van een bestaande soort (Rotom-vormen, regional forms):** laat een agent een systematische consistentie-analyse doen tegen alle bestaande vormen (palet-waarden, binnenlijn, spits, tanden, hooglicht-%, maat), met een script gemeten. Dat vond bij DJ Rotom vijf afwijkingen die geen gewone keuring zag (Jordi, 5 nov: "dat die klopt met de andere sprites is het belangrijkste"). Let op kleuren die in de shiny meeveranderen (equalizer deelde de gloedindex).

## Stap 5. Reparatierondes
- Alleen wat Jordi of de keurder noemt; benoemde zones, pixelbudget, diff-bewijs buiten de zones.
- **Kleine reparaties zijn klein**: Jordi vond olinguito ronde 3 al "het beste"; ronde 4 was 53 px.
- Wat Jordi goedkeurt wordt bevroren in SPEC.md; afkeuringen gaan onder "Afgekeurd".
- **Overtrekvel met pixelraster** (Coathief, 25 okt; Jordi: "zo met een pixelraster werkt goed voor dit soort aanpassingen"): bij vormreparaties de onderlaag en de sprite naast elkaar op hetzelfde 64-raster met spritecoördinaten (`docs/concept/sprites/coathief/kleur/ronde8/overtrekvel.py`). De maker trekt cel voor cel over en markeert elke afwijking met reden; Jordi tekent cellen af op het vel. Stuur het vel bij elke vormronde mee. Losse krabbellijnen op een 8×-uitsnede gaven 6 rondes drift (de sprite week telkens "net teveel" af van de onderlaag); het raster loste het in 1–2 rondes op.
- **Kleur volgt de onderdelen van de onderlaag:** lees per pixel af welk onderdeel het in de render is (nabije poot, verre poot, vacht, klauw; `coathief/silhouet/labels_voorpoten.py`). Een kloppend silhouet met een verkeerde kleurindeling las als "weer hetzelfde" (Coathief ronde 6).
- **Krabbels van Jordi terugrekenen:** schaal meten aan een bekend kenmerk (het oog), dan per cel aflezen; zijn lijn is een indicatie, de onderlaag is de maatstaf.

## Review wasbeer (2–3 nov): wat goed en slecht ging
Twee sessies, ±12 silhouetrondes op de klauw, 3 ontwerprondes, 11 kleurrondes, 6 keuringen; frontsprite af ("nee ik ben tevreden zo").

**Goed (houden):**
- 3D-poppetje met varianten en 1x-voorbeelden naast foto's en echte sprites: Jordi koos pose en verhoudingen in 4 rondes (P13 → E → E2 → S1a) zonder zelf te hoeven tekenen.
- Silhouet direct van de render met exact hetzelfde kader (controle: oud model opnieuw renderen = 0 px verschil), zodat alleen de gewijzigde zone verandert.
- Keuren in de vaste volgorde Claude → keurder → (verse) eindkeurder → Jordi; de verse eindkeurder vond nog fouten die geen eerdere keuring zag (dubbele zwarte rand, open oorvoet).
- Advies van de keurder eerst naast Jordi's woorden leggen; smaakvragen bundelen en in één bericht voorleggen (temperatuur, pupil, neus, wenkbrauw, mond); bij een twijfelkeuze 2 versies laten maken (9 en 9b).
- Een verse maker starten toen de oude ±380k context had: in één ronde netter werk dan de oude in drie.
- Warmer palet en meer contrast (ronde 4) gaven de grootste sprong in kleur; pixelreparaties in hetzelfde grijs hielpen weinig.

**Slecht (niet herhalen):**
- Een kenmerk beschrijven in woorden ("koevoet", "kleine inkeping") en de maker laten verzinnen: elke ronde een andere vorm, 12 rondes en een gefrustreerde Jordi ("JE SNAPT ER NIKS VAN", "ik word hier echt moe van"). Oplossing achteraf: een echte bron (Sneasel-klauw, de 3D-klauw) pixel voor pixel en alleen wijzigen wat Jordi aanwijst.
- Jordi's schets of foto niet letterlijk volgen, of een uitleg die al gegeven was opnieuw interpreteren ("je gokt maar"). Bij een schets: eerst zelf bekijken en per cel beschrijven wat weg/erbij gaat, dan pas laten uitvoeren.
- Keurdersadvies doorsturen dat een eis van Jordi brak (koevoetpunt dichtgemaakt tot een blok).
- Vorm "verbeteren" die Jordi al goed vond (Sneasel-vorm omgegooid): "niet elke keer die vorm omgooien".
- Dunne delen pas in de kleur willen redden (neus, staarthaak), terwijl het silhouet al bevroren was.
- Nog een reparatieronde draaien op een palet dat het probleem was (dof grijs): eerst de grote keuzes (temperatuur, contrast) aan Jordi voorleggen, dan pixels.

**Regels die hieruit volgen** (staan ook in de stappen hierboven):
1. Elk kenmerk uit een echte bron (foto, 3D-render, bestaande spriteklauw), nooit uit een beschrijving.
2. Lukt een klein onderdeel niet na 2 rondes: stoppen, het los in 3D tekenen of een tekenvel met raster sturen (`wasbeer/silhouet_v2/tekenvel_klauw.py`) en Jordi laten aanwijzen.
3. Wat Jordi goed noemt is bevroren, ook in de rondes daarna; een maker mag het niet "netter" maken.
4. Grote keuzes (pose, palet, contrast) vóór kleine reparaties.
5. Na ±250–300k context een verse maker met SPEC + NOTITIES + de laatste rijen-file.

## Stap 6. Afronden
- Eindversie in `docs/concept/sprites/<naam>/af/` + vel; SPEC.md, `CHANGELOG.md`, Stand van zaken in `CLAUDE.md` bijwerken; lessen naar het passende `docs/lessen/`-bestand.
- Daarna pas in een **latere fase voor alle soorten samen** (Jordi, 5 nov: "we bouwen eerst designs met sprites"): frame 2, rugsprite, icoon, shiny-palet (skins-regel), naam en data (incl. y-offset).

## Kosten en tempo (ter oriëntatie)
- Een maker- of keurderronde kost ±150–400k agenttokens; zuinig: één maker, één keurder, kleine vellen, geen parallelle experimenten.
- Commit en push na elke ronde (ook interne), zodat niets verloren gaat.
- **Gemeten (Coathief, 25 okt, uit de sessielogs `~/.claude/projects/.../*.jsonl`):** hoofdsessie ±0,4M output + 0,75M nieuwe input; één maker-agent over 13 rondes ±0,57M output + 3,6M nieuwe input (76M cache-reads, doordat zijn context bleef groeien); 4 keurders samen ±0,3M output + 0,8M nieuwe input. De 6 voorpootrondes zonder raster waren het duurste deel. Zuiniger: overtrekvel vanaf de eerste vormreparatie, kleine pixelreparaties (< 15 px) door Claude zelf, en een maker die erg lang doorloopt na ±8 rondes vers starten met SPEC + NOTITIES.
- Oudere sprites (olinguito, kolibrie) hebben geen logs meer in de container; alleen schattingen in `RETRO_KOLIBRIE.md` en `SPRITE_REVIEW.md`. Noteer daarom voortaan de gemeten kosten per sprite in zijn SPEC.md.

## Lessen lama fase 2 (2–3 nov)
- **Keur het poppetje kenmerk-voor-kenmerk naast de echte foto** (vooral de kop) vóór Jordi: de paardenkop van het poppetje glipte door en kostte ±10 rondes sprite (Jordi: "toch net wat meer een paard dan een lama").
- **Pose per dier uit het echte gedrag + Gen 3-posestudie** (`lama/fase2/posestudie/`): een lama staat horizontaal met de kop driekwart naar je toe (Manectric/Rapidash/Umbreon); "poten omhoog" is bij een lama gek, een opgetilde/geknikte poot leest als "gebroken".
- **Korrel tellen:** wolomtrek met een script nalopen op 1-px-bobbels/inkepingen (`lama/fase2/silhouet_r3/korrel.py`); Game Freak-wol (Mareep/Flaaffy) is bijna glad met 2–3 grote bogen.
- **Kleur nooit met tintwissel-scripts per zone**: gaf horizontale banden/stempelschulpen (de keurder vond het in 2b).
- **Oog:** droog = rechte lidlijn, pupil tegen het lid, licht laag vóór; nooit een zwart rondje met een wit puntje (oogstudie `lama/fase2/oogstudie/`).
- **Verse maker na ±8–9 rondes** (context >400k) met SPEC + NOTITIES + keuring: werkte direct beter en goedkoper.
- **Echte bronfoto's controleren op de soort** (foto 6 bleek een alpaca).
- **Lama fase 2 (4 nov):** silhouet pas goed toen het hele 3D-model werd overgetrokken met een dekkingskaart (50 %-grens, max. ±1 px); daarvoor 6 rondes doorpatchen omdat Claude eigen vormeisen (eigen kolom per poot, ≥ 5 px) boven het model zette. Fluffy wol: overlappende ronde wolbollen met eigen schaduwboog (Mareep/Flaaffy), binnenkleuren eerst, omtrek pas daarna; geen gestapelde gelijke bollen (buis) en geen losse plukken (uitstulping). Eindkeuring vond nog 6 px (nagels tegen transparant, zwart aan de lichtkant).
- **Lama fase 3 (5 nov):** zegt Jordi dat iets "in de sprite niet goed" is terwijl silhouet en model zijn goedgekeurd, dan is het werk in de kleursprite; niet terug naar poppetje of bron ("je luistert niet", "dit is nutteloos werk").
- **Lama fase 3 (5 nov):** een schuine mondlijn die naar achteren omhoog loopt leest als een (domme) lach; een neutrale lamablik = korte rechte/licht dalende mondlijn, hangende onderlip, zwaar vlak lid. Een kop mag in de sprite groter dan het silhouet als accessoires (hoed, vlechten) anders niet passen (Jordi gaf daar al eerder toestemming voor; niet opnieuw vragen).
- **Lama fase 3 (5 nov):** ook in de kleurronde de kop overtrekken van het model (bemonsterde kleur + labels + lijnen per spritepixel op een raster, `lama/fase3/kleur/kopbron/bron_kop.py`), niet laten hertekenen: een maker die de kop "naar het model" tekent verzint toch eigen snuit/oog/vlecht ("nu ben je gewoon weer dingen aan het verzinnen"). Opschalen = het model uniform schalen.
- **Lama fase 3 (5 nov):** kleur van een onderdeel nooit veranderen om een ander onderdeel te scheiden (vlechten werden bruin voor het oog; Jordi: "waarom zijn de vlechten opeens bruin?"); scheiden met 1 px tussenkleur. Een donker lidvlak met een vlakke lijn erboven leest als frons (boos); lui = licht lidvlak, lidlijn dalend naar buiten.
- **Lama fase 3 (5 nov):** is iets "bijna goed" (oog 5A: "best ok, maar nog wat bozer"), repareer dan met 1–3 px vanaf die versie; een heel nieuw recept (5A2) maakte het "veel slechter".
- **Lama fase 3 (5 nov, af):** wat werkte: (1) kopbron = model met alleen de kop uniform geschaald, cel voor cel overgetrokken (labels + lijnen + bemonsterde kleur op een raster); (2) daarna per Jordi-opmerking 1–50 px vanaf de vorige versie; (3) verse eindkeurder met een eigen sectie per poot; reparatielijst met huidige → nieuwe index, door Claude gecontroleerd en uitgevoerd. Wat niet werkte: poppetje/bron aanpassen voor een spriteprobleem, en een maker die een onderdeel "naar het model" hertekent.

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
- **Poppetje eerst passend op de foto, dan pas cute** (kolibrie pre-evo, 2 nov; Jordi: "waarom wijkt dit zo immens veel af van het silhouet?"): nooit een handsilhouet én een los poppetje naast elkaar. Volgorde foto → poppetje → silhouet. Meet de overlap van het poppetje met de foto-omtrek (`kolibrie_pre/pop3d/pas_foto.py`, zoekt de maten van lijf/kop/staart, ≥ 85%) en doe verhoudingswijzigingen (grotere kop, korter lijf) daarna in 3D, als raster van standen voor Jordi.
- **Poppetje moet ±100% op het goedgekeurde silhouet liggen** (kolibrie pre-evo, 2 nov; Jordi: "79% overlap is waarom het fout gaat"): ellipsoïden die op 79–88% passen geven een ei/pinguïn. Werkt wel: het goedgekeurde silhouet zelf **opblazen** tot 3D (hoogteveld = wortel van de afstand tot de rand, kop/vleugel eigen bolling, delen gekleurd en belicht): `kolibrie_pre/pop3d/opblazen.py`, 98–100% overlap.
- **Keurder nooit inperken tot "alleen afwerking"** (kolibrie pre-evo r5, 3 nov; Jordi: "dit is echt niet goed gekeurd, je volgt de instructies gewoon niet"): de eindkeurder toetst altijd ook of het op 6–8× naast Gen 3-sprites leest als sprite (binnenbelijning per onderdeel, oog, contrast), niet alleen de lijst van de vorige ronde. Reparaties van een keurder gaan via de maker en daarna opnieuw langs de keurder; Claude legt het resultaat zelf op 6–8× naast 2–3 echte sprites vóór Jordi. Een open punt "nog niet zo af als X" moet expliciet afgesloten zijn.

## Regional forms (Jordi, 3 nov)
- Een regional form begint van de bestaande sprite van de soort (aanpassen), niet vanaf een foto en een nieuw silhouet.
- **Bewezen op de Uyuni-Silicobra (3 nov, 6 rondes):** eerst ontwerpschetsen gescript óp de echte sprite (Jordi kon zich tekst niet voorstellen; een paletwissel is "niet genoeg"), studie van bestaande regional forms (kenmerk krijgt ander materiaal/functie, lijf en pose blijven), dan één maker die doorwerkt.
- Een nieuw kenmerk moet binnen het eigen silhouet passen: een zak die buiten de nek bolt raakte de staart of werd een aanhangsel; een band óm de nek loste het op.
- Bij onduidelijke feedback ("dat streepje", "een lijn") eerst navragen met een uitsnede waarin kandidaten omkaderd zijn (A/B), niet een variant gokken: de "kuiflijn"-test was een misverstand; Jordi bedoelde de gezichtslijn van het origineel.
- "Zoals het origineel" = dezelfde loop als de grens in de basis (overlay, per pixel de index); een grens tussen twee lichte vlakken leest pas als één kant zijn eigen kleur terugkrijgt.
- Gescripte schetsen: let op paletindexen die de basis voor twee onderdelen deelt (oogring = staartpunt; gezicht = buik), en laat gaten (staartkrul) transparant.
- Naden en barsten: begin bij Y-punten (drie naden, nooit een kruis), trapsgewijs 1 px naar de rand; rechte blokken lezen als baksteen/Rock. Een glanzende zak met facetten leest als edelsteen.
- Toevoegingen bovenop het silhouet (kuif) lopen aan de uiteinden taps uit tot de oude omtrek; anders steekt er een hoek uit of brokkelt het af.

- Gescripte schetsen werken alleen als kleine ingrepen op een eenvoudige sprite (Silicobra). Op een drukke sprite met een eigen patroon (Sandaconda) of voor een nieuwe vorm leveren ze lelijke rommel op (Jordi: "gruwelijk lelijke sprites"): dan niet sturen, maar eerst in woorden + referenties de vorm afspreken en daarna de silhouetronde.
- Een evolutie moet ook in de kop evolueren: dezelfde kop op een groter lijf leest niet als evolutie (Jordi, Salticonda). En ook een opgerolde slang staat 3/4 naar de kijker, niet in zijaanzicht.
- Claude stuurde Salticonda kleur2 door terwijl de eigen check drie zwakke punten noemde (oog, krokodillenkop, softijs); Jordi: "super lelijk". Regel opnieuw: zelfgenoemd zwak punt = niet sturen, ook niet "ter info". Een volledig nieuw ontwerp over een 3D-onderlaag gooide weg wat Jordi "al prima" vond: bouw verder op de laatste versie die Jordi goed vond, in kleine stappen.
- De kop van een evolutie staat in dezelfde 3/4-hoek als de pre-evolutie (neem die kop als skelet en laat hem groeien); een kop in profiel ("volledig horizontaal") is altijd fout, ook bij slangen.
- "Groter" betekent: dezelfde vorm in alle richtingen opschalen (vooral hoger), niet breder uitbouwen; en wat Jordi goed vindt (neus kleur3) niet "verbeteren" in dezelfde ronde. Ruimte bovenin? Schuif de sprite omlaag als er onderaan rijen vrij zijn.
