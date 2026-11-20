# Cosmic: soorten en moves

Matchups en het besluit om het type te maken staan in `CONCEPT.md` (Nieuw type: Cosmic). De huidige types komen uit de repo (`src/data/pokemon/species_info/`, `src/data/moves_info.h`).

## Besloten
**Soorten**
- Curiqui (fase 3 nachtaap-lijn): Psychic/Cosmic. Dustly → Hauntflare → Gengas: Cosmic/Poison. IJskomeet (fase 3 sneeuwbolslak): Ice/Cosmic.
- **20 nov (Jordi):** Lunatone en Solrock (Rock/Psychic → Rock/Cosmic), Clefairy-lijn ("akkoord"; Cosmic of Fairy/Cosmic nog open), Elgyem → Beheeyem (Cosmic; Psychic houden nog open), Staryu → Starmie (Water / Water/Cosmic), Sigilyph (Cosmic/Flying), Baltoy → Claydol (Ground/Cosmic; "wordt wel sterk gesuggereerd dat die buitenaards zijn"), Beldum-lijn (Steel/Cosmic).
- **Deoxys** komt officieel in de dex (Jordi, 20 nov). **Minior** ook (Jordi: "vgm al eerder aangegeven dat die erin moest"). Beide staan sinds 20 nov aan in `include/config/species_enabled.h`.

**Moves (Jordi's lijst, 20 nov):** Swift, Moonblast, Meteor Mash, Meteor Beam, Implosion, Laser Beam, Gravity, Lunar Dance, Moonlight, Lunar Blessing, Trick Room, Cosmic Power. Photon Geyser, Prismatic Laser, Hyperspace Hole en Doom Desire: vraag of het legendary-signatures zijn (antwoord hieronder).
- Jordi: "bij status moves maakt het niet uit wat voor type het is, want zit geen STAB op."
- **Jordi (20 nov): "we moeten ook cosmic moves gaan ontwerpen."**

- **20 nov, tweede ronde (Jordi):** Minior per vorm: meteoorvorm Rock/Cosmic, kernvorm Flying/Cosmic ("derde optie uitstekend idee"). Elgyem-lijn puur Cosmic. Deoxys Psychic/Cosmic. Clefairy-lijn Fairy/Cosmic. Comet Punch wordt Cosmic. Nieuwe Cosmic-moves ontwerpen: later.

- **Niet Cosmic (Jordi, 20 nov):** Inkay → Malamar ("hij is niet buitenaards, dus niet veranderen") en Bronzor → Bronzong ("evenals").

## Open: soorten

**Psychic houden of niet (Elgyem-lijn, Deoxys), berekend op de typetabel:**
- Puur Cosmic is zwak voor Poison, Rock, Psychic en Cosmic, resisteert Steel, Fire en Water en is immuun voor Fairy.
- Psychic/Cosmic is zwak voor Bug, Ghost, Dark, Poison, Rock en Cosmic (6 zwaktes), resisteert Fighting, Steel, Fire en Water en is immuun voor Fairy. Psychic doet neutraal.
- Voor Psychic houden:
  - Beheeyem leest en wist herinneringen en Deoxys is in de canon sterk psychisch; dat blijft kloppen.
  - Psychic dekt aanvallend Poison, de zwakte van Cosmic.
  - Psychic- en Cosmic-STAB samen raken veel types hard: Fighting, Poison, Steel, Electric, Fairy en Cosmic.
- Tegen Psychic houden:
  - Jordi wilde juist soorten weghalen bij Psychic.
  - Psychic/Cosmic heeft 6 zwaktes; puur Cosmic heeft er 4.
  - Curiqui is al Psychic/Cosmic. Ook de Baltoy-lijn, Lunatone en Solrock verliezen Psychic.
  - Deoxys: maken we hem puur Cosmic, dan kan Psycho Boost (zijn signature, 140) mee naar Cosmic.

**Meer opties (alleen ter overweging):**
- In de dex: Natu → Xatu (kijkt de hele dag naar de zon), Espeon/Umbreon (zon en maan), Volcarona ("vervangt de zon"), Magnezone (UFO-vorm), Unown.
- Niet in de dex: Jirachi, Cosmog-lijn/Necrozma, Celesteela (Ultra Beast in de vorm van een raket), Orbeetle (UFO-kever). Elk van deze moet eerst in de dex komen.

## Open: moves
- **Signatures:** ja. Photon Geyser en Prismatic Laser zijn van Necrozma, Hyperspace Hole van Hoopa en Doom Desire van Jirachi. Geen van die soorten zit in de dex, dus niemand leert ze tenzij we ze uitdelen, bijvoorbeeld aan Deoxys of een eigen ruimte-legendary.
- **Psycho Boost** (Deoxys, Psychic 140) mist nog op de lijst; alleen omzetten als Deoxys puur Cosmic wordt.
- **Implosion** (eigen move uit Grounded, Dark 200, "collapses into a black hole"; gebruiker valt flauw) leren nu Voltorb, Electrode (ook Hisui), Lunatone, Solrock, Dusknoir, Drifblim, Deoxys, Minior, Cosmoem, Necrozma en Darkrai. Wordt hij Cosmic, dan verliezen Voltorb, Electrode, Dusknoir en Drifblim hun Dark-nuke. Zij houden hem gewoon, maar zonder STAB.
- **Laser Beam** (eigen move, Psychic 75, gaat door Protect, schermen en boosts heen).
- **Status:** Jordi heeft gelijk dat het type daar bijna niets uitmaakt. Uitzonderingen: Protean/Libero (de gebruiker krijgt het type van de move) en de kleur en animatie in het menu.

**Gaten in de aanvallende moves:**
- Geen zwakke beginmove (±40); Swift (60) is de zwakste.
- Fysiek alleen Meteor Mash (90, Steel → Cosmic): geen fysieke beginmove en geen sterke fysieke move.
- Special loopt wel op: Swift 60 → Laser Beam 75 → Moonblast 95 → Meteor Beam 120 → Implosion 200.

## Nieuwe Cosmic-moves (ideeën Claude; ontwerpen komt later, Jordi 20 nov)
| Idee | Rol | Voorstel |
|---|---|---|
| Comet Punch (bestaat al, Normal 25 ×2–5) | fysiek, vroeg | **besloten (Jordi 20 nov): wordt Cosmic** |
| Stardust | special, vroeg | 40 kracht, 100%; misschien kans op accuracy omlaag (glinsterend stof) |
| Shooting Star | fysiek, priority | 40 kracht, +1 priority (vallende ster, de Mach Punch van Cosmic) |
| Black Hole | special, middel | 80 kracht, het doelwit kan niet wisselen (zwaartekracht trekt) |
| Solar Wind | special, sterk | 90 kracht, blaast hazards weg aan de kant van de tegenstander |
| Supernova | fysiek, sterk | 120 kracht met terugslag (de fysieke tegenhanger van Meteor Beam) |
| Eclipse | status | verlaagt de accuracy van iedereen op het veld (zon/maan, Inti en Mama Killa) |
| Mayu | status | de "rivier" van de Melkweg uit de Inca-sterrenkunde; idee: geneest een beetje per beurt voor het hele team. Koppeling met de lore van de Gastly-lijn (Mayu, `IDEEEN.md`) |
