# Nachtaap fase 2: kleursprite ronde 6

Basis is ronde 5. Jordi gaf de vragen van de keurder vrij: "doe maar wat de keurder goed lijkt". Het silhouet, de maan (D2), de ogen, de snoet en de kop zijn bevroren.

## Bewijs
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Palet:** gelijk aan ronde 5.
- **Pixeldiff t.o.v. ronde 5:** 158 px, waarvan 0 buiten de zones.

| Zone | Pixels |
|---|---|
| F5 kené (x 16–47, y 26–38) | 89 (de oude lijntjes weg plus de nieuwe meander van 46 px) |
| handen (x 3–27, y 55–62) | 48 |
| achtervoet (x 31–42, y 56–60) | 10 |
| oor links | 5 |
| oor rechts | 6 |

- Twee pixels liggen net onder de opgegeven F5-zone: de staart van de oude band A op x 35, y 37–38. Die heb ik ook weggehaald, anders bleef er een los stukje lijn staan.

## Wat er veranderde
- **Kené:**
  - De diagonale lijntjes en de ruggengraatlijn zijn weg (raster: de kené-laag geschrapt, zodat de vacht van ronde 1 terugkomt).
  - Daarvoor in de plaats: één doorlopende **meander met rechte treden** langs de rugmiddenlijn, van achter de kop (x 17) tot vóór de staartbasis (x 39).
    - De treden zijn horizontaal 2–4 px en verticaal 2–3 px, zonder diagonalen.
    - Hij ligt 2–5 rijen onder de rugrand en buigt mee met de bol: links omhoog, bovenop vlak, rechts omlaag.
  - **Kleur:** idx 6 (`m`) op het licht en de basis, idx 5 (`l`) waar hij in de schaduw komt (rechts). Geen wit, dus rustiger dan de maan.
  - Script: `bron/meander.py` (zie onder); de pixels staan als regels in `raster.txt`.
- **Handen:**
  - **Verre hand:** de rug is violet in de schaduwtint `s` met de selout `d`. Alleen de 3 vingertoppen zijn crème (`f`, met `e`-lijnen ertussen).
  - **Nabije hand:** de rug is violet (licht linksboven, `s` rechts). De crème zit alleen in de duimtop en de 4 vingertoppen, met de vingerlijnen die de rug in lopen, zoals bij Aipom en Monferno.
- **Achtervoet:** de rug is violet, de tenen en de zool vooraan zijn crème, met tenen gescheiden door `e`/`t`.
- **Oren:** beide violet (`b`, met `s` aan de schaduwkant). De binnenkant is een klein lila vlakje: 2 px `m` per oor. Er zijn geen crème vlakken meer naast de maan.

## Eerlijk
- Op 1× is de meander een rustig getrapt bandje langs de rug. Hij leest als patroon, niet als ruis, maar is bewust zachter dan de maan.

## Lessen
- **Een patroon dat op 1× als patroon moet lezen: kies rechte treden met een vaste maat** (hier 2–4 px), die meebuigen met de bol. Losse diagonale 1-px-lijnen lezen als krassen of bliksem.
- **Handen in de vachtkleur met alleen crème toppen** halen het "plankje" weg zonder het silhouet te veranderen. Ook het tweede lichte vlak naast het gezicht verdwijnt zo (de oren).
- **Een kené-laag schrappen in het raster** (in plaats van eroverheen te schilderen) geeft de oorspronkelijke vachtschaduw vanzelf terug.
