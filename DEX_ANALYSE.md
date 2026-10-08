> Status (9 okt): verwerkt in TODO.md; dit document is naslag.

# DEX_ANALYSE: wat zit er (niet) in de game zonder ruilen

Stand van de code (branch `claude/wonderful-brahmagupta-xz8pik`, gegenereerd door een script; machineleesbaar in `tools/grounded/dex_beschikbaar.json`). Entries = 1082 (1025 soorten + regionale vormen); verkrijgbaar zonder ruilen: 977; niet verkrijgbaar: 99 (+ 6 bewust weggelaten elemental monkeys). Mega/Gmax/Tera/Primal/Ultra Burst/kleur- en cosmetische vormen zijn weggelaten of onder de basissoort geschaard.

## 1. Nog niet in de game: aanvinklijst voor Jordi

Zet een `x` in `[ ]` bij wat erin moet. Evolutielijn per regel met [types]; een soort tussen haakjes zit al wel in de game. Tag achter de regel = legendarisch/mythisch/Ultra Beast/paradox.

### Generatie 1

- [ ] Caterpie [Bug] → Metapod [Bug] → Butterfree [Bug/Flying]
- [ ] Rattata [Normal] → Raticate [Normal]
- [ ] Rattata (Alola) [Dark/Normal] → Raticate (Alola) [Dark/Normal]
- [ ] Meowth [Normal] → Persian [Normal]
- [ ] Meowth (Alola) [Dark] → Persian (Alola) [Dark]
- [ ] Farfetch'd (Galar) [Fighting] → Sirfetch'd [Fighting]
- [ ] Voltorb (Hisui) [Electric/Grass] → Electrode (Hisui) [Electric/Grass]
- [ ] Articuno [Ice/Flying] `legendary`
- [ ] Articuno (Galar) [Psychic/Flying] `legendary`
- [ ] Zapdos [Electric/Flying] `legendary`
- [ ] Zapdos (Galar) [Fighting/Flying] `legendary`
- [ ] Moltres [Fire/Flying] `legendary`
- [ ] Moltres (Galar) [Dark/Flying] `legendary`

### Generatie 2

- [ ] Celebi [Fairy/Grass] `mythical`

### Generatie 4

- [ ] Buneary [Normal] → Lopunny [Normal]
- [ ] Glameow [Normal] → Purugly [Normal]
- [ ] Uxie [Psychic] `legendary`
- [ ] Mesprit [Psychic] `legendary`
- [ ] Azelf [Psychic] `legendary`
- [ ] Dialga [Steel/Dragon] `legendary`
- [ ] Palkia [Water/Dragon] `legendary`
- [ ] Cresselia [Psychic] `legendary`
- [ ] Arceus [Normal] `mythical`

### Generatie 5

- [ ] Cobalion [Steel/Fighting] `legendary`
- [ ] Terrakion [Rock/Fighting] `legendary`
- [ ] Virizion [Grass/Fighting] `legendary`
- [ ] Tornadus [Flying] `legendary`
- [ ] Thundurus [Electric/Flying] `legendary`
- [ ] Reshiram [Dragon/Fire] `legendary`
- [ ] Zekrom [Dragon/Electric] `legendary`
- [ ] Landorus [Ground/Flying] `legendary`
- [ ] Kyurem [Dragon/Ice] `legendary`
- [ ] Keldeo [Water/Fighting] `mythical`
- [ ] Meloetta [Normal/Psychic] `mythical`

### Generatie 6

- [ ] Xerneas [Fairy] `legendary`
- [ ] Yveltal [Dark/Flying] `legendary`
- [ ] Zygarde [Dragon/Ground] `legendary`
- [ ] Diancie [Rock/Fairy] `mythical`
- [ ] Hoopa [Psychic/Ghost] `mythical`

### Generatie 7

- [ ] Type: Null [Normal] → Silvally [Normal] `legendary`
- [ ] Komala [Normal]
- [ ] Tapu Koko [Electric/Fairy] `legendary`
- [ ] Tapu Lele [Psychic/Fairy] `legendary`
- [ ] Tapu Bulu [Grass/Fairy] `legendary`
- [ ] Tapu Fini [Water/Fairy] `legendary`
- [ ] Nihilego [Rock/Poison] `Ultra Beast`
- [ ] Buzzwole [Bug/Fighting] `Ultra Beast`
- [ ] Pheromosa [Bug/Fighting] `Ultra Beast`
- [ ] Xurkitree [Electric] `Ultra Beast`
- [ ] Celesteela [Steel/Flying] `Ultra Beast`
- [ ] Kartana [Grass/Steel] `Ultra Beast`
- [ ] Guzzlord [Dark/Dragon] `Ultra Beast`
- [ ] Necrozma [Psychic] `legendary`
- [ ] Magearna [Steel/Fairy] `mythical`
- [ ] Marshadow [Fighting/Ghost] `mythical`
- [ ] Poipole [Poison] → Naganadel [Poison/Dragon] `Ultra Beast`
- [ ] Stakataka [Rock/Steel] `Ultra Beast`
- [ ] Blacephalon [Fire/Ghost] `Ultra Beast`
- [ ] Zeraora [Electric] `mythical`
- [ ] Meltan [Steel] `mythical`
- [ ] Melmetal [Steel] `mythical`

### Generatie 8

- [ ] Skwovet [Normal] → Greedent [Normal]
- [ ] Zacian [Fairy] `legendary`
- [ ] Zamazenta [Fighting] `legendary`
- [ ] Eternatus [Poison/Dragon] `legendary`
- [ ] Spectrier [Ghost] `legendary`
- [ ] Calyrex [Psychic/Grass] `legendary`
- [ ] Enamorus [Fairy/Flying] `legendary`

### Generatie 9

- [ ] Brute Bonnet [Grass/Dark] `paradox`
- [ ] Iron Jugulis [Dark/Flying] `paradox`
- [ ] Iron Moth [Fire/Poison] `paradox`
- [ ] Iron Thorns [Rock/Electric] `paradox`
- [ ] Wo-Chien [Dark/Grass] `legendary`
- [ ] Chien-Pao [Dark/Ice] `legendary`
- [ ] Ting-Lu [Dark/Ground] `legendary`
- [ ] Chi-Yu [Dark/Fire] `legendary`
- [ ] Koraidon [Fighting/Dragon] `legendary`
- [ ] Miraidon [Electric/Dragon] `legendary`
- [ ] Walking Wake [Water/Dragon] `paradox`
- [ ] Iron Leaves [Grass/Psychic] `paradox`
- [ ] Gouging Fire [Fire/Dragon] `paradox`
- [ ] Raging Bolt [Electric/Dragon] `paradox`
- [ ] Iron Boulder [Rock/Psychic] `paradox`
- [ ] Iron Crown [Steel/Psychic] `paradox`
- [ ] Terapagos [Normal] `legendary`
- [ ] Pecharunt [Poison/Ghost] `mythical`

Bewust weggelaten, niet in de lijst: Pansage, Simisage, Pansear, Simisear, Panpour, Simipour.

## 2. Totalen per generatie (basissoorten; regionale vormen apart)

| Gen | soorten | verkrijgbaar | niet | regionale vormen verkrijgbaar/totaal |
|---|---|---|---|---|
| 1 | 151 | 141 | 10 | 26/36 |
| 2 | 100 | 99 | 1 | 6/6 |
| 3 | 135 | 135 | 0 | 2/2 |
| 4 | 107 | 96 | 11 | 0/0 |
| 5 | 150 | 139 | 11 | 9/9 |
| 6 | 72 | 67 | 5 | 3/3 |
| 7 | 88 | 64 | 24 | 1/1 |
| 8 | 96 | 87 | 9 | 0/0 |
| 9 | 120 | 102 | 18 | 0/0 |
| totaal | 1019 | 930 | 89 | 47/57 |

Eerste bron per verkrijgbare entry: wild 780, evolutie 147, statisch/scriptgevecht 31, gift 2, ei-gift 1, alleen fokken 16. Ditto is te vangen (Route 115), dus fokken werkt ook voor genderloze lijnen. Alle evolutie-items (stenen e.d.) komen ergens in de game voor; ruil-evoluties hebben in deze romhack een item-alternatief, dus geen soort valt af op ruilen alleen. Aanname: evolutievoorwaarden (tijd, plek, move) zijn haalbaar; eieren komen via de Daycare.

## 3. Types: hoeveel verkrijgbare soorten, en waar ze voorkomen

Entries met het type (dubbeltypes tellen twee keer). `Wild` = in minstens één wilde tabel; `Zee` = in water/vis-tabellen van de zeeroutes (Route 105–110, 122–134, havensteden, Underwater, Shipwreck Shoals, Whirl Island, Steam Island); `Laat` = tabellen van Route 115+, Meteor Falls, Victory Road, Sootopolis, Seafloor/Shoal Cave, Fortree Jungle e.d.

| Type | totaal | verkrijgbaar | wild | zee | laat |
|---|---|---|---|---|---|
| Normal | 131 | 113 | 87 | 12 | 54 |
| Fire | 84 | 78 | 51 | 2 | 30 |
| Water | 154 | 150 | 134 | 95 | 123 |
| Electric | 86 | 74 | 61 | 14 | 41 |
| Grass | 131 | 121 | 83 | 2 | 60 |
| Ice | 57 | 54 | 50 | 10 | 45 |
| Fighting | 81 | 69 | 48 | 4 | 34 |
| Poison | 91 | 85 | 62 | 11 | 40 |
| Ground | 82 | 79 | 68 | 7 | 46 |
| Flying | 109 | 95 | 78 | 20 | 62 |
| Psychic | 113 | 100 | 77 | 19 | 65 |
| Bug | 92 | 87 | 66 | 7 | 36 |
| Rock | 78 | 72 | 66 | 13 | 52 |
| Ghost | 73 | 68 | 60 | 16 | 43 |
| Dragon | 74 | 60 | 49 | 15 | 47 |
| Dark | 83 | 70 | 55 | 8 | 43 |
| Steel | 78 | 69 | 54 | 4 | 33 |
| Fairy | 72 | 62 | 50 | 5 | 37 |

Ondervertegenwoordigd op zee (168 soorten in zee-tabellen, 95 Water): **Fire (2), Grass (2), Fighting (4), Steel (4), Fairy (5), Dark (8), Ground (7), Bug (7)**; Electric (14), Ghost (16), Dragon (15) en Psychic (19) komen juist vaak voor. Verkrijgbaarheid is overal hoog; de gaten zitten in de verdeling, niet in het aanbod: Fairy (62 van 72), Dragon (60 van 74), Fighting (69 van 81), Dark (70 van 83) en Electric (74 van 86) zijn het minst volledig.

## 4. Niet-verkrijgbaar, gegroepeerd (zie lijst 1 voor de evolutielijnen)

- **Paradox-Pokémon (10):** Brute Bonnet, Iron Jugulis, Iron Moth, Iron Thorns, Walking Wake, Iron Leaves, Gouging Fire, Raging Bolt, Iron Boulder, Iron Crown
- **Ultra Beasts (11):** Nihilego, Buzzwole, Pheromosa, Xurkitree, Celesteela, Kartana, Guzzlord, Poipole, Naganadel, Stakataka, Blacephalon
- **Legendaries/mythicals gen 1–6 (29):** Articuno, Articuno (Galar), Zapdos, Zapdos (Galar), Moltres, Moltres (Galar), Celebi, Uxie, Mesprit, Azelf, Dialga, Palkia, Cresselia, Cobalion, Terrakion, Virizion, Tornadus, Thundurus, Reshiram, Zekrom, Landorus, Kyurem, Keldeo, Meloetta, Xerneas, Yveltal, Zygarde, Diancie, Hoopa
- **Legendaries/mythicals gen 7 (11):** Type: Null, Tapu Koko, Tapu Lele, Tapu Bulu, Tapu Fini, Necrozma, Magearna, Marshadow, Zeraora, Meltan, Melmetal
- **Legendaries/mythicals gen 8–9 (14):** Zacian, Zamazenta, Eternatus, Spectrier, Calyrex, Enamorus, Wo-Chien, Chien-Pao, Ting-Lu, Chi-Yu, Koraidon, Miraidon, Terapagos, Pecharunt
- **Overig gen 8–9 (geen legendary) (3):** Skwovet, Greedent, Sirfetch'd
- **Overig gen 1–7 (21):** Caterpie, Metapod, Butterfree, Rattata, Rattata (Alola), Raticate, Raticate (Alola), Meowth, Meowth (Alola), Persian, Persian (Alola), Farfetch'd (Galar), Voltorb (Hisui), Electrode (Hisui), Buneary, Lopunny, Glameow, Purugly, Arceus, Silvally, Komala
- Wel verkrijgbaar van de paradoxen (10): Great Tusk, Scream Tail, Flutter Mane, Slither Wing, Sandy Shocks, Iron Treads, Iron Bundle, Iron Hands, Roaring Moon, Iron Valiant. Ultra Beasts: geen enkele verkrijgbaar. Opvallend: Latias/Latios (Southern Island), Mew, Ho-Oh, Deoxys, de Regi's, Kyogre/Groudon/Rayquaza, Mewtwo, Lugia, Raikou/Entei/Suicune, Heatran, Darkrai, Jirachi, Shaymin, Victini, Genesect, Manaphy, Volcanion, Zarude, Ogerpon, Okidogi/Munkidori/Fezandipiti zijn wel te krijgen.

## 5. Suggesties voor de zee

Alles hieronder is al verkrijgbaar (elders op land/in een grot) tenzij vermeld; het is dus verplaatsen/bijvoegen in zee-tabellen, geen nieuwe soorten. Alleen wat in de wereld klopt. Teksten van de nieuwe zeegebieden zijn nog placeholders, de tabellen kunnen dus vrij.

- **Fire (2 op zee):** Slugma → Magcargo (lavaslakken; Steam Island/Volcanion-eiland, Route 130 vulkaanrif), Turtonator staat er al; Fuecoco → Crocalor → Skeledirge (krokodil, zwemt; nu alleen Safari/ei) op Paradiso Resort; Litwick → Lampent → Chandelure als dwaallichten op Shipwreck Shoals (spookschip); Torkoal (Steam Island heeft hem al, ook Route 130-oever); Salandit/Oricorio (Baile) op het tropische resort.
- **Grass (2):** Lotad → Lombre → Ludicolo (drijven op zee; nu alleen Route 102/104/119), Tangela → Tangrowth (zeewier; Route 120 land → water Route 125–127), Lileep → Cradily (zeelelie, nu Seafloor Cavern/Route 103 vis), Tropius (tropische fruitvlieger, boven Route 131–133 en het resort), Dhelmise staat er al, Bounsweet/Comfey op het resort-strand.
- **Fighting (4):** Crabrawler → Crabominable (strandkrabben; nu Route 132/Shoal Cave) op Route 128–129 en Pacifidlog, Throh/Sawk als strandtrainers aan Route 106/Dewford (Brawly-thema); Poliwrath, Clobbopus en Grapploct staan er al.
- **Steel (4):** Piplup → Prinplup → Empoleon (pinguïn, nu alleen Safari) in de koude zee bij Route 134–136, Skarmory (ijzervogel boven kliffen en wrakken, nu Route 113/Granite Cave), Magnemite/Magneton rond het wrak en de Plasma Frigate (scheepsmagnetisme), Mawile als schat-valstrik bij Shipwreck Shoals.
- **Fairy (5):** Popplio → Brionne → Primarina (zeeleeuw, nu alleen Safari), Comfey (leibloemen, Paradiso Resort), Dewgong, Azumarill, Togepi/Togetic/Togekiss staan er al; Marill-lijn kan op meer routes.
- **Dark (8):** Corphish → Crawdaunt (kreeft, nu Route 102/114 vis) op Route 108/109/125, Sableye (gezonken schatten in Seafloor Cavern/wrak, nu Granite Cave), Greninja-lijn (Froakie, nu Safari), Inkay → Malamar staat er al; Sharpedo/Carvanha vaker.
- **Ground/Bug (7 elk):** Ground: Barboach/Whiscash/Gastrodon/Wooper staan er al; Sandygast staat er; Palossand erbij (strandzand). Bug: Wimpod/Golisopod, Dewpider/Araquanid, Masquerain staan er al; weinig extra nodig.
- **Niet-verkrijgbaar met zee-link:** **Tapu Fini** (Water/Fairy, mist en zee, past op Shipwreck Shoals/Whirl Island als mist-wachter), **Keldeo** (Water/Fighting mythical, zee-/watervlakte, Swords of Justice als wachter bij Whirl Island of de zeetempel), **Walking Wake** (Water/Dragon paradox, als oerzee-spook in Underwater of Seafloor Cavern), **Palkia** (Water/Dragon, ruimte-oceaan: past beter bij Spear Pillar/Meteor Falls dan op open zee). Panpour/Simipour zijn bewust weg. Geen enkele gewone Water-soort mist.
- **Tweede helft van de game:** De latere routes (Route 124–134, Underwater) hebben veel Water+Psychic/Ghost/Dragon. Het meest gemist: Fire (Slugma-lijn, Fuecoco-lijn) en Grass (Lotad, Tangela) op zee en een Steel/Fighting-element (Empoleon, Crabominable) bij de koude Ashfrost-kant (Route 134–136).

## 6. Kandidaten om weg te laten uit een eigen Grounded-Pokédex (Jordi kiest)

Weglaten via `P_FAMILY_*` in `species_enabled.h` (per familie; let op: een familie uitzetten verandert soortnummers/saveblock niet, maar alle verwijzingen in trainers/Spire/Stadium moeten dan weg). ROM-besparing = gemeten uit `pokeemerald.elf` (voorkant+achterkant+icoon+paletten+footprint+overworld+learnsets) + kreet (`cries/*.bin`) + ±260 B SpeciesInfo per soort; de beschrijvingstekst (±0,2 KB) en naamtabellen komen er nog bij. Een kreet is ±15 KB en weegt het zwaarst (kreten niet verlagen, zie CLAUDE.md).

| Groep | soorten (verkrijgbaar) | ROM-besparing | in trainerteams | in Spire | in Stadium-teams |
|---|---|---|---|---|---|
| A. Ultra Beasts | 11 (0) | ±182 KB (kreten 148, graphics 30) | 2 | 0 | 0 |
| B. Paradox-Pokémon | 20 (10) | ±338 KB (kreten 275, graphics 55) | 4 | 0 | 3 |
| C. Gen 8–9 legendaries/mythicals | 23 (9) | ±454 KB (kreten 341, graphics 101) | 3 | 2 | 2 |
| D. Gen 7 legendaries/mythicals (Tapus, Necrozma, Magearna e.d.) | 15 (4) | ±271 KB (kreten 207, graphics 57) | 2 | 1 | 1 |
| E. Vaak verguisde ontwerpen (mijn gok, al verkrijgbaar) | 16 (16) | ±183 KB (kreten 131, graphics 46) | 13 | 7 | 4 |

- **A. Ultra Beasts** gebruikt in: Buzzwole (1 trainers: BRENT); Pheromosa (1 trainers: BRENT)
- **B. Paradox-Pokémon** gebruikt in: Scream Tail (5 trainers); Flutter Mane (5 trainers, Stadium 1); Roaring Moon (2 trainers: AARON, ZINNIA, Stadium 1); Iron Valiant (1 trainers: DAVE, Stadium 1)
- **C. Gen 8–9 legendaries/mythicals** gebruikt in: Eternatus (Spire enc); Urshifu (2 trainers: MUSTARD, STADIUM_MUSTARD, Stadium 1); Zarude (1 trainers: STADIUM_SHY_GUY_GREEN, Stadium 1); Okidogi (1 trainers: GRUNT_AQUA_HIDEOUT_7); Terapagos (Spire enc)
- **D. Gen 7 legendaries/mythicals (Tapus, Necrozma, Magearna e.d.)** gebruikt in: Necrozma (Spire enc); Magearna (1 trainers: COLRESS_MAGMA, Stadium 1); Zeraora (4 trainers)
- **E. Vaak verguisde ontwerpen (mijn gok, al verkrijgbaar)** gebruikt in: Probopass (6 trainers, Spire pool, Stadium 2); Trubbish (1 trainers: BERNIE_1, Spire pool); Garbodor (7 trainers, Spire pool, Stadium 2); Vanillite (1 trainers: GEORGIA, Spire pool); Vanillish (Spire pool); Vanilluxe (6 trainers, Spire pool, Stadium 3); Stunfisk (2 trainers: BEN, HECTOR); Bouffalant (1 trainers: HORATIO, Spire pool); Klefki (6 trainers); Falinks (4 trainers); Pincurchin (5 trainers); Stonjourner (3 trainers); Dracovish (4 trainers, Stadium 2); Arctovish (2 trainers: BRAM, TIFFANY)

Let op: de Spire-pool/encounters en het Stadium worden gegenereerd (`spire_pool.py`, `pool.py`); na weglaten daar opnieuw draaien en teams in `trainers.party` aanpassen. Mega/Gmax/Ultra-Burst/Tera-bazen in de Spire (bijv. Ultra Necrozma, Terapagos) hangen aan hun basissoort.

Schatting totale ROM-ruimte nu: 3,25 MB vrij (CLAUDE.md). Let op: groepen C/D/B bevatten ook leden die al verkrijgbaar zijn en bewust zijn toegevoegd (Zarude, Ogerpon, Okidogi enz.); die weglaten is een grotere ingreep. Alle groepen A–D samen: ±1245 KB.
