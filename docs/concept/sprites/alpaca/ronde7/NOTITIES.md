# Alpaca fase 1, ronde 7: pixel-over van concept A volgens de spritingregels

Opdracht: de Gen 3-frontsprite opnieuw, nu als **pixel-over** van de vaste modeltekening (`docs/concept/ontwerp/alpaca/concept_A.png`, Wolvuist) en aantoonbaar volgens `docs/lessen/SPRITING.md` en de Dragonfly Cave-gids zelf. Feedback van Jordi op ronde 6: de handschoenen en de ogen zien er niet Gen 3-achtig uit (kijk naar Makuhita en Hitmonchan).

## Bestanden
- `anim_front.png`: 64×128, 4bpp geïndexeerd, 16 kleuren, index 0 transparant; frame 2 eronder.
- `normal.pal`: JASC-palet.
- `compare.png`: modeltekening, ronde 6, ronde 7 (frame 1 en 2) en Mareep, Growlithe, Makuhita, Hitmonchan en Eevee op 3× en 1×; onderaan de ogen op 6× naast Eevee, Pikachu, Teddiursa, Zigzagoon, Growlithe en Mareep.
- `bron/sprite.txt`: **de sprite zelf**, één teken per pixel, met het palet bovenaan (`TEKEN RRGGBB index rol`). Dit is het bestand om met de hand verder te bewerken.
- `bron/stap1_verkleind.txt`: de modeltekening verkleind tot 38×43 (alleen naslag, niet in de sprite gebruikt), gemaakt met `bron/verklein.py`.
- `bron/stap2_grof_v1.txt` en `bron/stap2_glad_v3.txt`: het grove silhouet en het gladgestreken silhouet (vlakke kleuren) uit de tussenstappen.
- `bron/render.py`: zet `sprite.txt` om naar `anim_front.png` en `normal.pal`. Het tekent niets zelf. `bron/compare.py` maakt het vergelijkingsvel, `bron/meet.py` de metingen.
- Opnieuw maken vanuit de repo-root: `python3 docs/concept/sprites/alpaca/ronde7/bron/render.py docs/concept/sprites/alpaca/ronde7/bron/sprite.txt docs/concept/sprites/alpaca/ronde7`.

## Werkwijze in stappen
1. **Verkleinen:** de modeltekening uitgesneden en verkleind tot 43 px hoog (`stap1_verkleind.txt`, ±900 px oppervlak). Dat raster was alleen de onderlegger: de dikke lijnen van de tekening geven ruis, dus er is niets van overgenomen behalve de verhoudingen.
2. **Grof (v1):** het silhouet met de hand over de onderlegger getekend, alleen omlijning en vlakke kleuren. Zoals de gids zegt: eerst inzien hoe rommelig het is. De nek was een lange bruine paal en de vuisten waren platte plakken.
3. **Gladstrijken per deel (v2–v3):** eerst de kuif (wolwolk met twee bulten boven en een inkeping links en rechts), dan de kop met de V-frons, dan de nek als wol (zoals in de tekening), dan de vuisten rond, dan de achterpoten.
4. **Kleur en schaduw (v4–v6):** per deel met de hand: eerst basis, dan hooglicht linksboven, dan schaduw, dan de omlijning per kleurgroep. In v5 de vuisten opnieuw naar het voorbeeld van Hitmonchan (zie hieronder), in v6 de verre vuist als eigen bol en één kuifrij weg voor het oppervlak.
5. **Frame 2:** in `sprite.txt` staat `FRAME2 27`: rij 27 (midden in het lijf, waar beide flanken recht lopen) valt weg en alles erboven zakt 1 px. De alpaca duikt in voor een stoot; de vuisten en poten blijven staan.

## De handschoenen (feedback Jordi)
Makuhita en Hitmonchan op pixelniveau bekeken (`anim_front_gba.png`):
- **Hitmonchan:** een handschoen is een **gladde bol**. Groot vlak basisrood, een sikkel hooglicht linksboven, een smalle sikkel schaduw (1–2 px) rechtsonder, omlijning in donkerrood aan de lichtkant en zwart aan de schaduwkant, en een manchet waar de arm erin gaat. Geen naden of vingers.
- **Makuhita:** dezelfde opbouw; de hand is vooral lichtgrijs met de schaduw onderaan.
- **Ronde 6 deed het anders:** wolbolletjes, vouwlijnen en veel donkere schaduwpixels. Daardoor oogden de vuisten als rode laarzen of als een hoop bessen.
- **Ronde 7:** de rode ramp volgt Hitmonchans vier stappen (licht → basis → schaduw → donkere omlijning), gedraaid naar het karmijnrood van de tekening. Beide vuisten zijn gladde bollen met een manchet waar de voorpoot erin zit en één zachte duimlijn in de schaduwtint. De verre vuist ligt deels in de slagschaduw van de dichtbije.

## Checklist SPRITING.md, regel voor regel
| regel | hoe toegepast |
|---|---|
| 1. Alles met de hand, geen vormgereedschap | Elke pixel staat in `sprite.txt`. Geen ellips, polygoon, automatische schaduw of omlijning; `render.py` zet alleen tekens om in indexen. |
| 2. Grof, dan per onderdeel gladstrijken | v1 grof, v2–v3 per deel glad (kuif, kop, nek, vuisten, poten), details (ogen, duimlijn, krullen) pas in v4–v6. Pixel-over op de verkleinde modeltekening, niet op een bestaande sprite als skelet. |
| 3. Lijnen en curven | Kuif links: segmenten 4-2-1-1-4 (oplopend, geen hoek); vuist links: 3-2-1-1-4-1-2-9; snuit: 6 horizontaal, 1 diagonaal, 2 verticaal, 1, 7. De inkepingen in de kuif zijn bedoelde wolplooien, geen hoeken in een curve. Niets gespiegeld: oren, ogen (4×4 tegen 3 breed), vuisten (andere vorm, grootte en schaduw) en achterpoten verschillen. |
| 4. Palet: 3 tinten + omlijning | Wol A/B/C + D, vacht k/K/m + M, vuist r/R/s + S, plus wit (oogglans), hoef-hooglicht en zwart. Wol volgt de opbouw van Mareep (hooglicht als grootste vlak), de vuist die van Hitmonchan, de vacht die van Growlithe. Geen extra verlooptinten. |
| 5. Licht linksboven | Hooglicht op de linkerbovenkant van kuif, wang, lijf en vuist; schaduw onder de evenaar en rechts. Slagschaduw in de schaduwkleur: kuif op het gezicht (rij m onder de kuif), kop op de hals (C), borst op de voorpoot (mmm), manchet op de handschoen, dichtbije vuist op de verre vuist. Ruim hooglicht (R/S). |
| 5b. Wol: gekartelde grens | De grenzen tussen A, B en C lopen in boogjes en treden, met korte krulplooien (C en D) onder de bulten; geen dithering gebruikt (de gids zegt spaarzaam; op deze maat bleek het niet nodig). |
| 6. Ogen | Bouw van Pikachu overgenomen (zie de oogrij op het vergelijkingsvel): dichtbij oog 4×4 met afgesneden hoeken, witte glans linksboven en een gekleurde reflectie (vachtschaduw) rechtsonder; ver oog 3 breed (`##` / `#w#` / `##m`). Geen 'brillenglazen' of poppenogen meer. |
| 7. Texturen | Wol als vacht behandeld (zie 5b); vuisten glad (geen wolstructuur meer, zie handschoenen). |
| 8. Omlijning per kleurgroep | Zwart aan de schaduwkant (rechts en onder), D/M/S (donkere tint van die kleur) aan de lichtkant, de schaduwkleur als omlijnings-hooglicht op de meest belichte randen (bovenkant kuif `DCCD`, bovenkant vuist `SsS`, snuit `DCCDDD`). Overal 1 px; lichtere pixels alleen binnen de lijn (lichte buitenrand 0,03). |
| 9. Formaat | 64×128, 2 frames, 16 kleuren, index 0 transparant; wol, vacht, vuist en hoef hebben eigen indexen (voor kleurvarianten). |

## Extra lessen uit de gids zelf (niet in SPRITING.md)
- **Volgorde van een pixel-over (Scyther):** eerst de omlijning volgen, en afwijken van de tekening waar dat een gladdere lijn geeft; dan vullen, dan de eerste schaduwlaag, dan pas de omlijning arceren. Zo gedaan: de snuit steekt in de sprite verder uit en de kuif is iets kleiner dan in de tekening, omdat de lijnen daar beter lopen.
- **'Realiseer je hoe rommelig het is' (Scorplack):** de grove versie is bewust lelijk gelaten en daarna pas gladgestreken; kleine details zijn uit de eerste omlijning weggelaten.
- **Neutrale segmenten:** pas nodig bij vormen vanaf ±6 px; bij grotere bogen meer dan één. Op de oogjes (4 px) dus geen eis, op kuif en vuist wel.
- **Liever een eenvoudiger helling dan een bobbel:** de bovenkant van de verre vuist is één rustige schuine lijn (4 + 3) in plaats van een golf.
- **Schaduw na de evenaar wordt niet donkerder:** voorbij de evenaar één schaduwtint; de extra donkere tint alleen voor de omlijning, niet als vierde vulling.
- **Revamp/splice-les:** als een deel een ander deel afdekt, moet de slagschaduw mee (verre vuist, voorpoot onder de borst).
- **Glans alleen waar het glanst:** alleen in de ogen; geen witte glimlichtjes op wol of vuist.
- **Overgang langs de omlijning (reactie van de schrijver onder de gids):** van zwart, via zwart met een basispixel binnen, naar omlijningsbasis, naar basis met een hooglichtpixel binnen. Toegepast langs de linkerkant van de vuist (S bovenaan, # vanaf de evenaar) en de kuif.

## Metingen (frame 1, `bron/meet.py`, met `keuring_ronde5/scripts/metrics.py`)
| | oppervlak | donkere rand (<60) | puur zwart aan de rand | detail | verzadiging |
|---|---|---|---|---|---|
| **alpaca r7** | **965** | 0,74 | **0,56** | 1,68 | 0,53 |
| Mareep | 893 | 0,57 | 0,57 | 1,65 | 0,53 |
| Growlithe | 1088 | 0,41 | 0,41 | 1,85 | 0,48 |
| Makuhita | 1142 | 0,57 | 0,52 | 1,63 | 0,52 |
| Hitmonchan | 1058 | 0,65 | 0,65 | 1,79 | 0,37 |

Puur zwart aan de buitenrand: **0,56**, binnen het Gen 3-bereik 0,35–0,6. De 'donkere rand' van de oude meting telt ook de gekleurde omlijning M en S mee (die zijn donker); daarom ligt die hoger. Oppervlak 965, net boven het doel van 950.

## Eigen oordeel
- **Beter dan ronde 6:**
  - De vuisten lezen nu als bokshandschoenen (gladde bol met manchet, Hitmonchan-opbouw) in plaats van als laarzen of bessen.
  - De ogen zijn echte kraalogen in Gen 3-formaat met glans en reflectie.
  - De wol is lichter en rustiger, met de grootste vlakken in hooglicht zoals Mareep.
  - De nek is wol zoals in de tekening.
  - De omlijning zit in het Gen 3-bereik.
- **Zwak:**
  - **Op 1×** blijven de twee rode bollen onderaan het meest opvallende deel; ze kunnen nog steeds als schoeisel lezen. Dat komt uit het ontwerp (vuisten op de grond). Eén vuist opgeheven in dekking blijft het advies uit ronde 6 (keuze voor Jordi).
  - De kuif oogt als een grote muts boven een klein gezicht; dat is de verhouding van de modeltekening.
  - De wolschaduw is nog in brede banden (vooral onder de kuif); Mareep heeft meer losse krulvlakken.
- Geen blinde test in deze ronde (niet gevraagd).
