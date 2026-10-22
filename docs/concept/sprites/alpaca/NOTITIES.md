# Alpaca (Fighting-starter, fase 1): front-sprite

Bestanden: `anim_front.png` (64×128, 2 frames, 16 kleuren, index 0 transparant), `normal.pal` (JASC),
`compare.png` (naast Treecko/Torchic/Mudkip/Mareep/Skitty/Poochyena, GBA en in-game, vergroot en 1×),
`varianttest.png` (snelle proef: normaal / zwart / albino, de lijnen blijven staan),
`bron/compose.py` (maakt de sprite opnieuw: `python3 bron/compose.py`; `bron/gen.py` levert lijf, poten en staart).

## Ontwerp
- **Wolbol met een te grote kop:** rond wollig lijf, korte vachtpoten met donkere hoefjes, wolpluim als staart.
  De kop is groot (±45% van de hoogte) voor de schattigheid, zoals bij Torchic/Mudkip.
- **Kuif van krullen** over het voorhoofd (de echte "topknot" van alpaca's). De onderrand vormt een **V boven de ogen**:
  een wollige frons. Samen met de schuin afgesneden bovenkant van de ogen geeft dat de vechtersblik; de rest blijft knuffelbaar.
- **Andes-detail:** roze wollen **oorkwastjes** (pompons), zoals alpaca's en lama's in de Andes dragen. Ze krijgen een eigen
  ramp, zodat ze later in de cholita-lijn (bombín, kleurige stoffen) terug kunnen komen en per variant van kleur kunnen wisselen.
- **Gezicht en poten** in een warme kameel-/karameltint; de wol crème. Twee kleuren maken het silhouet leesbaar en geven de
  latere fasen (lama, cholita) een basis.
- **Frame 2 (actiepose):** kop omhoog en naar voren, **oren plat naar achteren** (zo laat een boze alpaca zien dat hij gaat
  spugen of schoppen), bek wijd open (roze binnenkant, één tandje), voorpoot opgetild om te stampen/trappen, lijf en staart iets omhoog.
- Driekwart naar links, licht linksboven, selout: linksboven de omlijning in de rampkleur (wol: tint 3, omdat de wol heel licht is;
  vacht: tint 7; kwastjes: tint 10), rechtsonder zwart (#101010, in-game-contrast, §0).
- Werkwijze: lijf procedureel (wolwolk van schijfjes op hele pixels, elke krul eigen glans), kop met de hand uit sjablonen
  (krullen, oren, pompons, gezicht, ogen), daarna één randpass voor de selout en een opschoonpass (losse pixels).

## Paletindeling (voor de varianten, §5)
| index | onderdeel | kleur |
|---|---|---|
| 0 | transparant | #94cd9c |
| 1–4 | **wol** (licht → donker; basis = 2) | #fff6de #f6deac #cdac7b #836262 |
| 5–7 | **vacht**: gezicht, oren, poten, hoefjes (basis = 6) | #f6c58b #cd8352 #834a39 |
| 8–10 | **oorkwastjes** (basis = 9) | #ff83ac #e62973 #941852 |
| 11–12 | **oog** (iris licht, iris donker) | #ac5a31 #522920 |
| 13 | mond binnenkant | #d55a6a |
| 14 | wit (oogglans, tandje) | #ffffff |
| 15 | omlijning, pupillen, mondlijn | #101010 |

Recept-vorm: `{'wol': [1,2,3,4], 'vacht': [5,6,7], 'kwast': [8,9,10], 'oog': [11,12], 'mond': [13]}`.
Let op: de hoefjes delen index 7 met de schaduw van het gezicht/de poten; aparte hoefkleuren per variant kan dus niet
(budget is vol: 15 kleuren gebruikt).

## check.py (`--stage 1`)
Geen FOUT. LET OP:
- *geen back.png / geen icon.png*: buiten deze opdracht (alleen de front).
- *rand: aandeel zwart 0,63* (Hoenn-GBA p90 0,58): bewust, de rechter-/onderrand is volledig zwart voor het in-game-contrast (§0, in-game Gen 3: 58%).
- *dithering 1,5%* (net onder p10): alleen een smalle schaakbordovergang op het lijf; meer maakte de wol rommelig.
OK: hoogte 48, breedte 46, oppervlak ±1190 (iets groter dan de Hoenn-starters, 780–970: de kop met kuif en oren), 15 kleuren,
licht boven −0,48, schaduw 37%, binnenlijnen zwart 3,4%, verschil frame 1–2 0,47.
De gecombineerde licht-x-meting geeft +0,12 (licht "van rechts"); dat is een meetartefact: per ramp gemeten komt het licht
van links (wol −0,15, vacht −0,59), maar de donkere vacht zit links (kop) en de lichte wol rechts.
species_info: `.frontPicSize = MON_COORDS_SIZE(48, 56)`, `.frontPicYOffset = 8`.

## Nog niet goed / open
- Het lijf is wat vlak en vlekkerig vergeleken met de kuif; de krullen van het lijf zijn subtiel (boogjes in tint 3).
- De zwarte kinlijn onder de kop is lang en zwaar.
- De poten zijn eenvoudige stompjes; de opgetilde poot in frame 2 leest als "stampen", niet als een echte trap.
- Back, icoon, shiny en varianten nog te maken.
