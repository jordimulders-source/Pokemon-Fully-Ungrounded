# The Spire – ontwerp (roguelike-faciliteit, Battle Frontier)

Stand: 3 okt 2026, gesprek Jordi + Claude. Dit document is de bron voor de volgende sessie.

**Beta (v0.8.103):** volledige run speelbaar via debugmenu > Utilities > The Spire: draft, act-kaart, kamers (gevecht, elite, rust, winkel, event, baas), relics, 3 acts met evolutie, pauzeren in de save. Code: `src/spire.c` (gevecht), `src/spire_run.c` (run, kaartgeneratie, kamers, relics), `src/spire_map.c` (kaart), `src/spire_cards.c` (kaartenschermen). Nog niet: ingang in de wereld, codex, intenties met patronen voor bazen, golven, echte event-teksten. Eerder: rekenscript (`tools/grounded/spire/`) en een prototypegevecht (debugmenu > Utilities > Spire prototype) met ×HP, DEFEND/blok en intenties; code in `src/spire.c`, constanten in `include/spire.h`. Nog niet: toren, kaart, drops, winkel, relics, RUN = pauzeren/opgeven, Spire-codex, act-overgang.

## Kernprincipes (Jordi, okt 2026)
- **Altijd een eerlijke winkans bij goed spel**, zoals in Slay the Spire: slordig spelen kost je meestal de run (tenzij je veel relic-geluk hebt), maar zelfs de zwaarste seed is te winnen. Daarom spelen pro's in Slay lange reeksen op A10/A20.
- **Elk gevecht is een puzzel**: verkeerd aangepakt een obstakel, goed aangepakt makkelijk. Vijanden beginnen zwak en krijgen per act meer gimmicks en kracht; passief spelen wordt steeds meer afgestraft.
- **Pokémon-kennis én Slay-kennis worden beloond** (types, abilities, look-alikes herkennen; patronen, tempo, kaartkeuzes).
- **Creatief, maar altijd grounded**: eerst kijken of er al een Pokémon-mechanic voor is (Ritual = Rage, opladen = Quiver Dance/Machine Learning/Acupressure, start-buff = totem-boost, Gremlin Nob = Defiant). Zoveel mogelijk binnen de Pokémon-wereld.
- **Altijd wiskundig onderbouwd**: elke keuze komt uit het rekenwerk (`SPIRE_BALANS.md`, gegenereerd door `tools/grounded/spire/spire_pool.py` en `encounters.py`). Breekt een voorstel de balans, dan meldt Claude dat meteen.
- **Alles is lv 100** (speler en vijanden); level is nooit een knop.
- Meer variatie dan Slay 1 en 2 mag: er zijn 1000+ Pokémon (al is een groot deel nutteloos voor deze modus).

## Concept
- Nieuwe, enorm hoge toren op het Battle Frontier-eiland: **The Spire**. Roguelike à la Slay the Spire.
- **3 acts**, per act verdiepingen met keuzes (gevecht, elite, winkel, rustplek, event) en een **baas**.
- Doel: snappy, methodisch, weinig RNG-pech; niet PokéRogue-achtig (geen tientallen one-shots).
- Zoveel mogelijk Pokémon-mechanics blijven overeind (crits blijven bestaan).

## Team
- **Rentals**, en je hebt er **altijd precies 2**. Je speelt **altijd doubles** (jij 2 Pokémon).
- Groot aantal Pokémon beschikbaar voor de speler; sommige zijn beter dan andere, dat is prima.
- Een nieuwe Pokémon (draft/event/shop) **vervangt** er één; de nieuwe komt met volle HP. Relics blijven.
- **Evolueren na act 1** (als de Pokémon dat kan).
- Flauwgevallen en toch gewonnen: doet het volgende gevecht weer mee met **1 HP**.
- **Switchen bestaat niet.**

## Tegenstanders
- **Geen trainers** (Jordi, v0.8.101): je vecht tegen losse Pokémon (wild dubbelgevecht met trainer-AI). Golven vragen nog engine-werk (wilde gevechten vullen niet aan).
- Intenties tonen **KO** (zeker dodelijk) of **KO?** (alleen met een hoge rol).
- 1 of meerdere tegenstanders: **2 tegen 1** (baas) kan, 2 tegen 2 ook. Meer dan 2 tegelijk kan de engine niet, wel **golven** (valt een lakei, dan komt de volgende uit de party).
- Bazen/lakeien: een **grote pool aan bazen** met vaste patronen (memoriseren zoals in Slay, maar meer variatie). Lakeien = zwakke support-Pokémon (weer, Tailwind, schermen, buffs).
- **Abilities van tegenstanders verborgen**; de ability-popup van expansion onthult ze. Idee: een **Spire-codex** (met R) die onthoudt wat je ooit zag (ability, moves, patroon).
- **Intenties**: de tegenstander legt zijn volgende move een beurt vooruit vast en toont die compact onder zijn levensbalk, bijv. `▶ EARTHQUAKE ⟷ beide ~38`, `▶ FLAMETHROWER → links ~65`, `▶ SWORDS DANCE  Atk^`. Pijl = doel (links/rechts/beide), getal = geschatte schade (bereik of max; crits kunnen erdoorheen). Iets liberaler met ruimte dan in normale gevechten mag.
- Kan de intentie niet doorgaan (doel flauw, Taunt, slaap, flinch, geen PP): gewone Pokémon-regels (ander doel / beurt kwijt).

## Gevechtsmenu
- **FIGHT / BAG / DEFEND / RUN**: het POKéMON-menu wordt **DEFEND**.
- **DEFEND**: kost de beurt van die Pokémon, gaat **altijd eerst** (prioriteit als Protect, +4), geeft **Blok** (getal dat deze beurt eerst wordt opgemaakt, vervalt aan het eind van de beurt).
  - Op **1 Pokémon** naar keuze, of **gespreid over beide** (elk iets meer dan de helft, voorstel 60%).
  - Hoeveelheid **schaalt met de verdediging** van de Pokémon die verdedigt (Def/Sp. Def) en **neemt per act toe**. Eerste schatting: ~15% van eigen max HP × verdedigingsfactor × act-factor (≈ één normale klap).
  - Blok werkt alleen tegen **directe schade van moves**, niet tegen brand/gif/weer/terugslag/Stealth Rock. Multi-hit eet het blok per klap op.
  - Beide Pokémon verdedigen: blokken tellen op.
- Andere verdedigende moves (Protect, Wide Guard, Follow Me, Reflect…) blijven zoals ze zijn.
- **BAG**: potions en battle items (X-items worden nuttig). Kopen in de winkel; aantal slots nog bepalen (Slay: 3).
- **RUN**: kiezen tussen **pauzeren** (run opslaan vanaf het begin van dit gevecht, eigen team terug, terug naar de overworld; later verder met dit gevecht) of **opgeven** (run eindigt, BP naar rato).
- Eigen ability/stats bekijken: L (of SELECT) opent de summary van je twee Pokémon.

## Moves als kaarten
- **4-movesprincipe blijft.**
- Elke rental begint met **startermoves** (zoals Strike/Defend in Slay).
- Na elk gevecht kies je een move uit een drop (zoals kaartbeloningen). **Elke Pokémon kan elke move leren** als hij hem in een drop krijgt. **STAB** blijft gelden.
- Moves gecategoriseerd zoals kaarten (aanval / skill / power), met **zeldzaamheid**: de echt goede moves zijn **rare drops**.
- **PP als kosten**: zeldzaam = sterk maar weinig PP. PP kan doorlopen over gevechten heen (bijv. Protect-achtige moves een paar keer per act, aangevuld op rustplekken).

## Relics, winkel, rust, events
- **Relics** = elite-drops, willekeurig uit een pool (run-brede effecten, simpele haken in de gevechtscode).
- **Winkel**: zelf kiezen welke moves, relics, een **ability** kopen, potions/items.
- **Rustplek**: helen, of een move verbeteren, of (vanaf act 1) evolueren.
- **Events**: tekstkeuzes met risico/beloning (Jordi's humor); ook kans op een andere Pokémon.
- **Kleine heal na elk gevecht** (orde 10%, exact getal bepalen tijdens het testen; relics kunnen het verhogen).

## Balans / HP
- **Rekenscript:** `tools/grounded/spire/balance.py` (echte Gen 5+-schadeformule, soorten/typetabel uit de broncode; `--run` speelt hele acts na, `--set sleutel=waarde` voor andere instellingen). Speler is een simpele bot zonder potions/relics/drops, dus de echte speler doet het beter.
- **Startwaarden (v0.8.100):**
  - HP-vermenigvuldiger: **speler ×4**, normale tegenstander ×1, elite ×2,5, baas ×4,5. Levels: speler 50, vijand 48 / 50 / 52 per act.
  - Normaal gevecht = **2 tegenstanders** (geen golf): ±3 beurten, ±15% HP kwijt. Elite ±4 beurten, ±25%. Baas (+ 2 support-lakeien) ±11 beurten, ±65%, bot wint 60–80%.
  - Klap van een tegenstander ≈ 7–15% van je max HP; jouw STAB-klap ≈ 45% van een normale tegenstander, 13–17% van een elite, ±7% van een baas.
  - **Bazen niet sterker laten slaan**: bewegingskracht 75/80/85 (STAB) per act; dreiging komt uit patronen en support (lakeien die de baas buffen: +15% schade per buff, max +60%), niet uit ruwe kracht. Met 90–110 kracht en een totem-boost won de bot <5%.
  - **Heal na gevecht 20%**, rustplek 50%. Met 10% / 30% strandde de bot al in de gewone gevechten van act 1.
  - **DEFEND**: 15% van eigen max HP × verdedigingsfactor × act-factor (1 / 1,25 / 1,5) ≈ één klap. Helpt vooral in act 3 (bot haalt act 3 in 68% i.p.v. 46%); in act 1 neutraal. Eventueel act 1 iets hoger (×1,2).
  - Resultaat bot per act (vers team): act 1 48%, act 2 74%, act 3 68% gehaald; vrijwel alleen gestrand op de baas.

## Beloning (BP naar rato)
- Ook bij een paar gewonnen gevechten BP. Voorstel: 1 BP per gevecht, 3 per elite, 10 per baas, bonus per act; act 2/3 ×2/×3. Volledige run grofweg 100–150 BP (tickets kosten 200).

## Technische notities
- De **Battle Pike** heeft al deur-keuzes met kamertypes en streak-opslag: bruikbaar als basis voor de verdiepingen (later eventueel een echt kaartscherm).
- Rentals/eigen team wisselen zoals de **Battle Factory**; run-state (act, verdieping, **seed** voor kaart en tegenstanders, valuta, relics als bitveld, 2 Pokémon) past in de Frontier-opslag (paar honderd bytes).
- Expansion heeft: `settotemboost` (bazen), starttoestand via var, 2-tegen-1 in doubles werkt in de engine.
- Blok: waarde per battler, eerst aftrekken bij schade, aan het eind van de beurt op 0; klein schildgetal bij de HP-balk.
- Intentie: AI kiest een beurt vooruit en moet zich eraan houden; schadeschatting uit de AI-schadeberekening.

## Nog open
- HP-vermenigvuldigers en Defend-formule: startwaarden staan hierboven; bijstellen na het prototype.
- Aantal verdiepingen per act, bag-slots, exacte heal na gevecht.
- Inhoud: rentalpool, startermoves per Pokémon, movepool met zeldzaamheden, relicpool, bazenpool met patronen, events.
- Prototype staat (zie boven); Jordi speelt het eerst. Daarna: toren, kaart, drops, winkel.
- Intenties staan nu in het vraagvak links onderin (bovenaan is geen ruimte: levensbalken en sprites vullen het scherm). Blok en schade in % van max HP, omdat je in doubles je eigen HP-getallen niet ziet.

## Schermen (mockups, akkoord Jordi)
- Flow: gevecht → beloningsscherm (3 moves, A kiezen, B overslaan, SELECT kaart) → act-kaart → volgende kamer. Geen overworld ertussen.
- Act-kaart scrolt (±4 verdiepingen in beeld), PokéNav-stippenachtergrond, schuine gele routes met rand, gelopen pad rood, Brendan- of May-hoofdje = speler (volgt het gekozen geslacht, zoals de Town Map), rode hoekhaken = cursor, alleen de baas zichtbaar (icoon op rood plateau).
- Kamericonen: gevecht = Poké Ball (item-icoon), elite = Substitute (overworld-sprite) met een klein geel Super Saiyan-aura, rust = Chansey (icoon), winkel = blauw Mart-embleem (dak), event = Unown-?.
- Relics: eerste twee in het zijpaneel + "+N"; R opent de relic-lijst met uitleg. Cursor in menu's = de PC-hand.
- Mockups: `tools/grounded/spire/mockups.py <uitmap> v2|v4`.

## Beta-keuzes (v0.8.103, bijstellen na testen)
- Act = 7 verdiepingen + baas. Verdieping 1 altijd gevechten, verdieping 7 altijd rust, elites vanaf verdieping 3.
- Geld (¥) per gevecht 15–25, elite 35–45, baas 80; winkel: move 40/70, relic 100, Potion 30.
- BP: gevecht 1, elite 3, baas 10, × act; altijd naar je totaal (ook bij verlies).
- RUN in een gevecht = pauzeren (kamer opnieuw bij terugkomst). Tas is uit in de Spire.
- Relics als run-brede effecten (8 stuks, zie `gSpireRelics`).

## Uitwerking v0.8.104 (zie SPIRE_BALANS.md voor alle getallen)
- **Rentals:** 315 lijnen toegelaten (rekenscript): eerste (niet-baby) vorm, evolueert na act 1 en na act 2 (Gible → Gabite → Garchomp); bij een vertakking (Eevee, Kirlia, Gloom, ...) kies je. Afgevallen: Magikarp, Caterpie, Ralts, Feebas e.d. (een act te zwak), Luvdisc en andere eenstaps-soorten die niet sterker zijn dan een gemiddelde act-2-vorm. Eenstaps-soorten die té sterk zijn (Heracross, Snorlax, Gholdengo, ...) komen alleen via een event. Tiers C/B/A/S = draft-zeldzaamheid 35/35/22/8%.
- **Startkit:** STAB 40-50 per type (fysiek/speciaal naar de hoogste aanvalsstat over de run), basis-statusmove (gekozen met een verwachtingswaardemodel: Growl wint meestal, Tail Whip bij fysieke aanvallers) en een grounded move (Leech Seed, Sing, Thunder Wave, Moonlight, ...). Eén type = 3 moves (een vrije slot voor beloningen).
- **Verboden moves:** wisselen/vluchten (Teleport, U-turn, Roar, ...), doet niets (Splash, Sweet Scent, ...), vaste/procentuele schade (Psywave, Super Fang, OHKO, Pain Split, ...), KO ongeacht HP (Perish Song, Destiny Bond), items stelen (Trick, Knock Off, ...), plus Jordi's lijst (Bubble, Pound, ...). Objectief slechtere moves (automatisch bepaald) komen niet als beloning of startmove.
- **Biomes:** twee per act (Overgrown Grove/Sunken Docks, The Hive/Frostbite Hollow, Gilded Court/The Abyss), elk met zwakke (verdieping 1-2), gewone en elite-ontmoetingen die op Slay-vijanden lijken (Vine Shambler = Tangela, Fogmog = Amoonguss, Gremlin Nob = Primeape met Defiant en Rage, Lagavulin = slapende Avalugg, ...). Gevechtsachtergrond per biome; kaart in de kleur van het biome met een verloop naar karmozijn bovenin.
- **Gimmicks met Pokémon-mechanics:** vaste patronen (de AI volgt een moveslot-volgorde; de intentie toont precies wat komt), abilities, vasthouditems, totem-boosts (elites zijn totems: +1 op hun aanvalsstat), beginveld (Grassy Terrain, Trick Room, ...), slapend beginnen.
- **Bazen per act:** act 1 Venusaur & Blastoise, Totem Wishiwashi + Araquanid, Totem Alola-Marowak + Salazzle, Gigantamax Pikachu + Plusle; act 2 Mega Metagross, Darkrai, Mewtwo & Mew, Dialga & Palkia; act 3 Mega Mewtwo Y, Ultra Necrozma, Eternamax Eternatus, Mega Rayquaza, Terapagos (Terastal). Mega-, Ultra Burst-, Gmax- en Tera-vormen staan daarvoor aan in `include/config/species_enabled.h`.
- **Rustplek = Snorlax-kamp:** Chansey (40% HP, alle PP, status weg) of Porygon2 (upgrade: aanval +30%, statusmove +1 stage en mist niet, max PP; "+" achter de naam).
- **Winkel:** twee schappen (UP/DOWN): 2 moves + 1 relic; 2 vasthouditems + Move Relearner (altijd; 50¥ + 25¥ per gebruik; elke level-up-move van de huidige soort, ongeacht level).
- **Items:** vasthouditems (één per Pokémon, gebruikt = weg) met Spire-regels: Life Orb 2%, Focus Sash op elke HP, Leftovers 1/32. **Relics** zijn trainerspullen voor het hele team: Berry Pouch, Amulet Coin, Guard Spec., Dire Hit, Muscle Band, Wide Lens, Soothe Bell, Sacred Ash.
- **Events (55, v0.8.105):** datagedreven: `tools/grounded/spire/events.py` → `src/data/spire_events.h`, uitgevoerd door `src/spire_event.c`. Per event een verhaal en 1-3 opties; de effectregel naast elke optie wordt uit de effecten gemaakt (groen = winst, rood = kost, blauw = gok), dus tekst en effect kloppen altijd. Opties met een type-eis (bijv. Poison over Toxic Spikes, Flying over Dugtrio) belonen Pokémon-kennis. Effecten: geld, HP, max HP, BP, relic (winnen/verliezen), vasthouditem, move leren (willekeurig/eigen type/vast), upgrade, vergeten (willekeurig of zelf kiezen), slaap of Toxic Spikes in volgende gevechten, elitegevecht, rekruteren, speciale Ditto, Wonder Trade, vroeg evolueren, Spinda's rad. Een paar events zijn bewust gemeen (Mimikyu: wegsluipen kost max HP); er is dan altijd een goedkope uitweg. Later beginnen: Gyarados (Magikarp-verkoper), Butterfree, Milotic (Feebas), Beedrill, Diggersby, Kricketune en Absol komen via events. Elk event één keer per run (64 bits in de save).
- **Toren:** in de Battle Frontier (noordkant, Frontier-stijl), lobby `BattleFrontier_SpireLobby`.

## Nog open
- Spire-codex, golven (derde vijand), dramatischer baas-intro, ja/nee-vraag bij de receptioniste, definitieve teksten (events, hints, lobby) door Jordi.
- Balans bijstellen na Jordi's testfeedback (de rekensheets herberekenen alles).
