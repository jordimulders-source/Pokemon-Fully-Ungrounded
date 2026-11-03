# Sprite-werkwijze: zo maken we elke nieuwe Pokémon-sprite

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
- **Slanke dieren op de achterpoten: het poppetje in lama-stijl** (`docs/concept/sprites/wasbeer/ontwerp/pop3d_v2.py`, wasbeer 3 nov: pose in 4 rondes goedgekeurd, na 3 mislukte rondes met het oude poppetje: "veel te dikke reet"). Lijf als één doorlopende getaperde buis (geen losse heup-/dijbollen), dijen slank, kop ±33% van de hoogte; ingekleurd en omlijnd, met per cel een 1x-voorbeeld, naast de foto's en 2 echte sprites (houding en beenlengte). Elke Jordi-opmerking wordt een knop in het script (romphoek, lijfdikte, stap, crouch, armstand) en een nieuwe rij varianten, zodat hij kiest in plaats van beschrijft.
- **Poten nooit in dezelfde stand** (Jordi: "dit is niet hoe dieren/mensen bewegen met poten precies in dezelfde pose"): één been geplant, het andere duidelijk anders (stap, op de tenen).
- **Een Gen 3-sprite als skelet + eigen buizen = verzonnen vormen** (wasbeer ronde 4–6, 2 nov): houding goed, maar het dier werd een fret (rechte rug, wigkop, stompjes). Neem de vormen altijd van een foto; een skeletsprite alleen voor de houding, en vergelijk elke ronde zelf eerlijk met alle foto's vóór Jordi.
- **Geen collage en geen scriptkleuring** (wasbeer, 2 nov: "erbarmelijk slecht", "helemaal geen pokemon sprite"): een romp uit een bestaande sprite knippen en er buizen en pixelsjablonen aan plakken, en dan per script inkleuren, geeft blokken en vlakken zonder samenhang. Elke opmerking van Jordi los repareren maakt het erger. Het silhouet wordt als één geheel getekend (bron overtrekken of een maker-agent met de hand), kleur altijd met de hand na een Game Freak-studie. Na ±5 rondes zonder voortgang: stoppen, de stand eerlijk benoemen en terug naar de werkwijze.
- **Vogels/vliegers en dieren met een simpele bouw:** een foto in de juiste pose is genoeg (kolibrie).
- Zijaanzicht mag als het bij het dier past (Swellow, Relicanth, Seviper, Skarmory).
- **Lastig klein onderdeel (klauw, gereedschap, oor): los in 3D tekenen, in 3 standen** (recht van voren, driekwart, opzij), en Jordi laten kiezen vóór het in de sprite gaat (wasbeer: de koevoetklauw kostte 12 silhouetrondes met beschrijvingen; de losse 3D-klauw was in 1 ronde "prima, driekwart in de sprite"). Opzij gezien vallen 2 klauwen achter elkaar en is elke inkeping onzichtbaar: kies een stand waarin het kenmerk in het silhouet staat.
- **Gokken is verboden:** is een kenmerk twee keer mis (kolibrievleugels), vraag Jordi om een referentie of een krabbel. Zijn krabbels over het silhouet gaven per stuk de meeste vooruitgang.

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
- Daarna (aparte taak): frame 2, rugsprite, icoon, shiny-palet (skins-regel), naam en data.

## Kosten en tempo (ter oriëntatie)
- Een maker- of keurderronde kost ±150–400k agenttokens; zuinig: één maker, één keurder, kleine vellen, geen parallelle experimenten.
- Commit en push na elke ronde (ook interne), zodat niets verloren gaat.
- **Gemeten (Coathief, 25 okt, uit de sessielogs `~/.claude/projects/.../*.jsonl`):** hoofdsessie ±0,4M output + 0,75M nieuwe input; één maker-agent over 13 rondes ±0,57M output + 3,6M nieuwe input (76M cache-reads, doordat zijn context bleef groeien); 4 keurders samen ±0,3M output + 0,8M nieuwe input. De 6 voorpootrondes zonder raster waren het duurste deel. Zuiniger: overtrekvel vanaf de eerste vormreparatie, kleine pixelreparaties (< 15 px) door Claude zelf, en een maker die erg lang doorloopt na ±8 rondes vers starten met SPEC + NOTITIES.
- Oudere sprites (olinguito, kolibrie) hebben geen logs meer in de container; alleen schattingen in `RETRO_KOLIBRIE.md` en `SPRITE_REVIEW.md`. Noteer daarom voortaan de gemeten kosten per sprite in zijn SPEC.md.
