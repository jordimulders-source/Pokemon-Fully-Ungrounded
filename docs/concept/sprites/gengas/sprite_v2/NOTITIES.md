# Gengas sprite v2 (15 nov) – het model overnemen, niets hertekenen

Basis: `../model/model_64_geschrapt.png` (elke pixel een modelpixel). Keten (reproduceerbaar, `./bouw.sh`):
`kwantiseer.py` (dichtstbijzijnde gemeten tint, Lab) → `gezicht_schuif.py` (hybride gezicht) → `ontruis.py`
(alleen losse 1-px vulpixels in het lijf; randen, gezicht, wervel en manen beschermd) → `handwerk.py`
(47 bewuste pixelcorrecties, elk met reden; log in `raster.txt.log`) → `maak.py`.
Tussenrasters in `tussen/`. Hulp: `toon.py`, `rooster.py` (close-up met raster), `controle.py`, `vel.py`.

## Palet (15 + transparant), alles gemeten in het model
| teken | RGB | bron (mediaan van het Lab-cluster in het model) |
|---|---|---|
| K | 11,5,8 | omlijning (lum < 38), 227 px |
| a | 81,37,60 | schaduwband/schaduwkant, 252 px |
| b | 96,54,74 | donkere band / masker, 324 px |
| r | 118,48,67 | selout lichtkant: bovenrand kop rij 11-13 (117-125, 48-53, 66-73) + donkerrode lijnen |
| m | 140,49,85 | middentint, 319 px |
| l | 187,84,105 | lichte band, 414 px |
| v | 196,128,139 | lichtvlek, 119 px |
| w | 220,172,176 | kern lichtvlek, 19 px |
| E | 201,62,70 | oogrood donker |
| R | 240,102,109 | oogrood helder |
| g | 62,62,61 | maan donker / grijze selout |
| G | 100,99,98 | maan midden |
| h | 136,135,132 | maan licht |
| H | 186,185,183 | maanglans + tandschaduw |
| W | 254,254,254 | tanden, oogglans |
Weggevallen (16e tint, kleinste verlies gemeten): gedempt mauve 121,70,91 (40 px, wig tussen de ogen,
rand bij het linkeroor) → nu b, op de punt van de wig m. Gem. kleurafstand model → palet: ΔE 2,8.

## Gezicht (Jordi: grootte/vorm van het model, positie van r3)
Middelpunten gemeten (model → r3): linkeroog +4,6/+3,2, rechteroog +4,1/+1,0, grijns +5,6/−0,1 → het hele
modelblok (rij 28-45, kol 8-27, incl. masker ertussen) als één blok dx +5, dy +1. Randpixels van het silhouet
schuiven niet mee. Vrijgekomen strook links: rij 28-37 maskerband (b, rand a/r zoals rij 27), rij 38-46 lichte
band (l) zoals links van de grijns in het model. Gengar-vorm (alleen waar het model afwijkt):
- rechteroog had geen pupil (Gengar wel, modellinkeroog ook): Gengars 3-px-pupil op (34,27),(34,28),(35,28);
- bovenlip linksboven liep K-a-K-a om en om → doorlopende zwarte 2:1-diagonaal; tandschaduw aan de punten één tint.

## Controles (`controle.py`)
- 15 kleuren + transparant.
- Silhouet: 1 px anders dan het model ((10,32), los omlijningsstaartje onder de bovenste maan weg).
- Cirkelfit bol (buitenrand lijf rij 22-58, zonder manen/rookarm): middelpunt (29,9; 35,4), straal 22,6,
  rms 0,32 px, max 0,70 px → bol.
- Afwijkend van de dichtstbijzijnde modeltint: 130 px (gezichtsblok vergeleken met het verschoven model);
  daarvan 45 in de vrijgekomen strook, 47 handwerk, 31 ruisfilter, rest de opvulling van verplaatste gezichtspixels.
- Omlijningspixels zonder buur: alleen (2,30), een zwart kratertje in de bovenste maan (model).
- Lichte pixels op de buitenrand: alleen de gaspunten van het linkeroor en de rookslierten (model, bewust).

## Zwakke punten (eerlijk)
- Losse 1-px pixels: nog 75, vooral kraterstructuur in de manen en tandschaduw/lijnen in het gezicht en de wervel.
  Bewust niet weggefilterd: een filter sloopte de wervel en de kraters (geprobeerd). Manen zijn dus nog korrelig
  zoals het model; als Jordi ze rustiger wil: per maan met de hand, kraters als 2-3-px-vlekjes.
- Lichtvlek: model heeft een zachte gradiënt, sprite 2 tinten (v/w) → iets vlakker.
- Bovenste tandenrij is grijs (H) zoals in het model (lipschaduw); Gengar heeft witte tanden met grijze naden.
- De pupil in het rechteroog is een toevoeging (Gengar-vorm); zonder pupil = model. Even aan Jordi laten zien.
- Het masker links van het linkeroog is nu een vlak donker stuk (vrijgekomen strook); in het model liep het oog
  tegen de rand.
- Gaspunten van het linkeroor en de rookslierten hebben geen buitenlijn (model: gas); Gen 3-keurder kan dat aanstrepen.
