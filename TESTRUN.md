# Testrun Jordi – bevindingen

Jordi speelt de 1.0 (ROM `Pokemon_Ungrounded_1.0_testfix8.gba`, save blijft werken). Per bevinding: wat hij zag, wat we deden, status.
Status: ✅ opgelost · 👍 goed zo (geen actie) · ⏳ open · 💡 idee/later. Details van oplossingen staan in `CHANGELOG.md` onder [v1.0.0], "Testrun Jordi".

## Ronde 1 (12 okt): begin t/m Roxanne

### Speelgevoel en balans
| Wat | Bevinding | Status |
|---|---|---|
| Levelcurve begin | Mudkip te snel lv 8–9 (dubbele EXP door inhaal-EXP + hogere trainers). Inhaal-EXP is nu alleen vangnet (pas 9+ onder de volgende gym-ace); routes vóór Roxanne terug op de oude levels, daarna geleidelijk. | ✅ |
| Levelsprongen | Na Petalburg sprongen van 8–9 naar 12. Hele game per trainer gladgestreken (looprichting). | ✅ |
| Route 116 | Liep van 12 naar 15 door elkaar; nu 12 → 13 → 14 in looprichting. | ✅ |
| Johnson (6× Metronome) | Lv 15 te sterk (Lucario/Electabuzz), 2× verloren; nu lv 12. Kon in een dubbelgevecht belanden: van plek geruild met Joey (nu 3 Poochyena). | ✅ |
| Keccles 1 | Te hoog (19–21, vóór Roxanne te bevechten); nu 15, Salandit 17. | ✅ |
| Team vlak vóór Roxanne | Lv 13–16 met 6 Pokémon (veel gerouleerd, een paar white-outs); Mudkip nog niet geëvolueerd → geen inflatie meer. | 👍 |
| **Roxanne** | Gewonnen in 1 poging, "perfect". Elke starter heeft een counter (Sableye ↔ Torchic, Shuckle ↔ Treecko, Lileep ↔ Mudkip). Lileep's Recover-stall voelde logisch. Minccino's Sing maakte het verschil tegen Sableye en Nosepass; Super Fang tegen Shuckle. | 👍 |
| Roxanne's ace | Nosepass is de ace, niet Shuckle: levels omgedraaid (Nosepass 19, Shuckle 18). | ✅ |
| Sterke vroege wilde Pokémon | Emolga (Mini Forest, 10%, 428 BST) en Minccino (Technician) zijn sterk. Voorstel: laten staan (zijgebied = marge); evt. Emolga naar een 1%-slot. | 💡 |
| Shellos (Billy) | Harden + Recover was eindeloos rekken; Recover → Mud Shot. Recover mag, maar niet om vroege gevechten te rekken. | ✅ |
| AI-debuffspam | Keccles' Charmander deed 3× Smokescreen vóór Dragon Breath. Nu: een stat-verlaging scoort alleen zolang die stat nog niet verlaagd is. Uitzondering: eerste rivaalgevecht (Route 103), daar maakt de spam het winbaar. | ✅ |
| Pokémon zonder aanval | Ivan's Pyukumuku (Baton Pass gaf Leech Seed door) kon niets: + Counter. Alle trainer-Pokémon zonder aanval kregen er een (behalve grappen). | ✅ |
| Bullet Seed | Raakte maar 2×. Kansen zijn standaard Gen 5+ (35% 2×, 35% 3×, 15% 4×, 15% 5×); de power is wel verhoogd (30 per hit i.p.v. 25, gemiddeld ±93 i.p.v. ±77). Jordi: viel mee, niet te sterk. | 👍 |
| Self-Destruct mist | Alola-Geodude's Self-Destruct "raakte niet": miss door 1 Mud-Slap (accuracy −1). Geen bug. | 👍 |
| Leech Seed na wissel | Bleef hangen: Pyukumuku gebruikte Baton Pass (geeft het door, zoals in de echte games). Geen bug. | 👍 |

### Bugs
| Wat | Status |
|---|---|
| Ingang Toadstool Hollow niet te vinden (zag eruit als een boom); nu een zichtbaar pad. Ook de Wo-Chien-ingang. | ✅ |
| Speler/rivaal onzichtbaar na de rivaal-intro (May) | ✅ |
| Verkeerde pc-melding na het vangen ("sent to PC" terwijl er plek was) | ✅ |
| Dave (Route 104) stond 1 tegel te laag in zee | ✅ |
| SickBlik dubbel rond Petalburg Woods; tweede verwijderd | ✅ |
| SickBlik/Dave/Colress misten soms hun intro/thema | ✅ |
| Save corrupt na nieuwe ROM (savestate) → hersteld als .sav | ✅ |
| Relearn-knop zwart in "welke move vergeten?" na evolutie | ✅ |
| Briney's boot voer over een eiland in Route 105; nu eromheen | ✅ |
| Fish Judge (Dewford) alleen met Surf bereikbaar; verplaatst | ✅ |
| Madame Silk had een Cooltrainer-sprite; nu de Bard-sprite (Mauville) | ✅ |
| SickBlik (strand Route 104) blijft niet staan na het gevecht maar gaat de wereld verkennen | ✅ |

### Wensen en teksten (verwerkt)
TV-teksten Mom/Dad, pc's van May/Brendan, Galar-Zigzagoon, Birch achtervolgd door Jigglypuff, hoog-gras-tekst, tijdschriften, Spinda-DJ, winkelplanken, muziekman Oldale verplaatst, VS-intro Route 103, wilde muziek (Hoenn, Kanto vanaf badge 4), tekstvakken afbreken op zinnen, Wally-Ralts-gevecht in Petalburg, Fisherman-intro (Wailord-finale) en Magikarp-intro, L INFO-melding in wilde gevechten, items verplaatsen in MOVE POKéMON, itemmelding onderin. Allemaal ✅.

### Open / later
- ⏳ Jordi heeft nog een lijstje met mogelijke aanpassingen.
- 💡 Simulatie: bij Brawly komt een hoofdpadspeler ±0,7 boven de ace uit; nalopen als Jordi daar is.
- 💡 Emolga eventueel naar een 1%-slot.

## Ronde 2 (13 okt): Dewford en Granite Cave
| Wat | Bevinding | Status |
|---|---|---|
| Granite Cave wild | 1F stond nog op lv 6–13; nu 14–17 (1F), 15–18 (B1F), 16–21 (B2F), 15–20 (Steven). | ✅ |
| Sirfetch'd op lv 18 | SIR LEEK (ruil) houdt een Leek vast: 50% crit per treffer, dus 3 crits in één gevecht gaat snel. Vroeg, maar niet game-breaking (Jordi): zo laten. | 👍 |
| Pollen Season verborgen | Butterfree had Pollen Season als verborgen ability (niet te krijgen). Bij alle 8 soorten nu in slot 1/2; verder geen nieuwe abilities alleen in het verborgen slot. | ✅ |
| Romero (Dewford Gym) Detect-spam | Gymtrainers hadden een bijna willekeurige AI; nu slimmere AI, Combusken een echte moveset. | ✅ |
| AI van gymtrainers | Alle gymtrainers (gym 1–8, 39 in totaal) hebben nu de slimmere AI. | ✅ |
| Team vóór Brawly | Lv 17–19 (Butterfree, Shroodle, Cutiefly, Emolga, Tinkatink, Sirfetch'd), 3 van 6 gewisseld na Roxanne, zonder grinden en zonder Slateport. Brawly ace 23: 4–6 eronder, iets lager dan het doel (2–3). Uitslag afwachten. | ⏳ |
| Black Belt Cristian heet nu Chael | | ✅ |
