# Battle Stadium (Project Grounded)

Een Pokémon World Tournament (B2W2) op het Battle Frontier-eiland: toernooien van 32 tegen iconische
trainers uit de game en uit andere generaties. Teksten zijn placeholders; Jordi herschrijft.

## Kernregels (Jordi)
- **32 deelnemers**, enkelvoudige eliminatie: ronde van 32, 16, kwartfinale, halve finale, finale (5 gevechten voor de speler).
  NPC-tegen-NPC-wedstrijden worden gesimuleerd.
- **Alles level 50**: jouw team én de tegenstanders, omhoog én omlaag geschaald. Geen andere restricties (geen verboden soorten of items).
- **Singles 4v4**: jij kiest 4; de tegenstander neemt de 4 sterkste uit zijn team (de ace altijd).
- **Doubles 6v6 = multi battle**: jij (3) + een compagnon (3) tegen twee trainers (elk 3). Werkt als de tag battles van Sword/Shield en de Frontier.
- **Iedereen gebruikt zijn sterkste team** (laatste rematch / post-game-versie).
- **BP per gewonnen gevecht** (zie Beloning).
- **Bracket op papier vanaf de kwartfinale**: acht trainers met hun plaatje, wie tegen wie, winnaars lopen door naar het midden.
- **Nieuwe personages** in de game komen ook in de pool (staat in CLAUDE.md).

## Level 50 (wiskundig, v0.8.108)
Rekenscript (scratch `lvl.py`, 20.000 willekeurige matchups, schade-formule gen 5+, rolls 85-100%):

| EV's | level | gem. klappen tot KO | KO hangt af van de roll | OHKO |
|---|---|---|---|---|
| 0   | 50  | 3,76 | 55,3% | 5,7% |
| 0   | 100 | 3,90 | 57,0% | 5,1% |
| 85  | 50  | 3,94 | 58,6% | 4,3% |
| 85  | 100 | 4,10 | 58,4% | 3,8% |
| 252 | 50  | 4,34 | 63,7% | 2,2% |
| 252 | 100 | 4,53 | 64,5% | 1,6% |

De formule is bijna schaalvrij: vaste schade (Seismic Toss = level) is op beide levels ±30% van een
gemiddelde Pokémon. Level 50 geeft 4-5% kortere gevechten en 13-35% vaker een OHKO: iets meer
momenten waarop één klap het toernooi beslist. Dat is spannender, het is de toernooistandaard
(VGC, Frontier), en het onderscheidt het Stadium van de Spire (lv 100). **Besluit: level 50.**

## Pool
Bestaand (sterkste versie uit `trainers.party`): Hoenn-gymleiders, Elite Four, Wallace, Steven, Wally,
Archie, Maxie, Birch, Keccles, Colress, Zinnia, Mimi, Brock, Oak, Red, Gabby & Ty, Youngster Joey,
Brendan/May, Dave, Mitch en SickBlik (Jordi en zijn maten, Ace Trainers in Victory Road).
Geïmporteerd (v0.8.108, pokefirered en zo mogelijk DS-repo's): Kanto-gymleiders en Elite Four, Giovanni,
Blue, plus wat er uit andere generaties schoon binnen te halen is.
Gasten (`TRAINER_STADIUM_*`, klasse GUEST STAR): Wario, Yoshi (de huilende), Golbat en Grimer (gen 1), Boo, Mew,
vier Shy Guys (rood, groen, roze Fly Guy, zwart), de Burglar uit Red/Blue en Ditto (Youngster met een Ditto-gezicht,
praat alleen in puntjes en :), team uit Pokopia). Meme-trainers uit de game als Stadium-versie: Donald (zes Ditto),
Ivan (zeldzame visjes), Johnson (alleen Metronome), Thomas (Zangoose-familie); Joey en Winston met een eigen versie.
Intro's staan als trainer slide in `src/data/stadium_slides.h`, nederlaag/winst per trainer in `src/stadium.c`.

## Compagnons (Vampire Survivors-stijl)
- Start: **Brendan/May, Keccles, Wally**.
- **Onzichtbare puntenteller met drempels (Jordi, 5 okt):** 70 punten per uitgespeeld toernooi, +10 per gewonnen
  wedstrijd, +20 voor een titel (±100 per toernooi, singles of doubles). Drempels: de eerste compagnon bij 1 punt, daarna
  elke 100, dus ongeveer één nieuwe compagnon per toernooi. Volgorde van gewoon naar episch (teamsterkte + bonus voor
  kampioenen, E4, Frontier Brains en legendarische sets); de laatste vier: Cynthia, Red, THE WEATHER, THE CREATORS.
  Volledige volgorde onderaan `STADIUM_TEAMS.md`. Melding "NEW PARTNER!".
- Iedereen uit de pool kan compagnon worden (ook Archie aan jouw kant).
- **Collecties zonder trainer**: legendarische trio's en andere sets van drie die samen met je vechten:
  de Regi-geest (Regirock, Regice, Registeel), legendarische vogels, beesten, meertrio, Swords of
  Justice, Forces of Nature, Treasures of Ruin, Loyal Three, Creation-trio, en creatieve sets
  (starters, fossielen, Eeveelutions, ...).
- Compagnons zonder rugplaatje staan met hun voorplaatje naast je, zoals de Frontier-tag battles in Emerald.
- Collecties (`TRIOS` in pool.py, klasse "THE": "THE REGIS sent out Regirock!"), op punten: Mascots 1, Starters 3,
  Fossils 6, Eevees 10, Lake Trio 15, Regis 20, Birds 25, Beasts 30, Pseudos 35, Swords 40, Loyal 3 45, Tapus 50,
  Genies 55, Ultras 60, Treasures 70, Weather 85, Creators 100. Trainerfoto = voorplaatje van de eerste Pokémon.

## Beloning
BP per gewonnen gevecht: ronde 1-2 = 1, kwartfinale = 2, halve finale = 3, finale = 5 (totaal 12 per toernooi),
zoals de Frontier-faciliteiten (±1-3 BP per gevecht).
