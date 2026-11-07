# Silicobra (Uyuni) – ronde 3 (kleine correctie op ronde 2)

Jordi over ronde 2 (letterlijk): "bij 2 vind ik de zak wat te groot geworden, die lijkt nu 1 met de staart. Plus de kuif links kapt erg scherp af. Verder wel prima"

Bestanden: `silicobra_uyuni.png` (64×64, geïndexeerd, 15 kleuren, transparency=0), `silicobra_uyuni_raster.txt` (bron, met de hand bewerkt), `vel.png` (basis, ronde 2 en ronde 3 op 4× en 1×, licht en donker, plus referenties), `scripts/` (bouw, controle, vel).

## Wat ik deed
1. **Pekelzak kleiner en los van de staart.** De uitbolling rechtsboven van ronde 2 is teruggedraaid, en de opvulling tussen zak en krul ook. De rechterrand per rij (32–41) is nu 40-40-39-39-38-38-37-35-34-34. Dat is overal gelijk aan of kleiner dan ronde 1, rond in trapjes van 1–2, zonder facetten. Tussen zak en krul zit nu op elke rij minstens 1 px lucht. De zak raakt de krul nergens meer recht naast of boven elkaar, alleen nog op drie punten schuin via een hoek, steeds omlijning tegen omlijning. De glans linksboven, de donkere onderkant en de twee belletjes zijn gebleven; alleen de schaduwkant rechts is mee versmald.
2. **Kuif links loopt geleidelijk uit.** De uitstekende hoek bij het voorhoofd is weg. De omlijning loopt nu in een gebogen lijn (24,13) → (23,14) → (22,15)/(21,15) → (20,16) → (20,17) → het voorhoofd, zodat de laatste plaat lager en smaller wordt en zonder trede of verticale rand op de kop aansluit.

## Diff t.o.v. ronde 2 (`scripts/controle.py`)
| Zone | Alpha eraf | Alpha erbij | Kleur | Totaal |
|---|---|---|---|---|
| Kuif links (rij ≤ 18, x ≤ 24) | 4 | 0 | 2 | 6 |
| Pekelzak | 16 | 0 | 17 | 33 |
| Bevroren: oog, gezicht/snuit, korst en barstpatroon, voet, krul, kleuren en buitenlijn | 0 | 0 | 0 | 0 |
| **Totaal** | | | | **39** (budget ±40) |

Pixels: 981 (ronde 2: 1001). Het palet is ongewijzigd. Open randen 0, losse pixels 0.

## Eerlijk oordeel
- De zak is weer een apart onderdeel: op 1× en 4× zit er zichtbaar lucht tussen zak en krul, en hij is kleiner dan in ronde 1 én ronde 2 maar wel rond.
- De kuif sluit links nu met een boog aan op het voorhoofd; geen scherpe hoek meer.
- Al het andere is pixel voor pixel gelijk aan ronde 2.
- Zelf zie ik geen open zwak punt.

## Lessen
- Een zak naast een ander lichaamsdeel krijgt minstens 1 px lucht; achter het andere deel weglopen maakte er op 1× één vorm van (Jordi: "lijkt nu 1 met de staart").
- Een toevoeging boven op het silhouet (kuif) moet aan de uiteinden taps uitlopen tot op de oude omtrek; anders ontstaat er een uitstekende hoek.
