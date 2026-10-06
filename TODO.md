# Project Grounded – takenlijst

Overzicht van wat nog moet gebeuren. Werkafspraken staan in `CLAUDE.md`; afgeronde taken gaan naar `CHANGELOG.md`.

## Openstaande taken (in volgorde)
- **Legendary-thema's + intro's (Jordi, 6 okt):** muziek loopt (Lugia 657, Ho-Oh 658, Tornadus/Thundurus/Landorus 659–661, eigen composities). Daarna: intro's Lugia, Ho-Oh, Volcanion, Hoopa, Forces-trio (voorstellen in de chat, wacht op Jordi's ok); thema's Volcanion en Hoopa. Hoopa en de Forces-trio zitten nog niet in de wereld (legendaries gepauzeerd).
Van makkelijk naar moeilijk uit de backlog en QoL (Jordi, okt 2026). Onderaan:
- **Muziek: Neo Plasma**: v4 (v0.9.70) naar Jordi's mp3; wacht op zijn oordeel (open: 'gitaar' = synth brass of strings? bas octaaf lager?).
- **Cinematische gevechtsintro's (Jordi, 5 okt; brief in de scratchpad `TRANSITIE_BRIEF.md`, voorbeeld Mewtwo):** klaar: SickBlik, Steven, Wally, Rayquaza, Kyogre/Groudon, Ogerpon, werkstraf, Dave-tribune, Mimi, Keccles, Burglar (v0.9.92–0.9.102; filmspeler `film.py` voor nieuwe intro's). Nog te doen: Maxie & Archie (werkstraf-prikbord; Jordi geen grote fan, sterker maken), Kyogre/Groudon (muurschildering barst, water/lava), Ogerpon (nachtfestival, maskerstal), Dave (tribune met wave, spandoek "DP PENNINGS", penalty in de winkelhaak, GOAL!; vriendengroep-meme), Mimi (poppenkast, Pikachu-pop draait zijn kop), Keccles (hoogintelligent + camouflage), Burglar (bewakingscamera, Gen 1-Burglarsprite als comic relief), en per gymleider één intro op basis van hun eigen dialogen en hun gym.
- **"Emerald super deluxe" (Jordi, 6 okt):** de hele kaart vol content: leuke dingen om te doen, leuke gevechten, ondervertegenwoordigde types en weinig voorkomende Pokémon een plek geven. Volgorde: (1) zee-fixes (bezig), (2) zeevulling Route 126/127/107 + onderwater (bezig), daarna 131/133 en de rest van `KAART_REVIEW.md` (Route 122, Ever Grande, Mt. Pyre Exterior, Desert Underpass, Whirl Island-lagune; Southern/Birth/Faraway mogen leeg blijven: ticket-eilanden), (3) gymleider-intro's in twee delen (`GYM_INTRO_IDEEEN.md`, zuinig ±30–60 KB per stuk), (4) vuurtoreneiland (schets goedgekeurd), (5) een **paradox-eiland/-plek** waar je paradox-Pokémon kunt krijgen (concept voorleggen), (6) **eigen Grounded-Pokédex** zonder weggelaten soorten (bijv. Ultra Beasts; `DEX_ANALYSE.md` geeft kandidaten, Jordi kiest), (7) Tapu-eiland en Dragon Island onder Pacifidlog. Contests: Jordi bedenkt zelf de ideeën.
- **Alle Pokémon verkrijgbaar (Jordi, 6 okt):** (a) de vergeten gewone lijnen wild (Caterpie, Rattata, Meowth, Buneary, Glameow, Komala, Skwovet); (b) Alola/Galar/Hisui-vormen alleen als gift of in heel speciale gebieden; (c) legendaries: **gepauzeerd** (Jordi, 6 okt), behalve Type: Null + Magearna (gifts), het Tapu-eiland en Cresselia op een nieuw eiland; plan in `LEGENDARY_PLAN.md`. Ondervertegenwoordigde soorten/types (overal, niet alleen zee) staan in `ONDERVERTEGENWOORDIGD.md`: die eerst een plek geven, vooral op zee (meeste ruimte).
- **Contests reworken** (Jordi, 5 okt): de Pokémon Contests helemaal herzien en leuker maken. Eerst een voorstel (wat is er saai, welke mechanics, QoL, beloningen), dan bouwen.
- **Spire (Jordi test eerst verder; daarna):** gewone gevechten per deel van de act (begin/midden/eind, zoals Slay the Spire), elites één pool per act. Gevechten meer als puzzel: elk gevecht iets unieks dat een veelzijdig team beloont, niet alleen je sterkste move (met de Pokémon-uitzondering dat je soms precies de perfecte counter hebt). Testchecklist: `SPIRE_TESTCHECKLIST.txt`.
- **Trick House vervangen?** (Jordi overweegt het weg te halen voor iets nieuws). Kost maar ±40-50 KB (11 kaarten, puzzels, teksten, tileset) van de 6,5 MB vrij: ruimte is geen reden, gameplay wel. Wacht op Jordi's idee.
- **Open vragen voor Jordi:** `VRAGEN_VOLGENDE.md` (shiny Rayquaza, Delta Episode, Archie/Maxie post-game, volgorde gebieden, signature moves, Gen 4+-sprites, Burglar). `VRAGEN_OCHTEND.md` is afgehandeld.

## Fase v0.9 (Jordi, 4 okt 2026), in deze volgorde
1. **Muziek uit MP3:** niet als gestreamd sample (kost ±5 MB; Jordi: ROM-ruimte is kostbaar). Alleen als MIDI (paar KB). Zinnia-gevechtsmuziek bestaat al als MIDI (`oras_zinnia.mid`). Voor Wally's Theme, Battle! Wally, The Heirs to Eternity en The Lament of Falling Stars: MIDI-versies nodig (Jordi levert aan of we zoeken ze).
2. ~~**Shiny Rayquaza**~~ (gedaan, v0.9.0): tweede ontmoeting op de Sky Pillar (zelfde soort, gegarandeerd shiny), pas nadat de gewone Rayquaza gevangen is. Pas daarna kan de Delta Episode. Alleen met de shiny Rayquaza in je team mag je de ruimte in ("zodat je kan blijven ademen").
3. ~~**Delta Episode met Zinnia**~~ (gedaan, v0.9.0; open: definitieve beloning, nu 3 Comet Shards): Zinnia-gevecht op het lanceerplatform in Mossdeep → ruimte/Deoxys zoals nu → afsluiter bij de meteoriet. Met de MP3-muziek.
4. ~~**Archie en Maxie post-game: werkstraf**~~ (gedaan, v0.9.1, dagelijks i.p.v. wekelijks). Vrijwilligers in de Lilycove-museumtuin/het Weather Institute, wekelijkse tag battle-rematch met steeds sterkere teams. (Ook in de Stadium-pool.)
5. ~~**Signature moves, met eigen animaties**~~ (gedaan, v0.9.4; voorstel extra signatures in `VRAGEN_VOLGENDE.md`):
   - Cofagrigus: **Mummy's Curse** (soort Curse, maar unieker; zelf bedenken).
   - Stunfisk: move waarbij hij zelf dubbelklapt en de tegenstander klemt; Stunfisk en Galar-Stunfisk elk een eigen variant.
   - Mightyena: **Pack Howl** (+1 Atk team in dubbel / +1 Atk +1 Spe solo).
   - Wailord: **Whale Song** (raakt alles, 30% slaap). Luvdisc: **Heartbreak**.
   - Daarna een voorstel: welke saaie/niet-unieke Pokémon (of met lore/power-reden) verdienen nog een signature move of buff?
6. ~~**Burglar in de overwereld**~~ (gedaan, v0.9.3): kleine kans als je een stad binnenloopt (meerdere steden, vooral 's nachts in Mauville) dat hij uit een huis komt; jij spot hem, gevecht (team zoals de Burglars in andere games). Na verlies staat hij verbijsterd, de bewoner komt naar buiten en pakt zijn/haar spullen terug, hij rent weg en laat een Nugget vallen.
7. **Gebieden (volgorde akkoord):**
   1. **Safari-uitbreiding (Jordi, 4 okt):** drie zones via openingen naar eigen kaarten (eigen tilesets): **Fairy Forest**, **Thunder Plains**, **Haunted Camp** (gedaan, v0.9.11; op slot met `FLAG_SAFARI_ZONES_OPEN`).
      - ~~**Sidequest om ze te openen**~~ (gedaan, v0.9.15; Petrel in de Stadium-pool v0.9.21): buiten de Safari Zone loopt een Team Rocket-grunt tegen je aan die de zonesleutels heeft gestolen en snel wegrent. De **Rocket-hideout is verstopt in Fortree Jungle**. Daar vecht je tegen grunts en een executive (Rocket-transitie met een rode R, Rocket-muziek; teams veel origineler dan alleen Koffing). Je krijgt de spullen terug, brengt ze naar de Safari en mag als dank de nieuwe zones testen.
   2. ~~**Jungle onder Fortree**~~ (kaart gedaan, v0.9.5; tropischer v0.9.8).
      - ~~**Zarude (post-game)**~~ (gedaan, v0.9.18): vaste ontmoeting op de vrijgehouden open plek, met ruïne-tiles, een eigen gevechtstransitie en het eigen thema "Battle! Zarude" (v0.9.9, nog bijstellen op Jordi's feedback). Na de Rocket-quest bouwen (die past nu de jungle aan).
      - ~~**Ogerpon:** eigen quest~~ (gedaan, v0.9.22; open: Stadium-pool, definitieve teksten, eventueel eigen transitie).
   3. ~~**Moeras: Mangrove Mire**~~ (gedaan, v0.9.18) – mangrovemoeras tussen Fortree Jungle en Route 120 (Jordi akkoord, 4 okt; Ekat99-moerastileset), aansluitend op de Scorched Slab-uitbreiding.
   4. Oostkant: eilandjes en Dive-grotten.
9. **Battle Stadium:** ~~N en Ghetsis in de pool~~ (gedaan, v0.9.2). **Back sprites:** niet tekenen (Jordi, 4 okt: niet overtuigend). In plaats daarvan toont het Stadium aan onze kant geen trainer-backs; de Pokémon staan meteen op het veld (in de maak).
8. **Dungeons uitbreiden (Jordi, 4 okt):**
   - ~~Petalburg Woods: verborgen paddenstoelenbos~~ (gedaan, v0.9.10: Toadstool Hollow).
   - ~~Meteor Falls~~ (gedaan, v0.9.13). Open: Selene (Draconid-oudere) in de Battle Stadium-pool.
   - ~~Jagged Pass ondergronds en Mt. Chimney hoger~~ (gedaan, v0.9.16).
   - ~~Victory Road: optionele kamers~~ (gedaan, v0.9.14). Open: Reginald (en eventueel Selene uit Meteor Falls) in de Battle Stadium-pool.
   - Onderwater: veel meer te ontdekken.
   - ~~Scorched Slab~~ (gedaan, v0.9.17: zonnetempel met lichtpuzzel). Open: Helia in de Stadium-pool (na Jordi's test); ~~vanilla Strength-puzzels (Seafloor Cavern) nalopen~~ (gedaan, 5 okt: duwen werkt, blok staat na opnieuw binnenkomen weer op zijn plek).
   - Eigen suggesties van Claude welkom (eerst voorleggen).

## Besloten met Jordi (2 okt 2026), nog te bouwen
1. ~~Fungal Control~~ (gedaan, v0.8.45)
2. ~~Transmutation~~ (gedaan, v0.8.46)
3. ~~Implosion~~ (gedaan, v0.8.48–0.8.49)
4. ~~Wild summary~~ (gedaan, v0.8.44)
5. ~~Gabby & Ty~~ (gedaan, v0.8.61)
6. ~~Heatran-cutscene~~ (gedaan, v0.8.59)
7. ~~Rotom-event~~ (gedaan, v0.8.60)
8. ~~Prof. Oak~~ (gedaan, v0.8.50)
9. ~~Mimikyu-trainer~~ (gedaan, v0.8.58)
10. ~~Laser Beam / Machine Learning / Shadow Siphon~~ (gedaan, v0.8.51–0.8.53)

## Volgende ronde (Jordi, 2 okt 2026), in deze volgorde
1. ~~Hoennian Grimer/Muk~~ (gedaan, v0.8.67–0.8.68; speler krijgt er één van Birch)
2. ~~Transities Regidrago/Regieleki/Deoxys/Birch~~ (gedaan, v0.8.62–0.8.65)
3. ~~Sootopolis na Rayquaza met Keccles~~ (gedaan, v0.8.66). Open: Archie en Maxie eventueel terug in de post-game.

## Quality of life (nog te doen)
- **Goedgekeurd:** (alles afgerond)
- **Later proberen:** (snellere schermovergangen bij warps gedaan in v0.8.36; gevechtsintro eventueel later)

## Backlog (brainstorm Jordi, okt 2026; nog niet ingepland, Ashfrost eerst)
Plan van aanpak en open vragen per onderdeel: `BACKLOG_PLAN.md` (3 okt 2026). Eerst Jordi's antwoorden afwachten.
Per idee eerst kort afstemmen vóór het bouwen. Credits van externe assets/muziek in de credits zetten.
- **Ruimte-tijdgrot (Jordi, 5 okt):** een grot waar Palkia en Dialga de dienst uitmaken en je laten teleporteren naar gebieden uit andere Pokémon-games: Cerulean Cave (volledig nagemaakt; de huidige Mewtwo-grot achter Meteor Falls is een placeholder), Lavender Town + Pokémon Tower, National Park, de Gen 4-meren. **Jordi ontwerpt de ruimte-tijdgrot zelf** (6 okt): niet bomvol, vooral nostalgische warps (o.a. Area Zero); geen vogellocaties, Ilex Forest of Fullmoon Island; Ultra Space wordt een los gebied.
- **Kaarten/gebieden:** Oostkant van de kaart interessanter (meer eilanden, beter onderwater-exploreren, nieuwe dungeons). Jungle onder Fortree (Ogerpon/Zarude). Swamp, fairy forest, mushroom forest, haunted house, outer-space-gebied vanaf Mossdeep. Safari Zone uitbreiden. Extra tilesets (Ekat99, o.a. Snowpoint Temple voor Regigigas).
- **Legendary/mythical events:** (Regi-quest v0.8.96; tickets en Lati-keuze v0.8.97; Genesect, Mewtwo, Giratina, Victini, Jirachi, Darkrai, Shaymin en Kubfu gedaan in v0.8.120–0.8.125, elk met eigen transitie) Nog open: shiny Rayquaza en de Delta Episode met Zinnia (zie `VRAGEN_VOLGENDE.md`).
- **Birch:** dialoog bij Ashfrost veel smeriger. (Verdanturf-gevecht en Route 135-team met Hisui-Avalugg gedaan, v0.8.67; Mossdeep-meteoriet en onder water gedaan, v0.8.79)
- **Trainers/NPC's:** (Colress gedaan v0.8.95; Burglar als Stadium-deelnemer v0.8.111, nog niet in de overwereld) trainersprites Gen 4+ (Greenphx); onderzoeken of Gen 4/5-overworldsprites om te zetten zijn.
- **Moves:** meer signatures (Cofagrigus, Stunfisk, Mightyena, Wailord, Luvdisc, ...).
- **Mechanics/systeem:** (The Spire en het Battle Stadium gedaan, v0.8.100–0.8.111) rental-teams van de Frontier reviseren.
