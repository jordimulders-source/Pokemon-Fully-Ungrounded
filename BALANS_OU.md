# Balans t.o.v. Gen 9 OU (simulatie, 19 okt)

Alleen analyse; er is niets aan game-data veranderd. Gereedschap: `tools/grounded/balance/ousim.py` (gevechtsengine in Python), `ou_analysis.py` (setbouwer, ranglijst, teams), `ou_refs.py` (OU-referentiesets), `ou_report.py` (samenvatting). Ijking tegen de echte engine: `test/battle/grounded/balance_sim.c`.

## Methode

1. **Verschillen**: de repo-data (stats, types, abilities, learnsets, moves, typetabel) is vergeleken met vanilla pokeemerald-expansion **1.14.4** (dezelfde versie als de basis; de oudste commit hier bevat al Grounded-wijzigingen, dus vanilla komt van GitHub: `ou_analysis.py fetch <map>`). Voor "officieel" is de movepool uit alle games gebruikt (`all_learnables.json`, zonder Return/Hidden Power), voor de rom de echte learnsets (level-up + voorgangers + TM/tutor + egg; Return/Substitute zijn universeel).
   - Volledig geëvolueerd (667 vormen): 118 met andere stats, 45 met andere types, 139 met andere abilities; 56 keer is de verborgen ability naar slot 1/2 geschoven (o.a. Salamence/Gyarados Moxie, Ninetales Drought, Politoed Drizzle, Blaziken Speed Boost, Heracross/Pinsir, Kingler/Nidoking Sheer Force, Metagross, Froslass, Mawile).
   - 83 eigen moves, 57 vanilla moves aangepast (o.a. Thunder Wave 100%, Rock Slide 100%, Inferno 160, Zap Cannon 160, Steel Beam 100%), 11 eigen abilities, eigen weer (Acid Rain, Pollen Haze). De typetabel is gelijk.
   - Gewijzigde engine-regels die meetellen: Parental Bond slaat alleen boven 50% HP twee keer, Steelworker geeft het Steel-type, Moai Watch stapelt tot 3.
2. **OU-referentie**: 44 standaardsets van Gen 9 OU-dreigingen (Great Tusk, Kingambit, Gholdengo, Dragapult, Iron Valiant, Garganacl, Corviknight, Toxapex, Lando-T, Heatran, Zamazenta, Ogerpon-W, Raging Bolt, Samurott-H, Weavile, Slowking-G, Dondozo, Kyurem, Gliscor, …) **zonder Tera**. In de rom-dataset vallen niet-leerbare moves weg en vult de setbouwer ze aan.
3. **Simulatie** (`ousim.py`): Gen 5+-schadeformule met rollen, crits, accuracy, de belangrijke abilities/items, weer (incl. Acid Rain/Pollen Haze precies zoals in `battle_util.c`), terrein via surges, Tailwind/Trick Room/schermen, hazards, status, verwarring, setup, herstel, pivots, Regenerator, Moxie/Eelevate/Supreme Overlord, Desolate Land, en de competitief relevante eigen moves (Machine Learning, Twin Lance, Tyrant Horn, Queen's Weight, Joust, Rev Up, Straight Line, Totem Gaze, Pitcher Trap, Omen Strike, Colossal Claw, Flytrap, Kelp Shroud, Rolling Thunder, …). De AI kiest per beurt de actie met de beste "race"-uitkomst (wie haalt wie het eerst neer, met herstel meegerekend) en wisselt in teamgevechten als een ander teamlid de matchup wint.
4. **Score per soort**: een setbouwer maakt per ability 2–5 sets (Choice-aanvaller, Scarf, setup, bulky/herstel, Iron Defense+Body Press) en kiest de beste; score = winstkans in 1-tegen-1 tegen de 44 OU-referenties (10 gevechten per paar). Dat is gedaan voor vanilla (Showdown-legaal, ook verborgen abilities) en voor de rom (**speler-legaal: zonder verborgen ability**). Δ = rom − vanilla. 583 soorten.
5. **Ijking**: drie engine-tests (Galvanize-Exploud Boomburst, Ribombee's Bug Buzz in Pollen Haze, Weezing's Sludge Bomb in Acid Rain) geven precies de schade die de simulator voorspelt (±2 HP): `make check TEST_SRCS_IN="test/test_runner*.c test/test_test_runner.c test/battle/grounded/balance_sim.c"`.

**Beperkingen** (eerlijk): 1-tegen-1 bevoordeelt Choice-aanvallers en setup; hazards, pivots en Regenerator tellen daar niet. Geen voorspellen, geen Protect/Substitute-spel, geen Taunt/Encore/Trick, geen Tera. Niet gemodelleerd: Burrow Maze, Fungal Control, Transmutation, Praise Helix, Marionette, Implosion, Weather Report, Mimic Shade, Innard Punch, Lure Light, Sleep Clause-randgevallen; Nine Lives is een eenmalige Sturdy. De teamgevechten zijn vrij deterministisch (veel 0/100-uitslagen): lees ze als "wie heeft het betere plan tegen wie", niet als exacte percentages. Itemschaarste (Booster Energy/Scarf/Assault Vest liggen elk maar één keer) is genegeerd.

## Top 10 stijgers (speler-legaal, 1v1 tegen OU-referenties)

| Soort | Vanilla → rom | Wat het doet |
|---|---|---|
| Volbeat | 22% → 64% | Fire/Electric + Levitate, +55 BST (Sp. Atk +58): Tail Glow + Life Orb is een echte sweeper |
| Spinda | 17% → 57% | Normal/Fighting + **Pure Power**: CB Close Combat/Knock Off/Ice Punch |
| Wigglytuff | 33% → 72% | +45 BST en Specs Boomburst (+ Moonblast); OU-niveau |
| Linoone | 11% → 48% | +65 BST, Tough Claws, Straight Line |
| Kricketune | 13% → 45% | +100 BST, Technician (Twineedle) |
| Butterfree | 25% → 56% | **Pollen Season** (slot 2): Bug Buzz ×1,5, Speed ×2 in eigen weer |
| Masquerain | 37% → 68% | Bug/Water + **Drizzle** (slot 2), +30 BST: Specs Surf/Bug Buzz |
| Electrode | 41% → 72% | +65 BST (Sp. Atk +30) en Galvanize: Specs-aanvaller met 150 Speed |
| Farfetch'd | 16% → 46% | Fighting/Flying + Moxie, +76 BST |
| Parasect | 20% → 49% | Ghost/Grass, +60 BST |

Verder sterk gestegen en nu **OU-niveau** (≥ 65%, de mediaan van de OU-referenties is ±55%): Dusknoir 51→76% (Ghost/Dark + Iron Fist-punches), Hariyama 63→77% (Purifying Salt + Headlong Rush), Milotic 64→73% (Multiscale in slot 2), Vileplume 53→73%, Kangaskhan 55→71% (Parental Bond, ook na de 50%-regel), Wailord 44→70% (Unaware/Multiscale + Curse), Swalot 41→69% (Unaware), Weezing 49→66% (Air Pollution: CM + Will-O-Wisp + Recover), Aggron 46→68%, Armaldo 49→67%, Arbok 43→67%, Altaria 47→65%, Exploud 55→64% (Steel/Electric Galvanize), Swampert 58→64% (Regenerator), Sceptile 46→61% (Sharpness), Magcargo 40→62% (Desolate Land), Heracross 48→59% (Skill Link).

## Mogelijk te sterk

Ter vergelijking: de sterkste OU-referenties in deze meting zitten op 68–84% (Great Tusk 68, Kyurem 76, Lando-T 81, Ursaluna 84).

1. **Acid Rain-team** (Air Pollution + Merciless/Corrosion + Toxic Spikes): het sterkste rom-thema, 68% gemiddeld in de teamcompetitie (82% tegen OU-stall, 98% tegen Pollen, 90% tegen Zon). Oorzaak is een stapeling: in Acid Rain wordt elke vergiftiging *badly poisoned* (ook Toxic Spikes), gifkansen verdubbelen, Poison-types krijgen ×1,5 Def + 1/16 herstel, en **Merciless** (Tentacruel/Seviper/Toxapex) crit dan altijd. Voorzichtig voorstel: laat Acid Rain óf vergiftiging niet meer naar badly poisoned omzetten óf de gifkans niet verdubbelen (één van de twee), zodat Merciless niet bij elke klap crit vanaf beurt 2.
2. **Hariyama (Purifying Salt + Headlong Rush)** 77%: geen status, half Ghost-schade en 120 BP Ground als tweede STAB-achtige move. Als dit te veel blijkt: Purifying Salt terug naar het verborgen slot of Headlong Rush later in de learnset.
3. **Dusknoir (Ghost/Dark, +45 BST, Iron Fist)** 76%: Ghost/Dark heeft alleen een Fairy-zwakte; met 135/135 bulk en Iron Fist-punches wint hij veel 1v1's. Voorstel om te volgen, niet meteen ingrijpen.
4. **Multiscale/Unaware-bulk** (Wailord, Milotic, Swalot): Curse- of Calm Mind-sets winnen veel lange 1v1's. In teamgevechten minder dominant; geen ingreep nodig zolang Haze/Knock Off/Taunt beschikbaar blijven.
5. **Volbeat** (Tail Glow + Levitate + Fire/Electric): van 22% naar 64% is de grootste sprong; Tail Glow (+3 Sp. Atk) is daar de motor. Als het in de game te snel sneeuwbalt: Tail Glow later of alleen via de Move Relearner.

Niet te sterk gebleken (wel gestegen, maar binnen OU-bereik): Exploud-Galvanize, Salamence/Gyarados-Moxie, Blaziken-Speed Boost (slot 1), Kangaskhan, Machine Learning op de Iron-paradoxen (Iron Valiant/Crown/Moth +0–3%).

## Ondanks buffs nog onderaan (speler-legaal < 40%)

Furret 18% (Burrow Maze niet gesimuleerd; zelfs met +50 BST blijft hij laag), Shuckle 20%, Wugtrio 22% (Hole Up helpt pas in teams), Delcatty 23% (+90 BST maar Normalize), Shedinja 27%, Delibird 28%, Banette 28% (Ghost/Dark + Prankster; Marionette niet gesimuleerd), Ledian 28% (+65 BST, Iron Fist), Dustox 30%, Ninjask 31%, Beedrill 32% (+80 BST, Twin Lance), Persian 32%, Dugtrio 32–34%, Minun 32%, Luvdisc 33% (+83 BST), Sableye 34% (Rock/Ghost, +100 BST), Vespiquen 34% (Hive Queen), Marowak 35%, Spidops 35%, Mawile 38%, Sudowoodo 38%, Castform 40%, Corsola 40%. Voor de meeste is de oorzaak dezelfde: lage aanvalskracht of snelheid; hun nieuwe trucs (hazards opruimen, ontwijken, wissels) zijn teamwerk dat 1v1 niet beloont. Swellow daalde (39→30%): het verlies van de Normal-typing en Guts/Scrappy-Boomburst wordt niet goedgemaakt door Gale Wings.

## OU-dreigingen in deze rom

**Zwakker** — vooral omdat verborgen abilities niet te krijgen zijn en de TM-lijst kleiner is:

| Dreiging | Vanilla → rom | Oorzaak |
|---|---|---|
| Cinderace | 57 → 41% | Libero verborgen; geen Acrobatics |
| Meowscarada | 63 → 50% | Protean verborgen; geen Triple Axel/Low Kick |
| Moltres | 72 → 59% | Flame Body verborgen |
| Dragonite | 75 → 63% | Multiscale verborgen; geen Draco Meteor/Dual Wingbeat |
| Heatran | 53 → 45% | Flame Body verborgen; geen Overheat/Power Gem |
| Zapdos | 70 → 63% | geen Hurricane, Static verborgen |
| Corviknight | 47 → 40% | geen Body Press, Mirror Armor verborgen |
| Kingambit | 50 → 44% | geen Low Kick/Foul Play |

Ook in de rom niet leerbaar: Body Press (Garganacl, Zamazenta, Corviknight, Great Tusk), Draco Meteor (Dragapult, Kyurem, Raging Bolt, Hydrapple), Psyshock/Aura Sphere (Iron Valiant, Slowking-G), Ice Spinner (Great Tusk), Triple Axel (Weavile), Flip Turn (Alomomola), Pain Split (Rotom-W), Defog (Lando-T, Gliscor, Zapdos). Verborgen en dus niet verkrijgbaar: Toxapex-Regenerator, Gliscor-Poison Heal, Cinderace-Libero, Greninja/Meowscarada-Protean, Dragonite-Multiscale, Incineroar-Intimidate.

**Sterker**: Lando-T 71→81% (Hammer Arm i.p.v. Superpower houdt de Attack heel), Hydrapple 61→69%, Kyurem 72→76% (Focus Blast als dekking), Iron Valiant/Crown/Moth +0–3% (Machine Learning), Toxapex/Slowking-G/Samurott-H/Dragapult krijgen Scald of Seltzer Surge (in SV niet leerbaar). Nieuwe TM's die OU-dreigingen krijgen: Acid Rain (o.a. Toxapex, Pecharunt, Glimmora), Pollen Haze (Volcarona, Meowscarada, Hydrapple), Rolling Thunder (Cinderace).

## Teams (rom-legaal) en uitslag

Onderlinge competitie, 60 gevechten per paar (beide kanten beginnen even vaak):

| Team | Gem. winst |
|---|---|
| OU Offense | 74% |
| Zure regen / Acid Rain | 68% |
| Rom-toppers | 62% |
| Regen | 59% |
| Grounded-buffs | 44% |
| OU Balance | 42% |
| Stuifmeel / Pollen Haze | 35% |
| OU Stall | 34% |
| Zon / Heliotropism | 33% |

Opvallend: standaard-OU-offense blijft het sterkst, Acid Rain is het enige rom-thema op dat niveau. Pollen Haze verliest het weergevecht van elke langzamere weerzetter (Weezing/Pelipper zetten later en winnen) en de Fire-moves van Volcarona halveren in eigen weer. Zon/Heliotropism lijdt onder Sunflora's lage Speed buiten de zon en Water-teams. In deze AI-simulatie zijn de uitslagen extreem (0/100), dus de volgorde is betrouwbaarder dan de getallen.

Showdown-export (`!` = in de game niet verkrijgbaar):

```
=== OU Balance (rom-legaal)
Garganacl @ Leftovers | Purifying Salt | 252 HP / 252 Def / 4 SpD Impish | Salt Cure, Recover, Stealth Rock, Iron Defense
Great Tusk @ Booster Energy | Protosynthesis | 252 Atk / 4 Def / 252 Spe Jolly | Headlong Rush, Close Combat, Knock Off, Rapid Spin
Kingambit @ Leftovers | Supreme Overlord | 252 HP / 252 Atk / 4 SpD Adamant | Swords Dance, Kowtow Cleave, Sucker Punch, Iron Head
Gholdengo @ Leftovers | Good as Gold | 252 HP / 4 SpA / 252 Spe Timid | Nasty Plot, Make It Rain, Shadow Ball, Recover
Dragapult @ Choice Specs | Infiltrator | 252 SpA / 4 SpD / 252 Spe Timid | Dragon Pulse, Shadow Ball, Flamethrower, U-turn
Toxapex @ Black Sludge | Regenerator (! verborgen) | 252 HP / 252 Def / 4 SpD Bold | Surf, Toxic, Recover, Toxic Spikes

=== OU Offense (rom-legaal)
Glimmora @ Focus Sash | Toxic Debris | 252 SpA / 4 SpD / 252 Spe Timid | Stealth Rock, Mortal Spin, Power Gem, Earth Power
Iron Valiant @ Booster Energy | Quark Drive | 252 SpA / 4 SpD / 252 Spe Timid | Calm Mind, Moonblast, Focus Blast, Psychic
Roaring Moon @ Booster Energy | Protosynthesis | 252 Atk / 4 SpD / 252 Spe Jolly | Dragon Dance, Knock Off, Earthquake, Dragon Claw
Ogerpon-Wellspring @ Wellspring Mask | Water Absorb | 252 Atk / 4 SpD / 252 Spe Jolly | Swords Dance, Ivy Cudgel, Horn Leech, Knock Off
Kingambit @ Black Glasses | Supreme Overlord | 252 Atk / 4 SpD / 252 Spe Adamant | Swords Dance, Kowtow Cleave, Sucker Punch, Iron Head
Cinderace @ Heavy-Duty Boots | Libero (! verborgen) | 252 Atk / 4 SpD / 252 Spe Jolly | Pyro Ball, High Jump Kick, U-turn, Sucker Punch
(! 3× Booster Energy-achtige items in één team kan in-game niet: er ligt er maar één)

=== OU Stall (rom-legaal)
Toxapex @ Black Sludge | Regenerator (! verborgen) | 252 HP / 252 Def / 4 SpD Bold | Surf, Toxic, Recover, Haze
Corviknight @ Leftovers | Pressure | 252 HP / 168 Def / 88 SpD Impish | Brave Bird, Roost, U-turn, Defog
Blissey @ Heavy-Duty Boots | Natural Cure | 252 HP / 252 Def / 4 SpD Bold | Seismic Toss, Soft-Boiled, Thunder Wave, Stealth Rock
Gliscor @ Toxic Orb | Poison Heal (! verborgen) | 244 HP / 248 Def / 16 Spe Impish | Earthquake, Knock Off, Toxic, Protect
Dondozo @ Leftovers | Unaware | 252 HP / 252 Def / 4 SpD Impish | Curse, Wave Crash, Rest, Sleep Talk
Clefable @ Leftovers | Magic Guard | 252 HP / 252 Def / 4 SpD Bold | Calm Mind, Moonblast, Soft-Boiled, Fire Blast

=== Regen (rom)
Pelipper @ Damp Rock | Drizzle | 252 HP / 252 Def / 4 SpA Bold | Scald, Hurricane, U-turn, Roost
Barraskewda @ Choice Band | Swift Swim | 252 Atk / 4 SpD / 252 Spe Adamant | Liquidation, Close Combat, Throat Chop, Aqua Jet
Masquerain @ Life Orb | Drizzle | 252 SpA / 4 SpD / 252 Spe Timid | Quiver Dance, Hydro Pump, Bug Buzz, Ice Beam
Starmie @ Life Orb | Electromorphosis | 252 SpA / 4 SpD / 252 Spe Timid | Hydro Pump, Thunder, Ice Beam, Recover
Swampert @ Leftovers | Regenerator | 252 HP / 252 Def / 4 Atk Relaxed | Earthquake, Flip Turn, Knock Off, Stealth Rock
Kingambit @ Leftovers | Supreme Overlord | 252 HP / 252 Atk / 4 SpD Adamant | Swords Dance, Kowtow Cleave, Sucker Punch, Iron Head

=== Stuifmeel / Pollen Haze (rom)
Butterfree @ Silver Powder | Pollen Season | 252 SpA / 4 SpD / 252 Spe Timid | Sleep Powder, Quiver Dance, Bug Buzz, Energy Ball
Ribombee @ Silver Powder | Pollen Season | 252 SpA / 4 SpD / 252 Spe Timid | Quiver Dance, Bug Buzz, Moonblast, Energy Ball
Heracross @ Life Orb | Skill Link | 252 Atk / 4 SpD / 252 Spe Jolly | Swords Dance, Pin Missile, Rock Blast, Close Combat
Scizor @ Life Orb | Technician | 252 HP / 252 Atk / 4 SpD Adamant | Swords Dance, Bullet Punch, U-turn, Knock Off
Volcarona @ Heavy-Duty Boots | Flame Body | 252 SpA / 4 SpD / 252 Spe Timid | Quiver Dance, Bug Buzz, Giga Drain, Fiery Dance
Pinsir @ Choice Band | Moxie | 252 Atk / 4 SpD / 252 Spe Jolly | First Impression, Earthquake, Stone Edge, Close Combat

=== Zure regen / Acid Rain (rom)
Weezing @ Black Sludge | Air Pollution | 252 HP / 252 Def / 4 SpA Bold | Sludge Bomb, Will-O-Wisp, Recover, Toxic Spikes
Garbodor @ Black Sludge | Landfill | 252 HP / 252 Atk / 4 SpD Adamant | Gunk Shot, Drain Punch, Recover, Spikes
Tentacruel @ Black Sludge | Merciless | 252 HP / 4 Def / 252 Spe Timid | Sludge Bomb, Toxic, Rapid Spin, Knock Off
Nidoking @ Life Orb | Sheer Force | 252 SpA / 4 SpD / 252 Spe Timid | Sludge Wave, Earth Power, Ice Beam, Thunderbolt
Crobat @ Black Sludge | Corrosion | 252 HP / 4 Def / 252 Spe Jolly | Toxic, Roost, Brave Bird, U-turn
Glimmora @ Black Sludge | Toxic Debris | 252 SpA / 4 SpD / 252 Spe Timid | Stealth Rock, Mortal Spin, Sludge Wave, Earth Power

=== Zon / Heliotropism (rom)
Ninetales @ Heat Rock | Drought | 252 SpA / 4 SpD / 252 Spe Timid | Nasty Plot, Fire Blast, Solar Beam, Will-O-Wisp
Sunflora @ Life Orb | Heliotropism | 252 SpA / 4 SpD / 252 Spe Modest | Solar Beam, Earth Power, Sludge Bomb, Synthesis
Magcargo @ Leftovers | Desolate Land | 252 HP / 252 SpA / 4 SpD Modest | Shell Smash, Fire Blast, Earth Power, Recover
Blaziken @ Life Orb | Speed Boost | 252 Atk / 4 SpD / 252 Spe Adamant | Swords Dance, Flare Blitz, High Jump Kick, Knock Off
Scovillain @ Leftovers | Spicy Spray | 252 HP / 252 SpA / 4 SpD Modest | Fire Blast, Energy Ball, Leech Seed, Will-O-Wisp
Great Tusk @ Leftovers | Protosynthesis | 252 HP / 252 Def / 4 Spe Impish | Headlong Rush, Knock Off, Rapid Spin, Stealth Rock

=== Grounded-buffs (rom)
Exploud @ Choice Specs | Galvanize | 252 SpA / 4 SpD / 252 Spe Modest | Boomburst, Ice Beam, Focus Blast, Flamethrower
Salamence @ Life Orb | Moxie | 252 Atk / 4 SpD / 252 Spe Jolly | Dragon Dance, Outrage, Earthquake, Fire Blast
Kangaskhan @ Life Orb | Parental Bond | 252 Atk / 4 SpD / 252 Spe Jolly | Double-Edge, Sucker Punch, Earthquake, Drain Punch
Swampert @ Leftovers | Regenerator | 252 HP / 252 Def / 4 Atk Relaxed | Earthquake, Flip Turn, Knock Off, Stealth Rock
Porygon-Z @ Leftovers | Adaptability | 252 HP / 252 SpA / 4 Spe Modest | Nasty Plot, Thunderbolt, Shadow Ball, Recover
Sableye @ Leftovers | Prankster | 252 HP / 4 Atk / 252 SpD Careful | Will-O-Wisp, Recover, Foul Play, Knock Off

=== Rom-toppers (sim-top)
Hariyama @ Choice Band | Purifying Salt | 252 HP / 252 Atk / 4 SpD Adamant | Close Combat, Headlong Rush, Ice Punch, Knock Off
Dusknoir @ Leftovers | Iron Fist | 252 HP / 252 Atk / 4 SpD Adamant | Knock Off, Ice Punch, Earthquake, Will-O-Wisp
Milotic @ Leftovers | Multiscale | 252 HP / 252 SpA / 4 Spe Modest | Calm Mind, Surf, Moonblast, Recover
Wailord @ Leftovers | Multiscale | 252 HP / 252 Atk / 4 Def Adamant | Curse, Waterfall, Earthquake, Heavy Slam
Electrode @ Choice Specs | Galvanize | 252 SpA / 4 SpD / 252 Spe Timid | Thunderbolt, Focus Blast, Psychic, Volt Switch
Kangaskhan @ Life Orb | Parental Bond | 252 Atk / 4 SpD / 252 Spe Jolly | Double-Edge, Sucker Punch, Earthquake, Drain Punch
```

Alle moves en abilities zijn gecontroleerd tegen de rom-learnsets (`ou_analysis.load_teams`); niets onleerbaars, alleen de drie gemarkeerde verborgen abilities.

## Opnieuw draaien

```
python3 tools/grounded/balance/ou_analysis.py fetch <scratch>/vanilla
python3 tools/grounded/balance/ou_analysis.py rank <scratch>/vanilla <scratch>/rank.json --jobs 4   # ±60 min
python3 tools/grounded/balance/ou_report.py <scratch>/rank.json <scratch>/vanilla
python3 tools/grounded/balance/ou_analysis.py teams tools/grounded/balance/ou_teams.txt --n 60
```
(In een worktree eerst `tools/learnset_helpers/build/all_learnables.json` uit de hoofdcheckout kopiëren.)
