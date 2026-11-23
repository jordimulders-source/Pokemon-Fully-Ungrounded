# Gnometrotter Ice – sprite r2 (23 nov)

Basis: r1 (`../sprite/`), dezelfde gedeelde reductie, hetzelfde palet en dezelfde onderdelen. Het silhouet is gelijk aan r1 (0 px verschil). Opgeleverd: `gnometrotter_ice.png`, `gnometrotter_ice_8x.png`, `vel.png` (r2 | r1 | model op 8×; 1× op licht/donker; 1× en 2× naast r1 en Rock r2) en de variant `gnometrotter_ice_gatdicht.png` (+ `gat_varianten.png`).
Bouwen: `python3 delen.py` (eenmalig), `python3 r2.py`, `python3 r2.py dicht`, `python3 vel.py`, `python3 tel.py`. Meetbeelden: `mg.py` (sprite | model met spriteraster op 4×).

## Reparaties (alles overgenomen uit het model)
1. **Baard = ijspegels.**
   - Spleten: de drie kolommen met de laagste modelhelderheid (X 20, 24 en 28). Vanaf rij 25 schaduwtint 12, recht verticaal; er staan geen V- of Y-lijnen meer.
   - Bovenin (tot rij 28) blijft één massa, zoals in het model. Daaronder hangen losse pegels.
   - Spitse punten op de onderkant gemeten in het model (rond = gemiddelde van meerdere pixels): pegel X 21–23 punt (22,38) en pegel X 25–27 punt (26,38) hangen over de riem; pegel X 29–31 punt (30,33) hangt over het lijf. De linkerpegel loopt door tot de riem, zoals in het model.
   - Tussen de punten komt terug wat er in het model achter zit (roze lijf in tint 7, of riem).
   - Per pegel: links licht (14), midden 13, aan de schaduwkant (X 31) 12. De rand tegen lijf en riem is in 2 (de baard ligt vooraan).
2. **Gat bij de mutspunt.** De rand volgt nu de DC-regel (outline base aan de lichtkant, zwart aan de schaduwkant). Er hangt één pegel in, zoals in het model. **Melding: op 1× leest het nog als een teken of oog**, vooral op een donkere achtergrond. Daarom staat er een variant naast met het gat dicht in mutskleur (`gnometrotter_ice_gatdicht.png`; 11 px silhouet erbij, 34 px gewijzigd). Vergelijking: `gat_varianten.png`.
3. **De punten van de Rock-keurder, op dezelfde plekken** (`delen.py`: het model geknipt langs zijn eigen donkere lijnen, helderheid < 100; 13 delen):
   - **Voetballen:** linkervoet X 17–28, Y 50–54; rechtervoet onder de gemeten modellijn Y 50 (X 40–48). Elke voet is een lichte bol (11/10, schaduw rechtsonder). De grens tussen dij en voet is 1 px in 9 op de pixel met de meeste modellijn.
   - **Broek zonder ruis:** de delen zijn linkerdij, rechterdij en de band onder de riem, elk als bol. Er zijn alleen lijnen waar het model ze heeft: de grenzen tussen de delen en de naden van minstens 3 px met modellijn ≥ 0,22 (o.a. de binnenrand van de rechterdij op X 38). De witte barsten zijn weg.
   - **Schouderovaal rechts:** een eigen deel (model x 40–50, y 19–29) met een ring in 6 rondom, ook de onderrand. Vulling als bol: 15 linksboven, 8, en 7 als sikkel.
   - **Haar R volledig:** alle pixels met ≥ 40 % helder modelijs (X 33–40, rij 15–19) horen bij het plukje (14 waar ≥ 75 %, anders 13). Waar het model onder het plukje een donkere lijn heeft (≥ 20 %), staat lijn 2 of 6.
   - **Linkerarm zonder dambord:** bovenrij in lijn 6, midden 8, de rij boven de onderrand 7, onderrand zwart/6. De vuist is een rond deel met een ring, en die ring vormt de scheiding tussen vuist en arm.
   - **Lijf:** één bol (licht linksboven), met slagschaduw 7 onder muts, neus, baard en haar, zoals in het model.

## Afwijking (`tel.py`)
| zone | anders t.o.v. kaal / zone | anders t.o.v. r1 |
|---|---|---|
| muts+rugkam | 367 / 468 | 13 |
| haar L | 34 / 39 | 0 |
| haar R | 26 / 40 | 15 |
| baard | 159 / 201 | 125 |
| neus | 21 / 56 | 8 |
| lijf | 175 / 278 | 115 |
| arm L+hand | 50 / 71 | 19 |
| arm R | 19 / 30 | 10 |
| hand R | 38 / 66 | 11 |
| riem | 162 / 200 | 0 |
| stok | 85 / 92 | 0 |
| broek/benen | 275 / 352 | 168 |
| zool L | 49 / 60 | 0 |
| zool R | 47 / 58 | 0 |

Totaal: 1509 van 2011 px anders dan de kale reductie, 484 anders dan r1. Het silhouet wijkt 7 px af van de kale reductie (zoals in r1) en 0 px van r1.

## Pixels die niet rechtstreeks uit het model komen
- **Volumetinten:** alle vlakpixels van lijf, nek, schouderovaal, armen, handen, dijen, band en voeten. Dit is een regel (een bol per deel), geen vorm.
- **Baard:** de puntvorm wordt per pegel getrapt (midden 1 rij dieper dan de zijkolommen). De pegelbreedte en de plek van de spleten zijn gemeten. De punt-rijen zijn gemeten op het 4×-raster; dat zijn waarden die ik zelf heb afgelezen.
- **Overgenomen uit r1:** de gesp, de oogstrook en de outline highlights op muts en haar L.

## Controle
64×64 P, transparant 0, 16 kleuren, zwart 9,6 %. Geen losse zwarte pixels en geen lichte kleur op de buitenrand. Vlekjes < 3 px: de notch (20,34) in lijfkleur tussen twee pegels, de slagschaduw van de neus (25,21) en (18,23), en lijnstukjes in 9.

## Eigen zwakke punten
- **Gat:** leest op 1× als teken of oog; de variant met het gat dicht leest rustiger. Ontwerpkeuze voor Jordi.
- **Baard:** het bovenste deel (massa) is egaal licht. Het model heeft daar ook pegelstrepen, maar tot rij 25 laat ik ze weg (anders komen de V-vormen terug).
- **Lijf:** de platen van het model zitten er nauwelijks meer in (alleen een paar naden in 6). Het leest als één gladde roze bol, net als Rock r2.
