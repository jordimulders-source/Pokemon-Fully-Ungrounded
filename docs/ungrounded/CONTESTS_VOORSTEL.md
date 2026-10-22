> Status (9 okt): verwerkt in TODO.md; dit document is nog actueel.

# Contests reworken: voorstel

Status: alleen een voorstel, niets gebouwd. Gebaseerd op `src/contest.c` (6205 r.), `contest_ai.c`, `data/scripts/contest_hall.inc`, `berry_blender.c` (3895 r.) en `pokeblock.c`. In de changelog zit niets over contests behalve v0.6.34 (alleen Lilycove-teksten). Mechanica is dus nog 100% vanilla.

## 1. Wat is er nu saai
- **Eén hal, vijf categorieën, vier rangen = 20 contests** (Cool/Beauty/Cute/Smart/Tough × Normal/Super/Hyper/Master) om alle lint-sets te vullen. Elke contest is hetzelfde ritueel: lobby, kaartje, Pokémon kiezen, 2 rondes × 4 deelnemers, uitslag, terug. Geen enkele rang verandert de regels, alleen de AI-tegenstanders worden sterker.
- **Veel schermen en wachttijd per contest:** lobby-menu (rang, categorie, Pokémon), omkleed-/introscène, Round 1 (voorrondes: Pokéblock-stats tellen), Round 2 (5 appeals × 4 deelnemers, elk met animatie, jury-reactie en 3–4× `{PAUSE 0x0F}` per tekstregel), uitslagbord, interview. Geschat 4–6 minuten per contest, bijna allemaal wachten. Contest-teksten (~380 `COMPOUND_STRING` in `contest.c`) herhalen zich elke ronde.
- **Pokéblocks = de Berry Blender-minigame:** timing/cirkel-draaien met 4 bessen, ook voor 1 speler (NPC's). Per blok een paar minuten, en je hebt er tientallen nodig (stat-limiet 255 per categorie, +/- per blok, glans/zwaarte). Pure grind, en tegen de QoL-filosofie ("minigames eruit").
- **Onduidelijke regels:** appeal-punten hangen af van een verborgen Excitement-meter (hartjes), "jam" (hartjes weg door de ander), nervous, volgorde-effecten (`CONTEST_EFFECT_*`: 59 effecten), combo's (`contestComboStarterId`) die nergens in het spel uitgelegd worden. De speler weet niet waarom hij verliest; de AI (`contest_ai.c`, `CONTEST_AI_CHECK_*`) leest het systeem beter dan jij.
- **Moves zijn geen keuze:** de contest-categorie van een move (`contestCategory`) bepaalt of hij telt; de nieuwe moves van deze romhack (TM51–58, Fungal Control, Implosion, ...) hebben waarschijnlijk geen doordachte contest-data. Het systeem raakt de rest van het spel niet.
- **Magere beloning:** linten (36 stuks in `pokemon.h`) en wat Lilycove-items (Luxury Ball e.d. via `giveitem` in `contest_hall.inc`), plus de schilderijen. Geen reden om na rang 1 door te gaan. Bovendien ligt het nu 100% in Lilycove (ver weg, laat in het spel), terwijl Slateport/Verdanturf/Fallarbor niets met contests doen.

## 2. Mechanic-ideeën (kies er 1–2)
**A. Publiek met zichtbare voorkeur per ronde (Slay the Spire-intenties).** Bij de start van elke ronde toont het publiek een vaste voorkeur (bijv. "wil Cool", "haat herhaling", "wil iets nieuws"). Je ziet het vóór je move kiest. Past bij de "AI-keuze vóór de speler"-techniek van de Spire: de data zijn er. Bouw: middel (nieuwe tabel + bonus/malus in de appeal-berekening + 1 icoon in de UI). Grootste winst voor het minste werk.

**B. Combo's plannen.** Toon in de moveskeuze welke moves met de vorige combineren (een gloeiend randje, `contestComboStarterId` bestaat al), plus een vaste "set" per Pokémon-soort (bijv. Gengar: Hypnosis → Dream Eater). Combo's geven dubbele punten. Bouw: laag-middel (UI + hint-vlag, geen nieuwe regels). Ook een tool om tegenstanders te "jammen" tonen.

**C. Jury met persoonlijkheid.** 3 vaste juryleden met eigen smaak (zie 5): de ene geeft bonus voor de nieuwste move, de andere haat Pokémon die al een lint hebben, de derde schaalt met de vriendschap/Pokéblock-stats. Het panel wordt per contest gerold uit een pool; je ziet de smaak op het kaartje bij de inschrijving. Bouw: middel-hoog (jury-sprites bestaan al, `CreateJudgeSprite`; vooral data + berekening + teksten).

**D. Contest-synergie met de nieuwe moves en de rest van het spel.** Elke move krijgt een door jou gekozen contest-categorie/effect (op `moves_info.h`-niveau; wij hebben al "per move, geen algemene regel"). Daarnaast een "Showstopper"-move per Pokémon (de signature moves van de romhack) die één keer per contest een 3×-appeal geeft, zoals Spire-relics. Bouw: middel (data per move; ±800 moves, dus alleen de ±100 relevante doen).

**E. (optioneel) Eén ronde i.p.v. twee.** Voorronde schrappen: Pokéblock-stats worden direct beginpunten. Halveert de tijd. Bouw: laag.

## 3. QoL (gaat altijd mee, ook zonder mechanic)
1. **Pokéblocks zonder minigame:** Berry Blender wordt een menu: kies 1–4 bessen, krijg meteen het blok (kwaliteit uit de bessen, vaste "Excellent"-snelheid), meerdere tegelijk (aantal kiezen, zoals Rare Candy). Minigame-code laten staan maar niet bereikbaar, of volledig weg om ROM te sparen (±12 KB). Blender-NPC's: de dialoog blijft.
2. **Rangen overslaan:** na Normal een directe toegang tot de hoogste waarvoor je een lint/badge hebt; of alle rangen in één contest per categorie met een moeilijkheid-keuze in het lobbymenu (laatste keuze wordt onthouden).
3. **Sneller animeren:** alle `{PAUSE 0x0F}`-ketens in `contest.c` eruit of één keer; AI-appeals van tegenstanders met halve animatietijd (`sFastBattleAnim`-achtig); "skip" voor de tekstregels van NPC's; uitslagbord direct. Doel: ≤ 90 seconden per contest.
4. **Geen overbodige vragen:** "Wil je meedoen?"-vragen weg (de keuze gebeurt in het lobbymenu), Pokémon kiezen met de laatst gebruikte voorgeselecteerd.
5. **Summary-scherm:** contest-stats (Cool/Beauty/...) + lintjes als eigen pagina met tekst "komt dit Pokémon beter tot zijn recht in Cool of Smart?"; plus in het Pokéblock-menu en bij de Lobby-receptioniste een bestemmingsadvies. De pc toont ze ook (nu alleen in het summary-scherm).
6. **Uitleg waar het hoort:** korte hint per appeal-regel in het contest-scherm (hartjes, jam, nervous) in plaats van een tutorial-praatje; één info-knop (SELECT) in het moveskeuzescherm.
7. **Contesthallen dichterbij:** Slateport (Contest Reporter staat er al) en Verdanturf (de 5 "Contest Hall"-kaarten zijn al in de ROM) als tweede/derde ingang, of een snelle warp vanuit de Lobby.

## 4. Beloningen (geen TM's; alle TM01–59 liggen al)
- **Nieuwe contest-items:** Contest Pass 2.0 (key item: Fly-bestemming Lilycove-hal), Contest Scarf-achtige hold-items met effect in contests én in gevechten (bijv. "Applause Band": +10% Sp. Atk. als de Pokémon een lint heeft), Luxury Ball blijft.
- **Linten krijgen gevechtswaarde (klein):** per 5 linten +1 vriendschap/happiness-trigger, of een permanente 1-Pokémon-trait (bijv. "Ribbon Master": jaar-lang ± 1% crit). Past bij "tools voor de speler".
- **Move Tutor-reward:** per categorie een unieke show-move die als aanval ook nuttig is, bijvoorbeeld voor elke categorie één (5 totaal), een move zonder TM en dus geen conflict. Eventueel de signature-moves van Jordi.
- **Battle Stadium-koppeling:** de contest-juryleden (zie 5) en de Contest Master als iconische personages in de Stadium-pool (CLAUDE.md-regel), met hun "sterkste" team.
- **BP-valuta:** contest-punten die je in de Frontier-winkel kunt inwisselen (geen tickets die al bestaan: wel nieuwe cosmetica: kostuums voor je trainer, filmposters voor je kamer).
- **Hall of Fame-hall in Lilycove:** de schilderijen (6 plaatsen) tonen je winnaars, met een grappig onderschrift per winnaar.

## 5. Humor-haakjes (huisstijl: droog, absurd, donker)
- **Jury van drie cynici:** een voormalige modejournalist die alles "gemiddeld" vindt, een gepensioneerde Pokémon-fokker die elke Pokémon met zijn oude Pokémon vergelijkt, en een AI-chatbot ("Beoordeling: 6,4/10, met een weging naar aanbod"). Per jurylid een reactiezin (goede/slechte appeal).
- **De Pokéblock-bar:** de Blender-baas ("Blend Master") verkoopt je gewoon kant-en-klare blokken en kan niet uitleggen waarom hij vroeger een minigame bouwde.
- **Pushy ouders, influencers en een deelnemer die een proces dreigt aan te spannen** (voortbouwend op de v0.6.34-sfeer, die al klopt).
- **Interview na afloop:** reporter vraagt "Wat betekent deze overwinning voor jullie?" met drie antwoorden die op speciale NPC-trainers reageren; ja/nee niet nodig, de A-knop geeft het standaardantwoord.
- **Lint-tekst als bijschrift:** "Dit lint is uitgereikt voor hard werken. Of voor niemand anders durven te laten winnen."

## 6. Vragen aan Jordi
1. Wil je contests een volwaardig tweede spoor (zoals de Spire, veel eigen mechanics) of een lichte QoL-opfrisbeurt zonder nieuwe regels?
2. Mogen de Berry Blender-minigame en de Pokéblock-grind volledig weg (menu met direct blokken)? Of moet er iets overblijven van de Blender?
3. Welke mechanic-ideeën (A–E) spreken je aan? Mijn voorstel: A + B (publiek + combo's), plus E.
4. Moeten de vier rangen blijven, of één contest per categorie met een moeilijkheidskeuze?
5. Mogen Slateport/Verdanturf een eigen contestzaal krijgen, of blijft alles in Lilycove?
6. Welke beloningen: contest-items en een unieke show-move per categorie (ja/nee)? Mogen linten kleine gevechtsvoordelen geven (past dat bij je ontwerp)?
7. Jury en Contest Master in de Stadium-pool: ja? En wil je zelf de humor van de jury schrijven (Dialoogstudio) of een placeholder van mij?
8. Moet contest-data per move ook voor de nieuwe moves van deze rom (TM51–58 e.d.) afgestemd worden? Welke categorie krijgt Acid Rain, Pollen Haze, Implosion, enzovoort?
9. Timing: wanneer in het spel? Nu (voor de beta) of na de beta, zoals het Trick House?

## Aanbevolen eerste bouwstap
**QoL-pakket (puntjes 3.1, 3.3, 3.4):** Berry Blender als menu (direct Pokéblocks, aantal kiezen) en de contest-wachttijden (`{PAUSE}`-ketens, AI-animaties) inkorten. Dat levert direct de grootste tijdwinst, kost geen regelwijzigingen, en geeft de basis om daarna mechanic A of B op te zetten. Bouwschatting: 1 sessie. Pas daarna (stap 2) de mechanics na jouw antwoorden op vragen 1–5.
