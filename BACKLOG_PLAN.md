# Backlog: plan van aanpak en vragen (voor Jordi)

Opgesteld 3 okt 2026. Per backlog-onderdeel uit `TODO.md`: wat er al is, mijn voorstel en de vragen die ik nodig heb vóór het bouwen. Beantwoord gerust kort ("1a, 2 ja, 3 Route 114"), dan begin ik.

**Vannacht al gedaan (kon zonder goedkeuring):**
- De Magikarp-transitie bouwt nu geleidelijk op en eindigt met een volledig gevuld scherm (v0.8.92).
- In `CREDITS.md` staan nu de graphics uit FRLG (Brock, Oak), de Red/Blue-ghost (pret/pokered) en MissingNo.

---

## A. Snel en goedkoop: legendaries die al in de game zitten

De eilanden uit Emerald staan al in de ROM en werken: **Faraway Island (Mew)**, **Birth Island (Deoxys, met de driehoekpuzzel; Deoxys krijgt van Jordi een ander event, zie Delta Episode)**, **Navel Rock (Lugia en Ho-Oh)** en **Southern Island (Latias/Latios)**. Ze zijn alleen bereikbaar met tickets (Old Sea Map, Aurora Ticket, Mystic Ticket, Eon Ticket) die in vanilla alleen via Mystery Gift te krijgen zijn. De boot vanuit Lilycove is al ingebouwd.

**Voorstel:** de tickets in de wereld verstoppen of laten verdienen. Dat is weinig werk en levert vier legendary-events op.

**Antwoorden van Jordi (3 okt):**
- Tickets voor **Mew (Old Sea Map)** en **Lugia/Ho-Oh (Mystic Ticket)** koop je in de **battle facility** (Battle Frontier, met BP).
- **Latias/Latios:** na het rivaalgevecht in Lilycove zegt de rivaal dat hij/zij twee tickets heeft gekocht; je mag er één kiezen. **Rood = Latias, blauw = Latios.**
- **Deoxys** krijgt een eigen event (zie Delta Episode), niet Birth Island.

**Oorspronkelijke vragen:**
1. Wil je deze eilanden gebruiken? Of liever eigen events voor deze legendaries (bijv. Latios/Latias "cryptisch kiezen", zoals in je backlog)?
2. Hoe krijg je de tickets? Opties: (a) van NPC's na bepaalde mijlpalen, (b) verstopt als zeldzaam item, (c) als beloning van een sidequest. Per ticket mag het verschillen.
3. Latios/Latias: in vanilla krijg je één van de twee als roamer (afhankelijk van je keuze op tv) en de ander via het Eon Ticket. Hoe zie je "cryptisch kiezen" voor je? Bijv. twee symbolen of raadsels op Southern Island, en de keuze bepaalt wie er komt (de ander post-game)?

## B. Regi-quest (Regieleki, Regidrago, Regigigas)

Al klaar: gevechtstransities voor alle Regi's, het Regi-heiligdom op laag 1 in Ashfrost (met de biddende oude vrouw), en de iglo als toekomstige ingang naar de Regigigas-grot. Regirock, Regice en Registeel staan nog op hun vanilla-plekken met braille.

**Voorstel aanpak:**
- **Regieleki:** grot bij Mauville (bijv. een nieuwe kamer via New Mauville of een grot langs Route 117/118). Kamerpatroon = het stippenpatroon uit zijn transitie.
- **Regidrago:** grot op Jagged Pass (verborgen ingang zoals de Magma Hideout). Kamerpatroon = vorkpatroon.
- **Regigigas:** grot ten noorden van Ashfrost, via de iglo. Opent pas als de vijf andere Regi's in je team zitten (zoals in DPPt).
- **Activatie** (jouw open punt), drie ideeën:
  - (a) Braille-puzzels zoals vanilla, met een nieuwe hint per grot.
  - (b) **Op de stippen staan:** de kamer heeft lichtgevende vloertegels in het oogpatroon van de Regi. Loop je ze allemaal af (of in de juiste volgorde), dan opent de deur. Dat is visueel en past bij de transities.
  - (c) Een Pokémon van het juiste type vooraan (Electric voor Regieleki, Dragon voor Regidrago) en dan Strength/Flash gebruiken in de kamer.

**Antwoorden van Jordi (3 okt):**
- Activatie **(b) op de lichtgevende stippen staan**. Dat vervangt de braille-puzzels en het "juiste Pokémon vooraan"-idee helemaal. De volgorde moet voor een mens makkelijk te snappen zijn.
- **Voorstel volgorde (nog bevestigen):** op de muur van elke kamer zit het oogpatroon van de Regi. De stippen op de muur lichten **één voor één op in een vaste lus** (zoals Simon Says). Loop de vloerstippen in dezelfde volgorde af. Een verkeerde stip laat alles doven en je begint opnieuw. Je hoeft niets te onthouden of te ontcijferen: kijken en nadoen.
- De **sneeuwtempel-tileset** (Ekat99) wordt de **Regigigas-grot bij Ashfrost** (via de iglo).

**Oorspronkelijke vragen:**
4. Welke activatie (a/b/c, of een combinatie)?
5. Waar precies bij Mauville en op Jagged Pass? Mag ik een plek voorstellen met een render?
6. Levels: Regi's op lv 50 zoals Suicune/Raikou/Entei, en Regigigas post-game lv 70?

## C. Overige legendary/mythical events (uit je lijst)

Per event een korte schets. Elk event krijgt een eigen transitie (zoals Suicune/Raikou/Entei) en een plek met verborgen ingang.

| Event | Voorstel | Vraag |
|---|---|---|
| **Jirachi** | Wens-event: een verlanglijstje of wensput in Fallarbor (meteorieten) of op Mt. Chimney's krater, alleen 's nachts. | 7. Waar en wanneer? |
| **Giratina** | Omgekeerde Sky Pillar: na Rayquaza verschijnt onder de Sky Pillar een gespiegelde toren die steeds dieper gaat (kaarten op de kop, andere kleuren); onderin Giratina. | 8. Hoeveel verdiepingen, met puzzels (bijv. zwaartekracht-/spiegeltegels) of alleen een tocht? |
| **Mewtwo** | Post-game, in een verborgen grot (Cerulean Cave-hommage), bijv. achter Meteor Falls of in de Safari-uitbreiding. | 9. Waar? |
| **Genesect** | Bij Devon/Rustboro (Devon-lab) of in het New Mauville-datacenter (past bij het thema). | 10. Datacenter of Devon? |
| **Raikou/Entei** | Gedaan (v0.8.80). | – |
| **Shiny Rayquaza** | Rayquaza op de Sky Pillar shiny maken (of een tweede, shiny Rayquaza post-game). | 11. De vaste Rayquaza shiny, of een extra event? |
| **Darkrai** | Mt. Pyre post-game: 's nachts een nachtmerrie-kamer (de speler valt in slaap bij de top), donkere kaart. | 12. Akkoord met Mt. Pyre-top 's nachts? |
| **Shaymin** | Bootticket naar een bloemenveld-eiland (nieuwe kaart met Gracidea). | 13. Nieuw eiland via de Lilycove-boot, zoals de andere tickets? |
| **Victini** | Victory Island-ticket: een gauntlet met nieuwe trainers door heel Hoenn, eventueel met keuzes. | 14. Hoeveel gevechten, en wat bedoel je met het keuze-element (route kiezen, team kiezen)? |
| **Kubfu** | Sidequest: een dojo (Dewford of Mt. Chimney-pad) met twee torens/proeven (Dark of Water), daarna evolueert Kubfu met de gekozen stijl. | 15. Waar, en hoe moeilijk? |
| **Delta Episode** | Post-game verhaal met Zinnia. **Jordi (3 okt):** vanaf Mossdeep (Space Center) word je de ruimte in geschoten en land je op een andere planeet, waar Deoxys zit. Landschap: Meteor Falls-tileset met paletswaps (geen ruimte-tileset beschikbaar). Zinnia-trainerfoto is omgezet (`graphics/grounded/trainers/zinnia/`). | 16. Hoe groot: een korte keten (5–8 scènes) of een echte episode met nieuwe kaarten? Muziek (Delta Emerald) moet je nog aanleveren. |
| **Heatran-gebied** | Post-game in Fiery Path/Mt. Chimney (niet de Entei-plek): een diepere lavagrot, cutscene is er al. | 17. Via een nieuwe ingang in Fiery Path? |

## D. Kaarten en gebieden

Grote brokken. Ik stel voor er één per keer te doen, met dezelfde werkwijze als Route 135/136 (bouwscript, render, emulatortest).

- **Oostkant interessanter:** meer eilanden en beter onderwater-exploreren op Route 124–134 (nieuwe Dive-plekken met kleine grotten/schatten, een paar eilandjes met trainers).
- **Jungle onder Fortree** (Ogerpon/Zarude): een nieuwe route of grot vanaf Route 119. Tileset: de bestaande Route 119-jungle plus extra bomen.
- **Swamp, fairy forest, mushroom forest, haunted house:** elk een eigen tileset. Ekat99-tilesets e.d. zijn hier niet te downloaden; die moet jij aanleveren (in de repo zetten, zoals de missingno.png).
- **Outer space vanaf Mossdeep:** koppelen aan de Delta Episode (Deoxys): lancering vanaf Mossdeep, landing op een planeet gebouwd uit Meteor Falls met paletswaps.
- **Safari Zone uitbreiden:** de twee extra zones uit Emerald (Route 121-uitbreiding) staan al in de ROM en gaan in vanilla open na de Hall of Fame. Goedkoop: eerder openzetten of uitbreiden met nieuwe soorten.

**Vragen:**
18. Welke als eerste? Mijn voorstel: de Safari-uitbreiding (bijna gratis), daarna de jungle onder Fortree.
19. ~~Tilesets aanleveren~~: staan in `graphics/grounded/tilesets/` (rotsen/lava, moeras, sneeuwtempel, tuin met meloenen). Welke hoort bij welk gebied (bijv. moeras = swamp, sneeuwtempel = Regigigas-grot)?

## E. Trainers en NPC's

- **Colress:** trainerfoto staat klaar (`graphics/grounded/trainers/colress/colress_front_pic.png`); de overworld-sheet is een JPG met ingebakken ruitjesachtergrond, een PNG is beter. Muziek "Battle! Colress" zit al in de game. Waar en wanneer moet hij verschijnen (20.)?
- **Red/Blue Burglar:** bedoel je de Burglar-trainerklasse uit Red/Blue (met hun teams), of Red en Blue zelf (21.)? De trainerfoto van **Red** staat al in de game (FRLG).
- **Gen 4+ trainersprites (Greenphx):** omzetten naar GBA (64x64, 16 kleuren) is goed te doen met een script, zodra de bestanden in de repo staan.
- **Gen 4/5-overworldsprites:** dat kan. Gen 4 gebruikt 32x32 met per richting een stilstaand frame en twee loopframes, hetzelfde formaat als de GBA (rechts = gespiegeld links). Per sprite is het reduceren naar 16 kleuren en een eigen palet. Ook hiervoor heb ik de sheets nodig (22.: welke personages eerst?).

## F. Moves: meer signatures

Voorstellen per soort (in de stijl van Seltzer Surge en dergelijke), elk eerst ter goedkeuring:
- **Cofagrigus, "Sarcophagus Slam"** (Ghost, fysiek, 80): Ghost-type Body Press. Gebruikt de eigen Defense in plaats van Attack.
- **Stunfisk, "Mud Trap"** (Ground, status): legt een verborgen val. Het volgende contactmove-raak tegen Stunfisk paralyseert de aanvaller en verlaagt zijn Speed.
- **Mightyena, "Pack Howl"** (Dark, status): +1 Attack voor het hele team (dubbels) of +1 Attack en +1 Speed solo. Past bij Joey's Poochyena-thema.
- **Wailord, "Whale Song"** (Water, special, 90, geluid): raakt alle tegenstanders, 30% kans op slaap. Of de grap-optie: een Water Spout die bij volle HP ook de gebruiker natspat.
- **Luvdisc, "Heartbreak"** (Fairy, special, 60): verdubbelt de kracht als het doel verliefd is, en maakt het doel daarna verliefd. Of iets droog-humoristisch passend bij Luvdisc' nutteloosheid.

23. Welke vind je goed, en wil je ze serieus sterk of met een knipoog?

## G. Battle Frontier

- **Nieuwe faciliteit:** (a) toernooi met bekende personages (gymleiders, rivalen, Birch, Keccles), of (b) roguelike: run met gehuurde Pokémon, na elk gevecht een keuze (nieuwe Pokémon, item, move), met permadeath. Dat past goed bij je Slay the Spire-filosofie.
- **Rental-teams reviseren:** de rental-Pokémon afstemmen op de gewijzigde soorten en moves.

24. Toernooi of roguelike (of allebei later)? Bij de roguelike: welk gebouw vervangen of erbij?

## H. Kleine open punten

- **Archie en Maxie** eventueel terug in de post-game (open uit de Sootopolis-ronde): als rematch, of als tag-partners (25.)?
- **Birch bij Ashfrost:** dialoog "veel smeriger". Dat is jouw humor; ik laat het bij de placeholder tot jij hem schrijft in de Dialoogstudio.
- **Ditto-trainer:** gepauzeerd, blijft staan.
- **PR naar `master`:** alles sinds v0.8.79 (Birch, Raikou/Entei, alle transities) staat op `claude/ecstatic-volta-kg8r32`. Zeg het, dan open ik de PR (26.).
