# Gnometrotter Rock – sprite r2 (23 nov)

Basis: r1 (`../sprite/`), zelfde gedeelde reductie, silhouet (diff 0 t.o.v. r1), onderdelen en palet. Lever: `gnometrotter_rock.png`, `gnometrotter_rock_8x.png`, `vel.png` (r2 | r1 | model op schaal 8×; 1× licht/donker; naast Gnomini/Gnomad). Tussenstap vóór de omlijning: `stap1.png`.

## Wat er veranderde (reparaties 1–6), alles uit het model
- **Facetten** (`facetten.py`): het model in vlakken geknipt langs zijn eigen lijnen (41 facetten; controle `facet_full.png`). Elke spritepixel hoort bij het facet dat zijn modelvlak het meest bedekt. Facetgrenzen = 1 px naad op de pixel met de meeste modellijn (gemeten plek). Facetten < 6 spritepx gaan op in hun buur, naadstompjes < 3 px weg.
- **Baard (1):** lichtgrijze facetvlakken met middengrijze facetlijnen (tint 4) op de modelnaden; buitenrand 2/zwart; hoekige onderrand uit het silhouet.
- **Ruis onder de muts (2):** losse stukjes en 1 px-uitlopers van lijf/haar/muts tussen baard, neus en haar R gaan naar het omringende onderdeel (22 px, lijst hieronder); geen losse donkere vlekjes meer.
- **Lijf (3):** de naden tussen de roze rotsplaten als binnenlijn in donkerroze 6 (25 naadpx in het lijf).
- **Benen (4):** naden tussen de blauwe stukken in donkerblauw 9.
- **Muts/rugkam (5):** meerderheidsfilter 5×5 binnen het facet (2 rondes): grote vlakken in 3 tinten (3/4/5), alleen de modelbreuklijnen.
- **Volume (6):** lijf = één bol (buik, zonder het gezicht) licht linksboven: 15 hooglicht, 8 licht, 7 schaduwsikkel; slagschaduw 7 onder muts/neus/baard/haar en op het gezicht onder de muts (zoals het model). Benen: één bol per been (split bij het kruis, kolom 34): 11 / 10 / 9.
- **DC-omlijning opnieuw** (`dc.py`, zelfde regels als r1): buitenlijn outline base aan de lichtkant, zwart aan de schaduwkant; binnenlijnen nooit zwart (behalve de vaste boog rond neus/handen en de gesp); 2 px om-en-om gelijkgetrokken; outline highlights 7 px.

## Afwijking (`tel.py`)
| zone | anders t.o.v. kaal / zone | anders t.o.v. r1 | waarvan naad |
|---|---|---|---|
| muts+rugkam | 171 / 436 | 93 | 9 |
| haar L | 29 / 31 | 5 | 0 |
| haar R | 26 / 34 | 8 | 0 |
| baard | 91 / 179 | 68 | 9 |
| neus | 24 / 60 | 2 | 0 |
| lijf | 191 / 297 | 162 | 25 |
| arm L+hand | 41 / 74 | 8 | 4 |
| arm R | 18 / 32 | 0 | 0 |
| hand R | 25 / 64 | 1 | 0 |
| riem | 91 / 201 | 47 | 5 |
| stok | 65 / 101 | 34 | 0 |
| broek/benen | 227 / 361 | 163 | 10 |
| zool L | 46 / 56 | 17 | 0 |
| zool R | 51 / 55 | 24 | 2 |
Totaal 1096 / 1981 t.o.v. kaal (vooral lijn 1 px, facetvlakken en volume; lijf/benen zijn bewust herkleurd: "kleur mag afwijken"), 632 t.o.v. r1. Silhouet t.o.v. r1: 0.

## Pixels die niet rechtstreeks uit het model komen
- Volumetinten lijf en benen (regel, geen vorm): alle vlakpixels van lijf en broek/benen.
- Onderdeelkaart opgeschoond (22 px): (37,20) (37,21) (38,21) muts→lijf; (38,14) (37,15) (32,18) (41,18) haar R→muts; (20,36) (21,36) (25,36) (26,36) lijf→baard; (22,37) (23,37) lijf→riem; (18,16) muts→neus; (31,17) (31,18) (26,19) (26,20) (27,20) lijf→muts; (17,22) baard→neus; (50,26) lijf→arm R; (17,31) lijf→arm L.
- Gesp (18 px, zoals r1, gemeten op het model), oogstrook (Jordi "1 akkoord", zoals r1), outline highlights 7 px (zoals r1).
- Niets getekend: geen vorm, naad of facet die niet op een modelplek ligt.

## Controle
64×64 P, transparant 0, 15 kleuren (index 14 ongebruikt), zwart 9,6 %, geen losse zwarte pixels; lichte kleur op de buitenrand alleen de 4 outline highlights. Vlekjes < 3 px: lijnstukjes die aan een lijn vastzitten en de glans op de handen.

## Eigen zwakke punten
- Haar R blijft een klein lichtgrijs plukje onder de muts (de spitse modelplukjes zijn ±1 px dik).
- Het ronde schouderstuk rechts leest als plaat tussen de platen, niet als apart ovaal: de bolschaduw van het lijf loopt eroverheen.
- Riem heeft veel segmentlijnen (zo staan ze in het model); op 1× rustig.
