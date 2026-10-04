# Pokémon-balans: wie is te sterk, wie verdient een buff?

Analyse van de hoofdgame (Hoenn, badge 1 t/m Champion) met de encountertabellen, evolutielevels, learnsets en
gymteams van dit project. **Alleen voorstellen:** Jordi beslist. In de code is alleen één changelog-fout rechtgezet
(Marill, zie [Consistentie](#3-consistentie-changelog--code)).

Gereedschap: `tools/grounded/balance/` (zie [Methode](#5-methode-en-beperkingen)).

---

## Samenvatting

- **Geen enkele Pokémon veegt de hele game schoon.** In de simulatie veegt geen soort meer dan 2–3 van de 13
  grote gevechten (8 gyms, 4 E4, Steven) helemaal leeg. Een volledige sweep komt bijna alleen voor met een
  duidelijk typevoordeel: Roserade tegen Wallace's waterteam, Octillery/Staryu tegen Flannery. Dat is gewoon
  Pokémon. De gymteams (6 Pokémon, 31 IV's, coverage, Focus Sash, prioriteit, slimme AI) vangen een sweeper
  zonder typevoordeel meestal op. Drake en Steven zijn het lastigst: zonder setup haalt niemand meer dan 3 op rij.
- Het risico zit in **het middenstuk (Wattson, Flannery, Norman) en Sidney/Phoebe**. Daar winnen een paar
  vroeg te vangen soorten met setup of prioriteit vrijwel alles.
- **De grootste risico's:** Volbeat/Illumise (Tail Glow op lv 22), Linoone (Tough Claws + Extreme Speed bij de
  evolutie op lv 20, Belly Drum op 39), Octillery (Protean + coverage van bijna elk type, vanaf de Old Rod),
  Kricketune (Technician Pin Missile; een wilde Kricketune van 1% al vóór Roxanne) en een groep setup-soorten
  (Crawdaunt, Magcargo, Grumpig).
- **Opvallend in de data:** veel legendaries, mythicals en paradox-Pokémon staan als 1–4%-encounter in het wild,
  vaak vroeg (Jirachi, Kubfu, Scream Tail, Cosmog, Larvesta). En **verborgen abilities zijn voor de speler
  onbereikbaar**: geen Ability Patch, geen DexNav, en de Ability Capsule wisselt alleen slot 1 en 2. Een paar
  revisies zetten een kern-ability in dat verborgen slot (Kecleon Protean, Sandslash Tough Claws, Feebas
  Adaptability).
- **Buff-kandidaten:** vooral eindvormen die je vaak tegenkomt maar met weinig aanvallen of een nutteloze ability:
  Delibird, Lumineon, Luvdisc, Minun/Plusle, Beautifly/Dustox, Kecleon, Swellow, Delcatty, Cacturne,
  Lunatone/Solrock en Huntail/Gorebyss.
- **Consistentie:** de revisies in de changelog en de code komen vrijwel helemaal overeen. Er was één echt verschil:
  **Marill → Azumarill op lv 25** (v0.4.0), maar in de code stond nog lv 18. Dat is rechtgezet in een aparte commit.

---

## 1. Top 10: risico op "te sterk"

Fase = aantal badges dat je nodig hebt (0 = vóór Roxanne). Sim-scores: **"op rij"** = hoeveel Pokémon van een
gymleider hij achter elkaar verslaat met overgedragen HP; **"1-tegen-1"** = van hoeveel van de 6 hij vanaf volle HP
wint. Over alle 13 gevechten zijn dat maximaal 78. Een gemiddelde goede Pokémon haalt 35–45 1-tegen-1.

| # | Pokémon | Beschikbaar | Waarom | Sim | Voorstel |
|---|---|---|---|---|---|
| 1 | **Volbeat** (en Illumise) | Route 116, 1%, lv 12 (fase 0) | Electric/Fire, 105 SpA / 100 Spe, Levitate, **Tail Glow (+3 SpA) op lv 22**, Thunderbolt/Flamethrower via de Game Corner (fase 2) | Met setup **38 KO's op rij** (de hoogste van de hele dex): 5/6 tegen Wattson, Flannery en Norman; 6/6 tegen Sidney en Phoebe; 5/6 tegen Glacia | Tail Glow naar **lv 38–40**; op lv 22 Charge (of Work Up). Illumise hetzelfde. *Risico:* klein; ze blijven een beloning voor wie de 1% vindt |
| 2 | **Linoone** | Zigzagoon 20% op Route 101/102 (fase 0); evolueert op lv 20 | 485 BST (95/90/70/50/70/110), Tough Claws in slot 2, **Extreme Speed als evolutiemove** (80 BP, +2 prioriteit, ×1,3 ×1,5 = effectief 156 BP), Belly Drum op 39 | **Hoogste 1-tegen-1-score van de dex: 59/78.** 5/6 tegen Brawly op lv 22, 6/6 tegen Wattson en Flannery. Met Belly Drum 6/6 tegen Sidney en Phoebe | Extreme Speed van de evolutieplek naar **lv 34**; Belly Drum naar **lv 48** (niet tegelijk met ES vroeg in de game). *Risico:* Linoone wordt in fase 1–2 een gewone sterke Normal-type, wat prima is |
| 3 | **Octillery** | Remoraid, Old Rod Route 115, 30%, **lv 25–30** (fase 1; door gehoorzaamheid pas na badge 2 bruikbaar); evolueert op 25 | 120 SpA / 100 HP, **Protean in slot 1** en per level-up vrijwel elk type: Dark Pulse 28, Scald 32, Aura Sphere 34, Ice Beam 36, Flamethrower 38, Shadow Ball 40, Energy Ball 44, Flash Cannon 46, Dragon Pulse 50, Moonblast 52, **Aeroblast 58** | 1-tegen-1 **55/78**; 6/6 tegen Flannery (de zon niet meegerekend) en Tate & Liza | Gen 9-Protean (één keer per inzet) remt al flink. Voorstel: **de Old Rod-levels op Route 115 omlaag naar 15–20** (ook Ditto 25–30), zodat Octillery verdiend wordt; **Aeroblast eruit** (signature van Lugia); het coverageblok 4–6 levels later. *Risico:* klein |
| 4 | **Kricketune** | Kricketot 10% op Route 101 (fase 0); **Kricketune 1% lv 13 in Rusturf Tunnel**, dus al vóór Roxanne | Technician + **Pin Missile en Fury Cutter op de evolutie** (lv 18), 105 Atk / 95 Spe, Twineedle 40 | **25 KO's op rij** zonder setup (de hoogste); 6/6 1-tegen-1 tegen Roxanne op lv 16; 6/6 tegen Tate & Liza | De **wilde Kricketune van 1% in Rusturf weghalen** (een Kricketot of een andere soort ervoor in de plaats); Pin Missile naar **lv 22**. Past bij Jordi's eerdere nerfs (Twineedle 40, Fell Stinger 26) |
| 5 | **Crawdaunt** | Corphish 14% op Route 103 (fase 0); evolueert op 30 | **Adaptability + Shell Smash als evolutiemove**, 125 Atk, Aqua Jet 20 | Met setup 6/6 tegen Tate & Liza en Sidney | Shell Smash naar **lv 42** (evolutiemove wordt Swords Dance of Razor Shell). *Risico:* klein |
| 6 | **Magcargo** | Slugma 20% op Fiery Path (fase 3); evolueert op 28 | **Shell Smash als evolutiemove + Desolate Land in slot 2** (zware zon: Water-aanvallen werken niet), Recover | Met setup 6/6 tegen Flannery, 4/6 tegen Norman (de sim rekent het weer niet mee, dus eerder te laag) | Desolate Land is primal-niveau en in slot 2 voor iedereen haalbaar. Optie A: Desolate Land → **Drought** (Flannery's Magcargo krijgt dan Drought of een ander ace-thema). Optie B: zo laten als Flannery-signature. Shell Smash in elk geval naar **lv 40**. |
| 7 | **Grumpig** | Spoink 20% op Jagged Pass (fase 3); evolueert op 28 | **Simple + Tail Glow op 33 = +6 SpA in één beurt**; Calm Mind op 21 geeft +2/+2; Stored Power op lv 1 | Met setup 5/6 tegen Norman | Tail Glow → **Nasty Plot op 33** (met Simple +4) of Tail Glow naar 45. *Risico:* Grumpig blijft een Simple-setup-gimmick, maar niet meer meteen klaar |
| 8 | **Huge/Pure Power**: Azumarill, Spinda, Medicham | Marill 10% op Route 104 (fase 0, 50% Huge Power); **Spinda 20% op Route 113, altijd Pure Power**; Meditite 10% in Rusturf Tunnel | Verdubbelde Atk. Spinda: Victory Dance 28, Drain Punch 30, Close Combat 50, Bullet Punch / Aqua Step | Marill lv 22 wint 6/6 1-tegen-1 van Brawly; Spinda met Victory Dance 6/6 tegen Sidney en Drake | **Laten** (het is leuk en Brawly gebruikt hetzelfde). Wel opletten: Spinda staat op 20% en heeft Pure Power gegarandeerd. Eventueel **Victory Dance naar 40**. |
| 9 | **Vroege pseudo-legendaries** | **Beldum 4%+1% en Larvitar 1% in Steven's kamer, Granite Cave (fase 1)**; Gible 4% en Bagon 5% in Meteor Falls (fase 3); Jangmo-o 4% (kraterkamer); **Kommo-o 1% lv 42** in Meteor Falls 1F-2R (fase 5); Dreepy 10% op Mt. Pyre Summit | 600 BST-eindvormen, maar de evolutielevels zijn hoog (Metagross 45, Tyranitar 51, Garchomp 48, Salamence 50) | Middenmoot: het hoge evolutielevel remt ze genoeg af. Beldum-lijn met setup 6/6 tegen Sidney | **Laten**, op twee punten na: (a) Beldum is het post-game-cadeau van Steven en is nu al in fase 1 te vangen; kies één van de twee. (b) Een **volledig geëvolueerde Kommo-o** van 1% in fase 5 → Hakamo-o |
| 10 | **Wilde legendaries/paradoxen** | Jirachi 1% lv 35 Mt. Pyre Summit (fase 5); Kubfu 1% en **Scream Tail 4%** lv 40 Route 115 (fase 5); Cosmog 1% lv 15 Meteor Falls (fase 3); Sandy Shocks 1% Mirage Tower (fase 4); Larvesta 1% Fiery Path (fase 3) | Hoge BST, ver boven de route | Jirachi 6/6 tegen Sidney; Volcarona met Quiver Dance 6/6 tegen Sidney en 5/6 tegen Glacia | **Beleidskeuze:** 1% is een loterij en vaak leuk ("leave it, it's fun"). Wel: Scream Tail op 4% is te gewoon voor een paradox; naar 1%. Jirachi Fairy/Steel met Serene Grace op lv 35 in fase 5: liever post-game |

**Ook bekeken, laten zo:** Blaziken (Speed Boost gegarandeerd, maar middenmoot in de sim; starter), Golisopod
(Wimpod 4% Rock Smash Route 111: 6/6 tegen Tate & Liza, maar Emergency Exit is een echt nadeel), Gyarados
(Dragon Dance pas op 40), Heracross (Skill Link + Swords Dance, pas vanaf de Safari Zone, 1%), Shedinja (met
echte HP sinds v0.8.37, maar elke gymleider heeft een supereffectieve aanval: Knock Off, Aerial Ace, Flame Burst),
Lanturn (Tail Glow op 23; 6/6 tegen Flannery, maar daarna middenmoot).

**Vuistregel die uit de data komt:** een sterke setupmove (Tail Glow, Shell Smash, Belly Drum, Quiver Dance) vóór
lv ±35 op een soort die je vóór badge 4 kunt vangen, is de belangrijkste OP-bron. Daarna komen
prioriteit + boost-ability (Linoone) en "elk type STAB" (Protean met een brede learnset).

---

## 2. Buff-kandidaten (18)

Geselecteerd op: zwakke eindvorm in de sim (1-tegen-1 tegen E4 + Champion op lv 66; max 30), vaak te zien in
encountertabellen en/of door Jordi gereviseerd. Voorstellen zijn klein en in de stijl van de bestaande revisies.

| # | Pokémon | Probleem | Voorstel | Risico |
|---|---|---|---|---|
| 1 | **Delibird** (330 BST, 7 tabellen, o.a. Coldstep) | Learnset is alleen Present en Drill Peck | Learnset: Ice Shard 1, Ice Punch 15, Icicle Crash 30, Brave Bird 40, Freeze-Dry 45; Atk 55→85, Spe 75→95 (BST 380). Present blijft (grap) | Geen |
| 2 | **Lumineon** (460, 7 tabellen) | Geen echte aanvallen tot U-turn op 48 | Scald 26, Ice Beam 38, Hurricane 44 (wind past bij de vinnen); SpA 69→84 | Klein |
| 3 | **Luvdisc** (413, 6 tabellen; revisie "Tanky Medic") | 50 SpA, Triage heeft weinig om te versterken | SpA 50→70; Calm Mind op 30 (met Draining Kiss + Triage een echte "medic") | Klein |
| 4 | **Minun** (450) | Minus doet niets in singles | Volt Absorb naar slot 1 (Minus naar 2); Calm Mind op 22 in plaats van Copycat | Geen |
| 5 | **Plusle** (450) | Plus doet niets in singles | Nasty Plot op 25 in plaats van Fake Tears; Transistor blijft in slot 2 | Klein |
| 6 | **Beautifly** (405) | Rivalry is zwak; dunne bulk | Rivalry → **Pollen Season** (vlinder + stuifmeel, past in het weer-thema); HP 60→70 | Middel: Quiver Dance (20) + Pollen Season, maar met 405 BST nog breekbaar |
| 7 | **Dustox** (415) | Quiver Dance (20) zonder aanvalskracht (50 SpA) | SpA 50→75 (BST 440): een bulky Quiver Dance-mot | Klein |
| 8 | **Kecleon** (480; Keccles) | Color Change doet weinig; **Protean staat in het verborgen slot = onbereikbaar** | Protean naar slot 2 | Middel (Protean + Shed Tail), maar Gen 9-Protean werkt maar één keer per inzet |
| 9 | **Swellow** (435) | Gale Wings werkt alleen bij volle HP; 60/60/50 bulk | HP 60→70, Def 60→70 (455); Brave Bird 46→40 | Klein; daarna Winona's Swellow nalopen |
| 10 | **Delcatty** (490) | Normalize ×1,2, maar 65 Atk / 55 SpA en pas op 45 een sterke STAB | Atk 65→85; Body Slam op 25 (in plaats van Assist) | Klein |
| 11 | **Cacturne** (490) | Sand Veil in slot 1 (doet bijna niets); Water Absorb is verborgen | Sand Veil ↔ Water Absorb (Water Absorb naar slot 1) | Geen |
| 12 | **Solrock / Lunatone** (500/490) | Alleen Levitate; 30 Spe | Solrock slot 2: **Drought**, Lunatone slot 2: **Drizzle** (zon en maan/getijden; Tate & Liza krijgen er een weer-duo bij) | Middel: weer-setters zijn sterk, maar beide zijn traag |
| 13 | **Huntail / Gorebyss** (505/495; Clamperl in 11 tabellen) | Evolueren alleen met Deep Sea Tooth/Scale uit de Slateport-haven | Ook evolutie op **lv 30** (mannetje Huntail, vrouwtje Gorebyss); de items blijven werken | Klein |
| 14 | **Pelipper** (440) | Hurricane pas op 56; 60 HP | Hurricane 56→42; HP 60→70 | Klein (Drizzle in slot 2 blijft) |
| 15 | **Hypno** (513) | Forewarn in slot 1; Bad Dreams alleen in slot 2 | Slot 1 Insomnia of Bad Dreams naar slot 1 | Geen |
| 16 | **Farfetch'd** (453) | Na de Brawly-nerf (−10 Spe, geen Leek) weinig over | Leaf Blade op 30 (prei), Super Luck in slot 2 in plaats van Moody | Klein |
| 17 | **Feebas → Milotic** | Adaptability (Feebas) en de sterke ability zitten verborgen | Adaptability naar slot 2 van Feebas (niet bij Milotic) | Geen |
| 18 | **Sandslash** (505) | De revisie draait om de klauwen, maar Tough Claws is verborgen | Tough Claws naar slot 2 (Rough Skin naar verborgen) | Middel: Sandslash wordt dan een tweede Linoone-achtige (sim: 1-tegen-1 52 → ±57) |

Niet voorgesteld, wel gezien: **Wobbuffet** (learnset = Splash op elk level; een grap, en Shadow Tag + Counter
werkt los daarvan), **Castform** (de sim kan weervormen niet beoordelen), Banette, Golduck, Xatu, Tropius:
middelmatig maar bruikbaar.

**Algemeen voorstel (ability-slots):** verborgen abilities zijn voor de speler onbereikbaar (geen Ability Patch,
`DEXNAV_ENABLED` = FALSE). Gereviseerde soorten met een sterke ability alleen in dat slot: Volbeat (Prankster),
Sandslash (Tough Claws), Carvanha/Sharpedo (Speed Boost), Makuhita/Hariyama, Mawile, Bagon en Trapinch (Sheer
Force), Gyarados, Mightyena, Pinsir en Heracross (Moxie), Feebas (Adaptability), Roserade (Technician), Sigilyph
(Tinted Lens), Cacturne en Chinchou (Water Absorb), Venomoth (Magic Guard), Kecleon (Protean). Trainers kunnen
ze wel gebruiken. Keuze: zo laten (bewust "alleen voor trainers"), een **Ability Patch** als dure beloning
(Battle Frontier-BP of The Spire), of per soort het slot verplaatsen (zie #8, #11, #17, #18).

---

## 3. Consistentie changelog ↔ code

Gecontroleerd met `tools/grounded/balance/consistency.py`: types, abilities, base stats, level-up learnsets
(`gen_9.h`) van alle ±225 revisieblokken, het type-overzicht uit `[0.2.0-TYPES]` en de evolutielevels uit `[v.0.4.0]`.

**Rechtgezet (aparte commit):**
- **Marill → Azumarill: lv 18 → lv 25.** In `[v.0.4.0]` staat "Marill -> lvl 25"; de code had nog de vanilla-18.
  Bijwerkingen om na te lopen: op Route 117 (Surf) zit een wilde Azumarill van 1% op lv 18–22 (dat mag zo blijven,
  maar is nu "te vroeg geëvolueerd"), en één trainer-Azumarill op lv 20 (`trainers.party` r. ±9609). Een Marill op
  lv 33 (r. ±26752) had al geëvolueerd moeten zijn (een grap?).

**Geen echt verschil (latere changelog-secties gaan voor):**
- Koffing/Weezing: Levitate → Air Pollution (v0.8.53). Venomoth: Tinted Lens → Pollen Season (v0.8.54). Spoink
  Psychic/Normal (v0.5.1). Parasect: Fungal Control erbij, Spore op 1 en 22 (v0.8.45). Galar Zigzagoon zonder
  Leer (v0.6.67). Vibrava → Flygon op 38 (v0.4.0, dat de 40 uit de revisie overschrijft).
- Moves die later bewust aan learnsets zijn toegevoegd (Pollen Haze, Transmutation, Chilly Reception, Shadow
  Siphon, Acid Rain, Implosion) en de bekende tikfouten uit v0.5.0/v0.5.1 (Nature Madness, Lear, Pure Pulse).
- Losse controles van latere wijzigingen klopten ook: Shuckle, Swellow, Kricketot/Kricketune, Emolga,
  Pollen Season-dragers (en de voorgangers zonder), Air Pollution (Trubbish/Garbodor), Hoenn-Grimer/Muk.

**Alleen de volgorde wijkt af (geen effect op het spel, wel in de Pokédex):** de typevolgorde van Loudred,
Exploud, Sableye, Volbeat, Doduo, Dodrio, Anorith, Armaldo, Venomoth en Farfetch'd, en de ability-volgorde van
Parasect (slot 1/2 omgedraaid; wilde Pokémon krijgen willekeurig één van de twee). Niet aangepast.

---

## 4. Andere bevindingen uit de data

- **Route 115 en Route 118: het gras is alleen met Surf te bereiken** (gecontroleerd met `reach.py`). De hoge
  levels daar (Chansey/Blissey, Scream Tail en Kubfu lv 40) zijn dus fase 5, niet fase 1. Maar de **Old Rod op
  Route 115 (Ditto en Remoraid lv 25–30)** is al na badge 1 bereikbaar.
- **Gehoorzaamheid kijkt naar het level waarop je hem ving** (`B_OBEDIENCE_MECHANICS` Gen 8+): 10 + 10 per badge.
  Wat je vroeg vangt en zelf traint, gehoorzaamt altijd, dus overleveling is geen probleem voor de game. Statics in de
  kraterkamer (lv 20–22, fase 3) gehoorzamen meteen.
- **Rare Candy's:** ±17 in de hoofdgame, een paar al vroeg (Petalburg City, Granite Cave B2F, Route 110). Dat
  versterkt vroege setup-soorten (Volbeat lv 22, Linoone lv 20).
- **Drake en Steven** zijn in de sim de lastigste gevechten: zonder setup haalt geen soort meer dan 3 op rij.
  Brawly, Winona en Wallace worden alleen met een duidelijk typevoordeel geveegd (Swellow tegen Brawly, Roserade
  tegen Wallace). De curve klopt aan het eind; de piek in "te makkelijk" zit bij Wattson, Flannery, Norman en Sidney.

---

## 5. Methode en beperkingen

**Scripts** (`tools/grounded/balance/`, hergebruiken `tools/grounded/spire/spiredata.py`):
- `balancedata.py`: fase per kaart en methode (Old Rod 1, Good Rod en Rock Smash 3, Surf 5, Dive 7, Super Rod 7,
  Waterfall 8), cadeaus en statics, evoluties volgens de levels van dit project, TM-fase per vindplaats en
  gymbeloning, het inlezen van `trainers.party`.
- `calc.py`: schade (Gen 5+-formule, gemiddelde roll, STAB, type, abilities zoals Huge/Pure Power, Technician,
  Sharpness, Strong Jaw, Tough Claws, Adaptability, -ate, Protean (Gen 9), Truant, Simple, Speed Boost, Levitate en
  absorbs, Thick Fat, Multiscale, Fluffy, Filter; items van trainers) en sweep-simulatie.
  - `calc.py rank [--setup] [--1v1]`: ranglijst. `calc.py mon SOORT [--setup] [--slot 1]`: per gym een tabel met
    schade heen en terug en wie sneller is. `calc.py dmg ...`: één berekening.
- `underpowered.py`: zwakke eindvormen + aantal tabellen + of ze gereviseerd zijn.
- `reach.py KAART RICHTING`: welk gras te voet bereikbaar is.
- `consistency.py [--learnsets] [--order]`: changelog ↔ code.

**Aannames:** speler-IV 20, geen EV's, neutrale nature, geen item; level = het ace-level van de volgende gym
(16/22/25/29/35/43/49/56, E4 66). De speler kiest de beste ability uit slot 1/2 (Ability Capsule). Moves: level-up
(ook van de voorgangers t/m hun evolutielevel) plus TM's/HM's die in die fase te krijgen zijn; geen egg- of
tutormoves. De trainer gebruikt steeds zijn sterkste aanval.

**Beperkingen (de sim is bedoeld om te vergelijken, niet om exact te voorspellen):** geen weer/terrein (Drought,
Desolate Land, Pollen Haze, Acid Rain), geen status, geen crits, geen wissels of AI-trucs van de gymleider, geen
hazards, geen items voor de speler, Focus Sash alleen tegen enkele treffers. "Setup" = één boost-beurt tegen de
eerste tegenstander. Soorten die via macro's zijn gedefinieerd (Mothim, Vivillon e.d.) ontbreken in de
spire-parser. Stone-evoluties krijgen de fase van het eerste te vinden item. Gebruik de cijfers als rangorde; de
voorstellen hierboven zijn ook met de hand nagekeken in de learnsets en encountertabellen.
