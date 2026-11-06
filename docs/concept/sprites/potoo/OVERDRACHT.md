# Overdracht great potoo (7 nov) — prompt voor een nieuw gesprek

We gaan verder met de great potoo (fakemon voor Pokémon Fully Ungrounded, Ghost/Normal, één stage). Jordi stuurt in dit gesprek zijn eigen overtrek van kop, snavel en bek (gemaakt op `docs/concept/sprites/potoo/tekenbasis/leidraad_gespiegeld_spritepixelraster.png` of `leidraad_origineel_raster.png`). Die overtrek is vanaf nu de bron voor kop + snavel + bek: **1 op 1 overnemen, niets verzinnen.**

**Lees eerst:** `CLAUDE.md`, `docs/lessen/SPRITE_KERN.md`, `docs/lessen/SPRITE_WERKWIJZE.md` (incl. de potoo-lessen en de blinde test), `docs/concept/sprites/potoo/SPEC.md` (alle besluiten, Jordi letterlijk; lees de hele tabel "Ontwerp" en "Afgekeurd"), `potoo/referenties/GROTE_SNAVELS_STUDIE.md`.

**Vast (goedgekeurd):**
- Pose driekwart naar links, bek wijd open, onzichtbare tak, klauwen verborgen. Kop hangt voorover; achterkop/nek lopen in één boog door in de rug (geen knik, geen hals).
- **Lijf** ("lichaam is oké"): sprite `potoo/sprite/ronde3/` en poppetje `potoo/poppetje/ronde14_spritehoek.png`: rechtop, brede schouders, gevouwen vleugel met pennen, brede platte staart, schorspatroon.
- **Kopvorm** ("hoofdvorm is prima"): vormschets `potoo/sprite/ronde6_schets/` (volle hoge koepel, kaak/wang sluit aan op het lijf).
- **Oog:** op de plek en in de verhouding van de foto (niet meeschalen met de kop); puur zwart, geen glans, geen lichte rand. Fotopositie: `potoo/sprite/bekrand_overtrek/overtrek.json`.
- **Bekrand-overtrek van de leidraad** ("zeer netjes"): `potoo/sprite/bekrand_overtrek/`; hele vorm: `potoo/sprite/vorm_overtrek/` (Jordi vond de bovenkant van de snavel nog niet goed genoeg en trekt die zelf over).
- **Snavel:** de haak is het einde van de bovensnavel, één vorm ("de snavel is geen punt dat is onderdeel van de snavel").
- **Halsrand:** moet erin, puur met kleur en schaduw (roze lijn in `vorm_overtrek/`).
- **Kleur C2:** bijna wit met lila zweem, muil geestblauw/paars met diepte (donker achterin), schorsstreepjes (verhoogden de herkenning in blinde tests).

**Aanpak:**
1. Zet Jordi's overtrek in de spritemaat (64×64) op het lijf van ronde 3, met het oog op de fotopositie. Toon hem eerst die vormschets naast zijn overtrek (een tekenbasis mag door het keurslot met `<bestand>.tekenbasis.md`).
2. Pas na zijn akkoord: één sprite-maker kleurt met de hand (Game Freak-studie, SPRITE_KERN; geen script-kleuring), met de halsrand en de grote-snavel-lessen (eigen snavelkleur met outline, twee kaakdelen, opening als donkere holte, haak als einde van de bovenkaak).
3. Vóór Jordi: blinde test (agent zonder context, plaatje met neutrale naam in de scratchpad) en een onafhankelijke keurder. Jordi wil alleen iets zien als het echt op de bron lijkt; kort statusbericht, geen tussenplaatjes.

**Niet herhalen:** Blender/3D; snavel uit bollen of formules (pacman, zeehond, helm, schild, slabbetje, vizier); oog met lichte rand; gokken in plaats van overtrekken; Jordi's zinnen verkeerd lezen ("geen bol hoofd" = niet bol genoeg); per ronde Jordi lastigvallen.

Antwoord in het Nederlands, kort. Werk op de branch die het gesprek krijgt; commit en push na elk afgerond stuk.
