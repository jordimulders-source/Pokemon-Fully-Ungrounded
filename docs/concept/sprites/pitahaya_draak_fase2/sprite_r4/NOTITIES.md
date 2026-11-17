# Pitahaya-draak fase 2, sprite r4 (maker): binnenvorm van de bek en de bovenlip

Twee versies: `pitahaya2_r4.png` (vanaf de r3-hoofdversie) en `pitahaya2_r4_lipB.png` (vanaf r3-lipB). Script: `maak_r4.py` (`--lipB` voor de variant). Per pixel staat in `*_afwijkingen.txt` wat er veranderde, met de modelmeting.
**Bewijs:** het script assert dat alle wijzigingen in de bek liggen (x 2–20, y 42–56), dat de diff erbuiten 0 is en dat het silhouet gelijk blijft. Palet ongewijzigd (12 + transparant; geen extra grijs nodig).
`vel.png`: r4 | lipB | model op 8×; bek op 12× (r4 | lipB | het model op zijn eigen natieve raster, zelfde uitsnede); onderaan 1× en 2× op licht en donker (links r4, rechts lipB).
Correctie r3: in `sprite_r3/NOTITIES.md` stond "(15,49) W → P". Die pixel is wit gebleven, en dat is juist (modelblok 6/9 vlees). Dat is nu aangepast.

## Wat is het omcirkelde vak (x 9–14, y 43–47)? Gemeten
Op het model (1024 en natief, 3×3 per spritepixel):
- **Linksboven, (9–13, 43–44) plus (10–11, 45): het gehemelte (binnenkant bovenkaak achter de tanden).** Grijs vlees, helderheid 184–190. Erboven ligt de zwarte kaaklijn met de tanden; rechts begrenst de zwarte lijn (14,44)–(16,44) het vak.
- **De onderrand van het gehemelte is de verre lip:** een diagonale roze strook (toon r (177,40,84)) met een donkere onderrand (d (113,43,55)). Die loopt van (9,45) via (10,46), (11,46) en (12,45) naar de zwarte lijn op (14,44).
  - Per blok: (10,46) 5 r + 2 d; (11,46) 4 r + 1 d; (12,45) 3 r + 2 d; (13,45) 4/9 roze (meerderheid vlees, blijft vlees).
- **Onder/rechts van de strook ligt de bovenkant van het vlees van de onderkaak, in de schaduw.** Grijs 187–197, dezelfde grijstint als het gehemelte, zonder aparte donkere band. Daaronder gaat het naar wit (≥ 218) via een smalle overgang van 1 spritepx (blokken 207–221 op rij 48), die al op de plek staat van het model.
- **Het model onderscheidt gehemelte en onderkaakvlees dus alleen met de verre-lipstrook en haar donkere onderrand, niet met een grijstint.** In r3 ontbraken (11,46) en (12,45), waardoor beide grijze vlakken één blok werden.
- **Pitjes in het vak:**
  - (44,11) ligt in het gehemelte; het modelblok heeft 4 pit-px, een duidelijke pit in het model → blijft.
  - (46,13) en (47,11) liggen onder de strook in het onderkaakvlees. Modelpitten van 2+1 px en 2 px, zichtbaar op het model (1024) → blijven.
  - Er is geen pit weggehaald.

## Wijzigingen
**A Bovenlip/kaaklijn (beide versies, 2 px).** Model: de rand onder de snuit is niet recht.
- Boven elke tand zit roze tandvlees. Op (4,42): 7 roze, 1 zwart, 1 vlees. Op (8,42): 6 roze, 3 vlees, 0 zwart.
- Tussen de tanden loopt de lijn zwart door, en achter de voorste tand zakt hij naar rij 43 ((7,43): 5 zwart).
- r2 had (4,42) en (8,42) zwart gemaakt. Ze zijn nu terug naar de modeltoon van het blok: K → r (roze gemiddelden (168,48,86) en (154,47,80)).
- De rij is nu K r K K K r K, met de tanden (4,43) en (8,43) onder het tandvlees en de lijn één rij lager op (7,43).
- Silhouet: het model geeft daar geen ander silhouet ((6,43) is 6/9 achtergrond, blijft transparant). Geen silhouetpixel veranderd.

**B Schaduw van de verre lip (alleen hoofdversie, 2 px).** (11,46) w → d en (12,45) w → d. Dat zijn de strookpixels waarin het model de donkere onderrand (113,43,55) heeft. Samen met (9,45) r, (10,46) r en de lijn (14,44) d / (15–16,44) K vormen ze een doorlopende diagonaal tussen gehemelte en onderkaak, in de schaduwtint en niet als felroze streep.
- In lipB zijn die twee pixels al r, de dominante strooktoon. Het model heeft onder de strook geen eigen schaduw ((12,46) en (11,47) zijn 100 % vlees), dus lipB krijgt alleen A.
- Verschil tussen de versies: alleen de tint van (11,46) en (12,45): d (schaduw) of r (strook).

Totaal: r4 4 px t.o.v. r3, lipB 2 px t.o.v. r3-lipB.

## Zelf bekeken
- Op 8×/12× leest het vak nu als gehemelte: grijze driehoek met één pit onder de tanden, afgesloten door een donkere diagonaal. Daaronder het grijze schaduwdeel en het witte vlees van de onderkaak.
- Op 1× is het verschil klein; het grijs blijft één tint, want het model heeft geen tweede.
- De bovenlip heeft nu tandvleesinkepingen boven de tanden in plaats van een rechte zwarte streep.
- **Zwak:** de diagonaal is 1 px en zit tussen pitjes. Op 1× valt de scheiding vooral op door de toon (d tegen grijs). Een tweede grijstint zou het verder scheiden, maar die staat niet in het model, dus niet gedaan.
