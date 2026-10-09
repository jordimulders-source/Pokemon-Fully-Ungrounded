# Levelcurve (9 okt)

Vraag van Jordi: door alle nieuwe trainers en grotere teams loopt een reguliere speler ver voor. Daarna (feedback): **de E4 rond lv 80, Steven ace 84, de sterkste superbosses op 100; grinden is een no-go; extra content is het alternatief voor grinden; variatie in teams moet worden aangemoedigd.**

## Ontwerp in één alinea
Het **hoofdpad alleen** brengt je zonder grinden net boven elk doel (ace van de volgende gymleider/E4/Steven). **Extra content** (zijgebieden, optionele trainers) geeft marge, of houdt een grotere rotatie van Pokémon op niveau. Daarvoor zijn er twee knoppen: **trainer-EXP 50%** (er zijn ±2100 trainer-Pokémon tot de kampioen) en **inhaal-EXP**: een Pokémon onder het ace-level van de volgende mijlpaal krijgt +100% EXP per level achterstand (max. ×10). Een verse vangst of een Pokémon die op de bank zat, is dus snel weer bruikbaar, zonder levelcap: erboven verandert er niets.

## Methode
Script: `python3 tools/grounded/levelcurve.py [--profile hoofdpad|compleet6|completionist] [--postgame]` (parsers in `levelcurve_data.py`).
- **Route:** het Emerald-verhaal in hoofdstukken (tot en met elke gym, E4, kampioen; met `--postgame` daarna alle post-game-trainers oplopend en de superbosses). Alle trainers op de kaarten (`scripts.inc`, geen rematches, één rivaalvariant). Trainers die nog te hoog zijn (water op vroege routes) schuiven door tot hun mediaan ≤ ace + 3.
- **Wild:** 6 wilde gevechten per kaart (gewogen naar de slotkansen), inclusief vangen.
- **EXP zoals de engine:** Gen 5 geschaald, Gen 5-verdeling met twee Exp. Shares (Birch vóór gym 1, Mr. Stone), `B_TRAINER_EXP_PERCENT`, inhaal-EXP (`src/caps.c`).
- **Profielen:**
  - *Hoofdpad*: alleen het verhaal, vast team van 6 (starter + 5 vangsten), EXP evenwichtig verdeeld.
  - *Alle content, 6*: plus alle zijgebieden vóór de E4 (Toadstool Hollow, Dojo/Towers, Fortree Jungle, Mangrove Mire, Rocket Hideout, Scorched Slab, Route 135/136, Beacon Isle, Ghost Ship, Shipwreck Shoals, Hermit Crater, Koraalkathedraal, Whirl Island, onderwater, Meteor Falls-tunnels, VR-kluizenaar).
  - *Alle content, rotatie van 12*: hetzelfde met 12 Pokémon (EXP over 12 verdeeld). Gemeten: het gemiddelde van de sterkste 6.

## Resultaat
Grafieken (scratchpad): `levelcurve_levels.png` (ace en teamlevel per profiel) en `levelcurve_verschil.png` (team − ace). Getal tussen haakjes = team (sterkste 6) − ace.

| Mijlpaal | Ace vóór | Team vóór | Ace na | Hoofdpad (6) | Alle content (6) | Alle content (12 rotatie) |
|---|---|---|---|---|---|---|
| Roxanne | 16 | 22.7 | 23 | 25.4 (+2.4) | 25.4 (+2.4) | 25.4 (+2.4) |
| Brawly | 22 | 26.4 | 26 | 28.1 (+2.1) | 28.3 (+2.3) | 28.3 (+2.3) |
| Wattson | 25 | 34.5 | 34 | 36.9 (+2.9) | 36.9 (+2.9) | 36.2 (+2.2) |
| Flannery | 29 | 42.3 | 45 | 48.8 (+3.8) | 49.0 (+4.0) | 48.0 (+3.0) |
| Norman | 35 | 45.2 | 47 | 49.7 (+2.7) | 49.9 (+2.9) | 48.7 (+1.7) |
| Winona | 43 | 52.6 | 55 | 57.8 (+2.8) | 59.5 (+4.5) | 57.3 (+2.3) |
| Tate & Liza | 49 | 62.0 | 66 | 69.8 (+3.8) | 69.8 (+3.8) | 67.7 (+1.7) |
| Wallace | 56 | 69.7 | 76 | 79.3 (+3.3) | 80.2 (+4.2) | 77.6 (+1.6) |
| E4 (Drake) | 66 | 73.5 | 81 | 84.6 (+3.6) | 85.1 (+4.1) | 83.5 (+2.5) |
| Steven | 70 | 73.7 | 84 | 84.7 (+0.7) | 85.2 (+1.2) | 83.7 (−0.3) |
| Superbosses | — | — | 100 | 100 (0) | 100 (0) | 100 (0) |

- **Vóór:** het team liep 7–14 levels voor op de gymleiders en 10–25 op de routetrainers.
- **Na:** het hoofdpad zit bij elke mijlpaal 1–4 boven de ace, ook bij Steven en de superbosses; nergens grinden. Alle content met 6 Pokémon geeft wat meer marge. Met een rotatie van 12 blijf je op de curve in plaats van ver erboven of eronder.
- **Zonder inhaal-EXP** zakt de rotatie van 12 weg (−5 bij Flannery, −20 bij Steven, −30 bij de superbosses): de inhaal-EXP is wat teamvariatie mogelijk maakt.
- **Waarom niet alleen levels omhoog:** met geschaalde EXP geeft een sterkere tegenstander ook meer EXP, dus de speler loopt mee. Een oplosser die alleen levels verhoogde, kwam uit op Roxanne 32 en de E4 op 99–100. Het gat zit in de hoeveelheid trainers.
- Gevoeligheid: zonder wilde gevechten of met 12 per kaart verandert er weinig; de inhaal-EXP trekt het recht. Wie alles met één Pokémon doet, zet die ver boven de curve: dat is een keuze van de speler.

## Wat is aangepast
1. **EXP** (`include/config/battle.h`): `B_TRAINER_EXP_PERCENT 50` (was vast 150%), en `B_GROUNDED_CATCHUP_EXP` met `B_CATCHUP_EXP_STEP 100` / `B_CATCHUP_EXP_MAX 900` (`GetGroundedCatchUpExp` in `src/caps.c`).
   - Het doel leest de ace rechtstreeks uit het team van de volgende gymleider; na badge 8 is dat Steven, na de Hall of Fame 100. Past Jordi een gymteam aan, dan schuift het doel vanzelf mee.
   - Wilde EXP blijft 100%.
   - Getest in de emulator: een Arceus lv 5 zonder badges kreeg na twee wilde gevechten ±×10 EXP (lv 5 → 6; zonder inhaal-EXP zou hij volgens de berekening lv 5 blijven).
2. **Trainerlevels** (schaalregel per hoofdstuk, alleen omhoog; `solve()` in het script):
   - Gewone trainers +r tot de mediaan van (team − ace) ≤ +3.
   - Gymleiders tot team − ace ≤ +1,5. Gymtrainers schuiven mee met hun leider, maar blijven max. ace − 2.
   - Story-gevechten tot ≤ +2,5. Zinnia (Sky Pillar) mocht daarvoor ook 3 levels omlaag.
   - E4 en Steven op Jordi's ankers.

   Totaal sinds het begin:

   | Hoofdstuk | Routes | Ace na |
   |---|---|---|
   | Roxanne | +6 | 23 |
   | Brawly | +6 | 26 |
   | Wattson | +8 | 34 |
   | Flannery | +12 | 45 |
   | Norman | +6 | 47 |
   | Winona | +17 | 55 |
   | Tate & Liza | +24 | 66 |
   | Wallace | +29 | 76 |
   | Victory Road / E4 | +28 | Sidney 78, Phoebe 79, Glacia 80, Drake 81 |
   | Steven | | 84 (team 81–84) |

   - **Meegeschoven:** rivaalvarianten en rematches `_2`–`_5` van gewone trainers (zelfde +r).
   - **Zijgebieden per regio:** Toadstool Hollow, Dojo/Towers, Fortree Jungle, Mangrove Mire, Rocket Hideout, Scorched Slab.
   - **Zijgebieden via de levelafbeelding van de routes** (oud → nieuw): Route 135/136 (35–39 → 44–49), Beacon Isle (41–54 → 51–68), Ghost Ship (48–53 → 62–67), Shipwreck Shoals (52 → 66), Hermit Crater/Koraalkathedraal (46–50 → 58–63), Whirl Island (46 → 58), onderwater (43–51 → 54–64), Meteor Falls 2R/tunnels/Draconid (42–54 → 52–68), VR-kluizenaar (60 → 77).
   - **Niet verschoven:** grap-teams (Ivan, Lyle, elk team met ≥ 10 levels spreiding), bewust lage teams, Magikarp, Trick House, Battle Frontier.
   - **Evoluties:** 165 + 175 Pokémon geëvolueerd waar het nieuwe level dat vraagt. Niet bij sleutelgevechten, Stadium-personages, Jordi's eigen teams, bijnamen, Eviolite of als de ability niet past. Stadium-pool/omroeper: geen diff.
3. **Post-game** (alles samengedrukt in 83–100, op de ace: nieuw = 83 + (oud − 40)/3):
   - Tao-eiland (46–53 → 85–87).
   - SS Tidal (44–51 → 84–87).
   - Pokémon Tower, Cerulean Cave, Chargestone Cave, National Park, Plasma Frigate, Nothing Island, Mega Forest, Tapu Isle (65–71 → 91–93).
   - Desert Underpass (91), Liberty Garden en Mirage Bazaar (94).
   - Paradiso Misty/Erika/Lorelei/Birch (95–96), Giovanni en Colress (95), Zinnia Delta (95).
   - Archie/Maxie-taakstraf 1–3 (93/95/97).
   - **Superbosses op precies 100:** Steven (Meteor Falls), Cynthia (Paradiso), Ghetsis (Tao), Archie/Maxie-taakstraf 4, alle gymleider-rematches `_5` en Wally VR_5. De andere rematches: `_2` 86, `_3` 90, `_4` 95.
4. **Gymgidsen** noemen de nieuwe ace-levels (23/26/34/45/47/55/66/76).
5. **Gehoorzaamheid:** zonder badges 15 (was 10); zie hieronder.

### Voorstellen (niet aangepast)
- **Wilde levels** zijn niet meegeschoven: laat in de game liggen wilde Pokémon ver onder de trainers (bijv. Route 128 lv ±44 tegen trainers rond 70). Dankzij de inhaal-EXP is een verse vangst snel bruikbaar, maar voor de immersie kunnen de wilde tabellen per hoofdstuk mee omhoog (zelfde +r, vooral vanaf Winona).
- **Wilde legendaries:** post-game lv 70/75 → 93/95 (zelfde afbeelding als de post-game-trainers). Story-legendaries (lv 50–60) → rond het ace-level van dat moment (±70–76). Dat raakt veel kaartscripts waar nu andere agents in werken, dus niet nu.
- The Spire staat los: rentals op vaste levels.

## Gehoorzaamheid (blijft erin, op vanglevel)
Sinds `B_OBEDIENCE_MECHANICS` GEN_8 kijken eigen Pokémon naar hun **vanglevel**. Doortrainen, inhaal-EXP en Rare Candies raken de regel niet; alleen vangen boven de grens, geruilde Pokémon en gifts.

**De Abra van Jordi's maat:** Abra komt alleen voor op Route 116, op lv 11–12, en die route is al vóór gym 1 bereikbaar. Zonder badges was de grens 10, dus een Abra van 11–12 was ongehoorzaam tot de eerste badge. Abra kent alleen Teleport, dus dat valt niet op. Pas als Kadabra (lv 16, vaak nog vóór Roxanne) echt aanvalt, zie je hem 'loafing around'. Na de Stone Badge (grens 20) luistert hij weer.

**Opgelost:** de grens zonder badges is nu **15**. Getest in de emulator: vanglevel 15 zonder badges gaf 8/8 keer gehoorzaam, met de oude grens 4/8.

**Andere vroege plekken:**

| Plek | Wild level | Bereikbaar met | Grens | Na de fix |
|---|---|---|---|---|
| Route 116 | 10–13 | 0 badges | 15 | binnen de grens |
| Rusturf Tunnel | t/m 14 | 0 badges | 15 | binnen de grens |
| Petalburg Woods, Route 104 | t/m 10 | 0 badges | 15 | binnen de grens |
| Granite Cave | t/m 15 | 1 badge | 20 | binnen de grens |
| Route 110/117 | t/m 15 | 2 badges | 30 | binnen de grens |
| Route 115 (land) | 30–50 | 0–1 badges | 15/20 | **bewust erboven** |
| Old Rod op Route 115 | 25–30 | 1 badge | 20 | **erboven** |

Gifts (Lileep/Anorith 20, Grimer 22, Kubfu 22, Castform 25) vallen binnen de grens. Route 115 is de bewuste uitzondering: daar is de gehoorzaamheid precies de rem.

## Opnieuw draaien
Na nieuwe trainers of routes: `python3 tools/grounded/levelcurve.py --postgame` (tabel per mijlpaal; met `--profile completionist` de rotatie). `solve()` geeft de nieuwe verschuivingen (met de huidige data 0–2 levels).
