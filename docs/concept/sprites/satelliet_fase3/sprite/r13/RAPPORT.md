# Ruimtestation sprite r13 (25 nov): PB half zo ver, PF doorlopend achter voorbuis en PE

Jordi over r12: "rechtsboven paneel opgelost, boven is nu juist te ver doorgeschoven en onder heb je nu bijna helemaal weggehaald".

Jordi over PF: "hij moet overlapt worden maar op een goede manier".

**Werkwijze:** `herstel13.py <naam> <PB px> <PF px> <PF-lengte>` start opnieuw vanaf `r11/sprite.png`, met dezelfde stappen en hetzelfde recept als r12 (`recept.py`).

**Wat gelijk blijft en wat verandert:**
- PC en de PE-punten zijn gelijk aan r12: het PC-vak is pixel-gelijk. De ogen zijn niet aangeraakt (0 px verschil in alle varianten).
- Per variant zijn alleen PB en PF anders.
- Elke variant staat in een eigen map met `sprite.png`, `sprite_8x.png`, `diff_r11.png` en `log.txt`. De log geeft per pixel de reden en onderaan de zichtbare PF-stukken.
- `vel.png`: r11, r12 en A–D op 8×; close-ups van PB en PF per versie op 12×; 1×/2× naast fase 2.

## Varianten

| | PB | PF | anders dan r11 |
|---|---|---|---|
| **A** `A_pb15_pflang` | −1,5 px | lang, r11-plek | 105 px |
| **B** `B_pb15_pflang15` | −1,5 px | lang, −1,5 px | 118 px |
| **C** `C_pb20_pflang` | −2 px | lang, r11-plek | 130 px |
| **D** `D_pb20_pflang15` | −2 px | lang, −1,5 px | 143 px |

**PB:** de verschuiving gaat langs de breedterichting, net als in r12:
- −1,5 px wordt −1,5 / −0,83 (x / y)
- −2 px wordt −2 / −1,11
- r12 was −3,01 / −1,67.

De stok zit daardoor tussen de rand (r11) en het midden (r12) in. Waar PB weg is, krijgt de romp omlijning; die is navenant.

## PF: waarom "lang"
**Lengte 47 werkt niet.** Met de r11-lengte (47 modelpx) is het stuk onder PE een snipper van 12 px, 3 px breed (u 0,63–1,00). Bij −1,5 px blijft daar nog 2 px van over.

**Lengte 61 wel.** Dat is 61 modelpx met 3 vakken (het besluit "mast 3 vakken" blijft). Daarmee komt PF aan beide kanten van PE met minstens één heel vak uit:
- de grenzen liggen op één lijn;
- de randen sluiten door;
- er zijn geen losse snippers.

**Gevolg:** een vak van PF is nu 20,3 modelpx in plaats van 15,7 (PB). PF wordt dus iets langer dan PB, en het onderste punt komt op y 59 (was 55).

**Links van de voorbuis** blijft niets van PF zichtbaar: de buis is breder dan het halve paneel.

## Zichtbare PF-stukken
u loopt van 0 (boven) tot 1 (onder); de vakgrenzen liggen op 1/3 en 2/3.

| | boven PE | onder PE | totaal |
|---|---|---|---|
| A en C (r11-plek) | 37 px, x 34–40, y 41–47, u 0,01–0,31: vak 1 heel | 36 px, x 34–40, y 51–59, u 0,48–0,99: rest van vak 2 + rasterlijn + vak 3 heel | 73 px (r11: 50) |
| B en D (−1,5) | 27 px, x 34–38, y 41–47: vak 1 heel; links navy rand waar PF achter de buis gaat | 23 px, x 33–38, y 54–59, u 0,70–0,99: vak 3 (bijna) heel | 50 px (gelijk aan r11) |

## Aandachtspunten
- **Advies Claude: A of C.** Daar is PF aan beide kanten het duidelijkst, met de rasterlijn zichtbaar onder PE.
- **Vak 3 is donker:** het onderste vak heeft de donkerste vaktint van het recept (14/13/11). Het stuk onder PE is daardoor donker; dat volgt het bestaande recept.
- Nog geen keurder geweest.
