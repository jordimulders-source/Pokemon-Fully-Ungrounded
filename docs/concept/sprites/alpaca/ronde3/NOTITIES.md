# Alpaca ronde 3: viervoeter met bokshandschoenen (Fighting-starter, fase 1)

Feedback op ronde 2 (Jordi): "alpaca moet op 4 poten blijven staan, humor dan als 2 poten bokshandschoenen hebben, maar zorg wel dat het niet teveel Hitmonchan wordt, daarnaast is het nu geen duidelijke alpaca meer." Daarnaast zijn de zwakke punten uit ronde 2 meegenomen: te groot voor fase 1 en een zwevende achterste handschoen.

## Bestanden
- `anim_front.png` (64×128, geïndexeerd, index 0 transparant)
- `normal.pal`
- `thumbnails.png`: drie silhouetten.
- `compare.png`: ronde 1, ronde 2 en ronde 3 (f1/f2) naast Wooloo, Mareep, Stufful, Makuhita, Riolu, Clobbopus, **Hitmonchan** (de valkuil) en de drie Hoenn-starters. Vergroot en op 1×, in kleur en als silhouet.
- `bron/`: `sh bron/build.sh` bouwt alles opnieuw.
  - `alpaca3.py` maakt de vormen (`procbase.png`) met `shapelib.py`.
  - `alpaca3.seg` bevat de kop met de hand, via `segraster.py`.
  - `thumbs3.py` en `compare3.py` maken de vellen.

## Thumbnails
- **A** staat op vier poten, met de voorpoten óp de handschoenen zoals op hoeven.
- **B** is dezelfde houding met één handschoen omhoog naar voren.
- **C** ligt (kush, zoals een rustende alpaca) met de handschoenen voor zich.

**Gekozen: A als frame 1, B als frame 2.** C is het schattigst, maar verliest de lange hals en wordt in het zwart een liggende hond of vos. Bij A zie je meteen een alpaca/lama: lange wollen hals, banaanoren en een wolkenlijf op vier poten. De twee ronde handschoenen onderaan zijn de grap. In B breekt de opgeheven handschoen de omtrek zoals Mudkips vin.

## Ontwerp
- **Duidelijke alpaca:** viervoeter in driekwart naar links.
  - Een lange, dikke **wolhals** (drie bolletjes) met een smalle kop en een snoet erop.
  - **Banaanoren**, met de rode kwastjes aan de oorpunt (zoals de oorkwastjes in de Andes).
  - Een **wollig lijf** van met de hand geplaatste bolletjes met een geschulpte rand en schubboogjes (de Mareep/Wooloo-techniek). Een **wolstaartje**, en de achterpoten als stompjes met donkere hoefjes.
- **De grap / Fighting:** alleen de **twee voorpoten** dragen **rode bokshandschoenen** met een gouden polsband, en hij staat erop als op hoeven. Hij wordt geen mensachtige bokser: hij blijft een dier op vier poten (geen Hitmonchan; zie het silhouet naast Hitmonchan in `compare.png`). Fighting lees je verder aan:
  - de **wollen V-wenkbrauwen** boven grote ogen met glans;
  - het **vastberaden mondje**;
  - in frame 2 de **stoot**.
- **Frame 2:** de nabije voorpoot gaat omhoog en stoot de handschoen naar voren. De kop komt 1 px naar voren en omlaag, met boze oogleden en een open mond (schreeuw). Hij staat dan op drie poten.
- **Bombín-zaadje:** het **mini-bolhoedje** (een wolkuif met koepel en rand) blijft, kleiner dan in ronde 2.
- **Kleurendriehoek:** hetzelfde palet als ronde 2. De vacht is cacao, de wol wit met een lavendel schaduw, het accent rood met een beetje goud. Hij blijft de lichte starter van het trio.

## Paletindeling (zelfde indeling als ronde 2)
| index | onderdeel | kleur |
|---|---|---|
| 0 | transparant | #94cd9c |
| 1–4 | wol (lijf, hals, staart, kuif, wenkbrauwen) | #fffff6 #f6eee6 #cdc5d5 #837b94 |
| 5–7 | vacht (kop, snoet, oren, poten, hoefjes) | #de9c73 #b4734a #7b4129 |
| 8–10 | rood: handschoenen + oorkwastjes | #ff7b6a #e63939 #9c1831 |
| 11–12 | goud: polsbanden | #f6c541 #ac7b29 |
| 13 | mond binnenkant | #d54a5a |
| 14 | wit (oogglans, tandje) | #ffffff |
| 15 | omlijning | #101010 |

Recept: `{'wol': [1,2,3,4], 'vacht': [5,6,7], 'rood': [8,9,10], 'goud': [11,12], 'mond': [13]}`.

## check.py (`--stage 1`)
Geen FOUT. LET OP:
- *geen back.png / icon.png*: buiten deze opdracht.
- *rand zwart 0,589* (p90 0,578): bewust in-game-contrast (§0).
- *rand linksboven helderheid 0,227* (p10 0,262): de selout van de witte wol is mijn donkerste wolkleur (lavendelgrijs #837b94). Op witte wol mag die lichter: tint 3 als selout. Dat is een kleine aanpassing in de volgende ronde.

OK:
- **hoogte 47** (was 54); breedte 46; oppervlak 1102 (was 1384);
- 15 kleuren;
- schaduw 51 %;
- dithering 5,2 %;
- 13 losse pixels;
- verschil frame 1–2 0,38.

species_info: `.frontPicSize = MON_COORDS_SIZE(48, 48)`, `.frontPicYOffset = 3`.

## Checklist Pokémon-design
- [x] **Dier × idee × type:** alpaca (hals, oren, wol, viervoeter) × bokser-grap (handschoenen aan de voorpoten) × Fighting (frons, handschoenen, stoot).
- [~] **Type met ≥ 3 middelen:** de handschoenen, de V-wenkbrauwen, het rood en de stoot in frame 2. In frame 1 staat hij stil, dus de houding draagt minder dan in ronde 2. Dat is de prijs voor de viervoeter.
- [x] **Basisvorm:** een wolwolk met een hals erop en stompjes eronder. Geen realistische gewrichten.
- [x] **Eén iconisch kenmerk:** de handschoenen als "hoeven". Het bolhoedje is een klein tweede zaadje.
- [x] **Silhouettest:** zonder twijfel een alpaca/lama, met twee ronde bollen als voeten. Niet te verwarren met Wooloo (bol), Mareep (geen hals) of Hitmonchan (rechtop, mensachtig).
- [x] **Kleur:** wit + cacao + rood accent, met een klein goud tweede accent.
- [x] **Gezicht:** grote ogen met glans en wollen V-wenkbrauwen. Frame 2 is een karaktermoment.
- [x] **Vooruitwijzing:** het bolhoedje (bombín), de handschoenen (later de wraps van de lama en de luchadora) en de kwastjes (linten).
- [x] **Starters:** valt naast de 27 niet weg; de enige witte viervoeter met rode handschoenen.
- [x] **Zelfde dier bekeken:** Wooloo en Mareep worden een Pokémon door een vorm (bol, wolk) plus één twist. Hier zijn dat de wolk, de hals en de handschoenen.
- [x] **Gespriet:** egale vlakken, schubboogjes in plaats van ruis, 1 px omlijning.

## Wat ik zelf nog niet goed vind
- **Hoogte 47:** net boven de gevraagde 40–46. Eén pixel eraf kan door de hoefjes 1 px korter te maken.
- **De wenkbrauwen** lezen op 1× deels als een witte band onder de hoedrand. Ze kunnen een rij lager of dikker.
- **De binnenkant van de handschoenen** heeft wat rommelige donkere pixels: de duimlijn en de belichting van de procedurele vorm.
- **De wol** is in het midden nog wat druk met lavendel boogjes. De selout van de wol kan lichter (zie check.py).
- **De mond in frame 2** is klein (3×3).
- Nog te maken: back, icoon, shiny en de varianten.
