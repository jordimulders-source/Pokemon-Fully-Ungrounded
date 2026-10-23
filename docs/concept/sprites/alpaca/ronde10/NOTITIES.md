# Alpaca fase 1, ronde 10: nieuw silhouet ("geen schaap")

Jordi na ronde 9: "de alpaca is geen alpaca, het is meer een schaap." Ronde 10 tekent het silhouet opnieuw: lange nek, kleiner lijf, kop hoger. Van ronde 9 blijven alleen het palet, de omlijningstechniek en de twee bokshandschoenen (rijen overgenomen, Jordi vond ze goed). De referentiefoto is inspiratie, geen blauwdruk: alleen de herkenbare alpacakenmerken zijn overgenomen, verder blijft het gestileerd, simpel en schattig (Pokémon-filosofie, `FAKEMON_DESIGN.md`).

## Silhouetschetsen (`schetsen.png`)
Drie ruwe 64×64-schetsen naast de verkleinde, gespiegelde foto:
- **A rechtop:** de nek staat verticaal en de kop zit erbovenop, zoals op de foto. **Gekozen**, omdat de nek hier het duidelijkst het silhouet bepaalt.
- **B nek naar voren:** leest meer als een paard of een ezel.
- **C chibi:** de grote kop dekt de nek bijna helemaal af en neigt weer naar het schaap van ronde 9.

## Keuzes
| Punt (Jordi) | Ronde 9 | Ronde 10 |
|---|---|---|
| Lange nek | Kop direct op het lijf | Nek als wollige zuil: 7–9 px zichtbaar onder de kin. De nekrug loopt als één curve van het achterhoofd via een holle nek (x27) naar de rug (segmenten 4-2-2-2-2-1-1). Een wolnaad (V-lijn) scheidt de nek en borst van het lijf |
| Lijf kleiner | Wolbal 24 px breed, groter dan de kop | Romp 17 px zichtbaar, smaller dan kop en borst samen; de kop zit 10 px hoger |
| Vrijwel zwarte ogen | Zwart met blauwe reflectie | Bijna geheel zwart. Dichtbij 3×5 met één glanspixel linksboven en één donkerblauwe reflectiepixel rechtsonder; ver oog 2×4, smaller, vlak bij de neusbrug (3/4) |
| Vacht op het hoofd | Kuif als losse bol | Wollige kruin als pony over het voorhoofd (gekartelde onderrand met franjes tot boven de ogen); het gezicht is kort behaard in de vachttinten |
| Neus/snuit | Rond Eevee-gezicht | Korte snuit die linksonder uitsteekt, met een neusgat (K) en een gespleten bovenlip ('w'-vorm in de vachtomlijning) |
| Oren | Bananenvorm | Recht en puntig, de punt iets naar voren (links); het verre oor (links) is kleiner en zit in de schaduw, het dichtbije oor (rechts) heeft een roze binnenkant |
| Handschoenen | Goed | Rijen van ronde 9 ongewijzigd; de voorpoot staat nu gecentreerd boven de manchet |
| Vier poten | Ja | Ja: twee handschoenen (de verre kleiner en hoger) en twee achterpoten met een hak (de verre poot donkerder en 1 px hoger) |

Wol: een gekartelde buitenrand (bulten met inkepingen bovenop het lijf, aan de nekvoorkant en aan de onderrand), een rafelige schaduwgrens, een paar korte krulnaden in de haarrichting en lichte omlijning (V) aan de lichtkant. Licht valt van linksboven.

## Controle (checklist)
- [x] Tellen: 4 poten, 2 oren, 2 ogen, neus en mond (gespleten lip), geen staart (ontwerp).
- [x] Omtrek dicht: `bouw10.py` vindt geen randpixels zonder omlijningskleur.
- [x] Geen spiegeling: ogen, oren en poten zijn elk apart getekend, met een andere maat en tint.
- [x] Zwart-aandeel rand **0,53** (doel 0,35–0,6).
- [x] Rechte randstukken > 4 px alleen waar het mag: de onderkanten van de handschoenen en hoeven (die staan op de grond), de zijkanten van de handschoen (ongewijzigd uit ronde 9), de schenen van de achterpoten (5 px) en de borstonderkant tussen de voorpoten (5 px).
- [ ] Oppervlak **1248 px**, boven het doel van ±850–1050. Een lange nek en vier lange poten kosten oppervlak: Mudbray zit op 1080 en Ponyta op 1291. Het lijf is al 6 px ingekort. Verder krimpen kan alleen met een kleinere kop, en die maakt hem minder schattig. Voorstel: zo laten, tenzij Jordi hem kleiner wil.
- [x] 64×64; anim_front 64×128. Frame 2: kop, kruin en oren 1 px omlaag (een knikje), de nek blijft staan.
- [x] 16 kleuren, index 0 transparant. Het palet is gelijk aan ronde 9.
- [x] Met de hand: alle pixels staan als run-length-rijen in `bron/delen.txt`. Geen vormfuncties en geen automatische schaduw. Alleen de schetsen gebruiken PIL-vormen.

## Eigen oordeel
Het silhouet leest nu als alpaca of lama en niet meer als schaap: de nek en de holle nekrug doen het werk, ook op 1×. Zwakke punten:
- De oren zijn maar 3–4 px zichtbaar boven de kruin.
- De borst is nog vrij breed en wollig.
- Het oppervlak ligt boven het doel.

## Bestanden
- `anim_front.png`, `normal.pal`
- `schetsen.png` (foto en schetsen A/B/C)
- `compare.png` (foto, ronde 9, ronde 10, Mudbray, Girafarig, Mareep; 1× en 3×)
- `bron/delen.txt`: de handgetekende rijen, per deel van achter naar voor
- `bron/palet.txt`
- `bron/bouw10.py`: samenvoegen en controleren (oppervlak, zwart-aandeel, open randen, rechte stukken), met een dump met kolomnummers
- `bron/raster_f1.txt` en `bron/raster_f2.txt`
- `bron/schetsen.py` en `bron/vergelijk10.py`
