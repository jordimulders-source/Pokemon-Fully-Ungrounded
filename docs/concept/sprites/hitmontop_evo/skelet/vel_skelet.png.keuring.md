# Keuring: vel_skelet.png (stap 1, stick man van de pose)

Bron: `skelet/vel_skelet.png`, `skelet/optie_A.png`, `optie_B.png`, `optie_C.png`, `skelet/skelet.py`, `referenties/pose_eenhandsstand.webp` (gespiegeld, 790×845), `SPEC.md`. Eigen controle: alle gewrichten van `P` als cirkels op de gespiegelde foto gezet (op 790 px is 1 px op 64 ≈ 10,6 fotopixels; ±2 px ≈ ±21 fotopixels) en de 1×-optie's op 4× vergroot; posities op 64 nagerekend met `naar64`.

## Wat ik zag
- **8×:** A ligt netjes over de foto. Drie skeletten met dezelfde lezing: één rechte, verticale steunarm, schuin lijf, kop laag naast de arm, twee benen in een V als hoogste punten, koord omlaag van de heup. B is A met grotere kop en iets langer lijf (na herschalen wordt alles iets kleiner); C maakt de dijen bijna horizontaal en schuift de kop tegen de arm.
- **1×:** alle drie lezen direct als een omgekeerde Y / eenarmige handstand met benen in een V; de kop-cirkel is herkenbaar. De vrije arm is op 1× een klein driehoekje met een oranje stip eronder: leest als "iets voor de buik", niet storend.

## (1) Gewrichten van A op de foto
| Gewricht | Lijkt op / wijkt af in |
|---|---|
| hand, pols | lijkt op: handpalm plat, vingers naar voren (links). Binnen 1 px. |
| elleboog, schouder (steunarm) | lijkt op: arm recht en bijna verticaal; schouder op de onderrand van het shirt. Binnen 1 px. |
| nek, kop | lijkt op: kopcentrum en straal (48) passen op het hoofd; nek aan de cirkelrand. Binnen 1 px. |
| heup | lijkt op het kruis/de splitsing van de benen (440,325). De riem (vertrekpunt koord) zit lager, ±(455,370): ±4 px op 64. Voor het skelet prima; voor het koord zie hieronder. |
| knie1, knie2 | lijkt op: knikken in de wijde broek zijn niet scherp zichtbaar, de punten liggen plausibel op de lijn. knie2 mag ±2 px verder naar rechtsboven (±585,250); grensgeval. |
| enkel1 | **wijkt af**: ligt op de broekzoom (165,140), de echte enkel zit ±(130,125): ±3 px op 64. |
| voet1 | wijkt af in **richting**: op de foto is de voet geflexed en staat hij **verticaal** (hiel boven ±(80,50), tenen onder ±(60,205)); het skelet geeft één punt met een horizontaal stuk enkel→voet. |
| enkel2, voet2 | lijkt op: gestrekte voet in het verlengde van het onderbeen, voet2 = teenpunt. |
| vrije arm | lijkt op: schouder verborgen achter de borst (365,430 plausibel), elleboog steekt omhoog (345,330), onderarm over de buik, hand (425,458) klopt. Binnen 1–2 px. |
| koord | lijkt op in richting en lengte, maar begint bij `heup` in plaats van bij de riem (±4 px te hoog). |

## (2) Leesbaarheid op 1×
A, B en C: ja, eenarmige handstand met de benen in een V. C leest meer als een brede T/schaal dan als V (dijen bijna vlak); A en B houden de V van de foto.

## (3) Verhoudingen B en C als Pokémon-skelet (gemeten op 64)
- A: kop Ø 9,1 · romp 21,7 · been 31,8 · steunarm 22,7. B: kop Ø 10,8 · romp 23,9 · been 32,1 · arm 20,8. C: kop Ø 11,3 · romp 24,9 · been 33,4 · arm 21,7.
- Kop is in B en C ruim kleiner dan de romp: goed, en past bij "lijf langer dan Hitmontop". Met afrohaar wordt de kop ±14–16 px; dat blijft in verhouding.
- Benen ±1,35× de romp: past bij "langere benen" (verder dan Hitmonlee-achtig hoeft niet).
- **Marge:** het skelet is geschaald op 58 px en zit tegen de randen. Voeten (B): voet1 (5,3; 4,0), voet2 (58,7; 4,1); de hand (handpalmcentrum) op y = 62 met de grond op 63. Een ronde Hitmontop-hand (Ø ±5–6 px) rond y = 62 steekt onder het vel uit, en een blauwe klauwvoet van ±6–7 px heeft aan voet1-zijde net te weinig ruimte. Er is dus geen marge voor de onderdelen.
- De kop en lijf staan links van het midden (hand x ≈ 22); dat klopt met de foto (balans over de hand) en is geen fout.

## (4) Rare dingen
- Vrije arm: logisch (over de buik, zoals op de foto). De onderarm **kruist** de ruggengraatlijn; dat is anatomisch juist (arm vóór het lijf), maar bij het plakken moet de arm **boven** de romp liggen, niet erachter.
- De nek vertakt vanuit de steunschouder; voor een stick man prima, bij het plakken de romp van nek tot heup als één vorm bouwen (de nek is geen losse stok).
- C: de kop-cirkel komt bijna tegen de elleboog van de vrije arm en tegen de steunarm; de kop "plakt" aan de arm. Geen kruisende ledematen verder.
- Het vel zelf: de 2×-weergave en het onderschrift onder elke optie worden onderaan afgesneden (vel `W+150` hoog, nodig ±`W+185`). Alleen cosmetisch.

## NODIG (vóór stap 2, het plakken; geen nieuwe keurronde nodig)
1. **Marge:** B herschalen naar ±52–54 px (in `naar64` 58 → ±53) en zo verschuiven dat het handcentrum op y ≈ 59–60 ligt (ronde hand rust dan op de grond op 63) en de voetpunten ≥ 5–6 px van boven- en zijrand.

## POLIJSTEN
- enkel1 ±3 px naar (130,125) en voet1 als **verticale** voet (hiel boven, tenen onder) zoals op de foto; dat bepaalt hoe de blauwe klauwvoet geplakt wordt.
- Koord laten beginnen bij de riem (±(455,370)), niet bij het kruis.
- knie2 eventueel ±2 px naar (585,250).
- Vel iets hoger maken zodat 2× en onderschrift zichtbaar zijn.

## Advies
**Optie B.** Die houdt de V en de schuine romp van de foto (Jordi: "de perfecte pose"), met een iets grotere kop en langer lijf. C wint niets: de vlakke dijen maken er een T van, de kop plakt aan de arm en het brede skelet wordt kleiner geschaald. A is de referentie, maar de kop is daar te klein voor een Pokémon.

Oordeel: PASS
