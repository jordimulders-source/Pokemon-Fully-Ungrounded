# Pokémon Fully Ungrounded – concept (overzicht)

Wat in de conceptdocumenten staat, is **besloten** door Jordi. Losse ideeën staan in `IDEEEN.md` tot ze besloten zijn.

| Document | Inhoud |
|---|---|
| `CONCEPT.md` | dit overzicht: basis, structuur, gyms |
| `REGIO.md` | regio, kaart, steden, gebieden, landmarks |
| `VERHAAL.md` | toon, verhaal, protagonist, Keccles, tegenstanders, mythologie |
| `POKEMON.md` | starters, legendaries, fakemon en regional forms, met per Pokémon de inspiratie (los van de plek in de regio) |
| `SPRITE_PLAN.md` | hoe we sprites maken (Hoenn-sprites als leidraad) |
| `MUZIEK.md` | soundtrack: Zuid-Amerikaanse en Latijns-Amerikaanse stijlen |
| `FAKEMON_PITCH.md` | 100 korte fakemon-pitches om te keuren |
| `ROUTEPLAN.md` | verdeling van plekken, dungeons en legendes over de gymsegmenten (concept) |
| `DUNGEONS.md` | originele dungeons (natuurverschijnselen met een eigen mechaniek, à la Chargestone) |
| `MYTHOLOGIE.md` | legendes en mythen uit Zuid-Amerika als bron voor plekken en Pokémon (opties) |
| `IDEEEN.md` | ruwe verzameling van alle ideeën |
| `regiokaart*.png` | schetsen van de regiokaart (`tools/concept/regiokaart*.py`) |

## Basis
- Vervolg op Pokémon Ungrounded, ambitieuzer en groter dan Hoenn. Fork van Ungrounded op pokeemerald-expansion: revisies, nieuwe moves/abilities en QoL blijven.
- Nieuwe regio gebaseerd op Zuid-Amerika: geïnspireerd, niet nagemeten (zoals Hoenn op Kyushu). Eigen kaart en eigen namen.
- 8 gyms en een Elite 4. **Gymvolgorde lineair** (houdt de levelcurve gezond), maar **de kaart niet** (zie `REGIO.md`). E4 rond lv 80–90.

## Gyms en Elite 4
- **Gymtypes:** Dark, Ice, Bug, Dragon, Ground, Grass, Fire, Poison. **Gym 1: Ground in Uyuni** (direct vanuit La Paz naar de zoutvlakte), **gym 2: Ice**, **gym 8: Bug, in de jungle** (Jordi: Bug wordt altijd als early-game-type gezien, juist daarom als laatste; en insecten zijn de meest voorkomende dieren in het regenwoud). Een mooi einde van de gymtocht: **helemaal afgelegen in de jungle, met extreem veel avontuur** om de laatste badge te halen: de rivier/Amazone **helemaal af naar het einde**, **geen Pokémon Centers maar een paar rest houses**, **veel sterke wilde Pokémon**, ook hele sterke Bugs (bijv. Flygon, in deze game Bug/Dragon). De volgorde mag **onconventioneel en onverwacht**; volgorde en plekken: zie hieronder (akkoord).
- **Elite 4:** Electric, Flying, Ghost, Steel.
- **Gymlevels (ace, Jordi 22 okt):** gym 1 ±18, gym 2 ±24, gym 3 ±30, gym 4 ±36, gym 5 ±47, gym 6 ±54, gym 7 ±63, gym 8 ±75, League mid 80 tot 90. Gevolg: rond het midden van de game is vrijwel alles fully evolved. De sprong 36 → 47 valt in het grote middenstuk tussen gym 4 en 5. Levelcurve-regel uit Ungrounded: met regulier spelen zit de speler 2–3 levels onder de ace (meten met `tools/grounded/levelcurve.py` zodra er trainers zijn); evolutielevels van eigen fakemon hierop afstemmen.
- **Pokémon League in Machu Picchu.** Cuzco bezoek je al eerder en je komt er meerdere keren terug. De League staat **los van het verhaal** (zoals in bijna elke game behalve B/W).
- **Gymlocaties akkoord (Jordi, 22 okt, nogmaals bevestigd):** Ground – Uyuni (gym 1), **Ice – Cordillera Real** (gym 2; Jordi, 22 okt: 'meer grounded', echte gletsjers naast La Paz, en het past bij het niet-lineaire: na Uyuni terug naar het noorden, daarna weer zuidwaarts via Lípez naar Atacama), **Fire – Atacama** (San Pedro), **Dragon – Cuzco** (Amaru), **Poison – Buenos Aires**, **Dark – Rio de Janeiro**, **Grass – Paramaribo**, Bug – diep in de jungle (gym 8). **Volgorde akkoord (Jordi, 22 okt):** 3 Fire (Atacama), 4 Dragon (Cuzco), 5 Poison (Buenos Aires), 6 Dark (Rio), 7 Grass (Paramaribo), 8 Bug (jungle): van Rio **niet** langs de kust naar Paramaribo: je moet **terug (backtracken) en via Colombia** (Andes-noord: Quito/Salento/Medellín/Cartagena) naar Paramaribo, zodat het niet lineair wordt (Jordi); de kustroute Rio → Belém → Paramaribo gaat pas later open. Daarna de Amazone in.
- Niet als gym/E4: Normal, Water, Fighting, Psychic, Rock, Fairy (kampioen open).
- **Cosmic krijgt een gym of E4-lid** (Jordi, 12 nov). Welke plek: nog open (de huidige 8 gyms + 4 E4 zijn allemaal ingevuld).

## Nieuw type: Cosmic (besloten, Jordi 12 nov: "we gaan het doen")
- 19e type voor al het buitenaardse (ruimte, sterren, maan, meteorieten, aliens); haalt soorten weg bij Psychic. Uitwerking (soorten, moves, code) in een later gesprek.
- **Matchups:** super effective tegen Steel, Electric, Fairy, Cosmic; not very effective tegen Bug, Rock, Ice. Resist Steel, Fire, Water; immuun voor Fairy; zwak voor Poison, Rock, Psychic, Cosmic. Fairy mag een flinke nerf (Jordi).
- **Kandidaten (Jordi) worden definitief Cosmic (Jordi, 21 nov: "de kandidaten die ik noemden mogen cosmic worden definitief"):** Elgyem-lijn, Lunatone & Solrock, Baltoy-lijn, Minior, Deoxys, Clefairy-lijn; Cosmic Power wordt een Cosmic-move.
  - Typing per soort (voorstel Claude 21 nov, waarop Jordi dit besloot): Lunatone en Solrock Rock/Cosmic, Baltoy/Claydol Ground/Cosmic, Clefairy-lijn Fairy/Cosmic, Elgyem/Beheeyem puur Cosmic (Jordi, 21 nov: "Elgyem lijn puur cosmic"). Minior en Deoxys staan niet in de dex; terughalen is niet besloten.
  - **Staryu en Starmie (gewone vorm) worden Water/Cosmic** (Jordi, 27 nov: "staryu en starmie normaal worden water/cosmic"). Regionale koekjes-vorm: Staryu Fairy, Starmie Fairy/Psychic (Jordi, 27 nov).
  - **Dottler en Orbeetle worden Bug/Cosmic** in plaats van Bug/Psychic (Jordi, 25 nov: "Dottler en Orbeetle worden trouwens ook cosmic ipv psychic"). De Blipbug-lijn staat in DEX_IN_ROM nog onder Categorie C (geschrapt); of hij terugkomt: gevraagd.
  - Met de al besloten Cosmic-soorten (Dustly-lijn Cosmic/Poison, Cryomet Ice/Cosmic, Curiqui Psychic/Cosmic) komt het op ±13 Cosmic-soorten. Nog geen vroege Cosmic; Steel/Cosmic (satelliet-lijn) staat in TODO. Meer kandidaten en de discussie: `IDEEEN.md` (Nieuw type: Cosmic).
- **Techniek:** eigen typenummer (niet `TYPE_MYSTERY`, dat is de codemarkering voor "geen type"); tabel in `src/data/types_info.h`.
- Typetabel als afbeelding: `typetabel_cosmic.png`.
