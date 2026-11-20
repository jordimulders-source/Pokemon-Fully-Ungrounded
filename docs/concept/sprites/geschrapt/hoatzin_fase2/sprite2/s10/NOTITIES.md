# Hoatzin fase 2, ontwerp 2, s10 (20 nov): kleur naar bestaande sprites

Jordi: "nog blurry ... De poten zijn nog niet netjes afgemaakt. De hele sprite mist gewoon schaduw/tinten/contrast. Het is heel veel 2 kleuren per stuk" · "lichaam/vleugel lijkt ook bijna willekeurig te zijn" · "kijk echt naar al bestaande sprites".
`sh alles.sh` (bouw10.py op s9). Silhouet = s9 (0 px anders); oog: zwart + 6 rood gelijk (assert), ring blauw.

## Studie (graphics/pokemon, 6-8x)
- **Braviary-vleugel:** de hele vleugel is één vlaktint. De pennen zijn korte donkere streepjes in een donkere eigen tint, niet zwart; zwart alleen op de buitencontour en de penpunten.
- **Honchkrow-lijf:** twee grote zones (licht linksboven, donker rechtsonder), met de grens langs de vorm. Binnenlijnen in een bijna-zwarte navy (40,40,64), buitenlijn zwart.
- **Staraptor-borst / Honchkrow-bef:** wit/crème vlak, schaduw grijs rechtsonder, geen gekleurde rand.
- **Honchkrow/Skarmory-poten:** grijs met zwarte lijn rondom, klauw = lichte punt.
- **Pidgeot/Staraptor-kuif:** licht linksboven, donker onder, zwarte buitenlijn.
- Les: niet per pen een lichte/donkere rand (dat gaf strepen en "willekeurige" vlekken), maar per vorm grote zones en de pennen alleen als donkere lijn.

## Toegepast
- **Vleugels, lijf, staart:** per vorm een lichte zone linksboven en een donkere zone rechtsonder. De grens volgt de vorm: afstand tot de rand linksboven tegenover die tot de rand rechtsonder. Daarbij een sikkel van 1 px in de donkerste tint langs rechtsonder.
- **Binnenlijnen:** in de lichte zone de donkerste navy; in de donkere zone zwart (anders vallen ze weg). Buitencontour zwart.
- **Verre vleugel:** een stap donkerder (donkere zone + lichte rand linksboven).
- **Crème** (nek, staartpunt): licht, midden, schaduw rechtsonder. **Kuif:** licht linksboven, midden, donker onder.
- **Gezichtsring:** licht linksboven, midden, schaduw rechtsonder. **Snavel:** licht boven, midden, donker onder.
- **Poten:** scheen licht boven → midden onder, tenen grijs met de zwarte lijn eronder, klauwen als lichte punt.

## Paletbudget (15 + transparant = 16)
| # | kleur | gebruikt voor |
|---|---|---|
| 1 | (16,14,24) | lijn (ook kuif-selout) |
| 2 | (96,108,170) | navy lichte zone, gezicht midden |
| 3 | (64,60,104) | navy donkere zone, gezicht schaduw, krop donker |
| 4 | (32,30,54) | navy binnenlijn/sikkel, grijs donker |
| 5-6 | (244,236,212) (208,198,172) | crème licht/midden |
| 7 | (146,144,136) | crème schaduw = grijs midden (zoals Staraptor/Honchkrow wit grijs schaduwen) |
| 8 | (192,192,188) | grijs licht (snavel, poten); niet gelijk aan het crème van de nek |
| 9-10 | | krop licht/midden |
| 11-13 | | kuif licht/midden/donker |
| 14 | | oogrood |
| 15 | (110,150,194) | gezicht licht |
Geprobeerd en verworpen: kuif-licht = oogrood (de kuif werd rood).

## Controle
dambord 0 · om-en-om 0 · klonten 0 · barcode 0; losse tintpixels 39 (penlijnstapjes in de donkerste tint, klauwpunten).
`vel.png`: s10 | s9 | model, en per onderdeel de uitsnede van het voorbeeld naast s10. `naast.png` 1x/2x, `zes.png` 6x naast Honchkrow en pitahaya.

## Eerlijk
- De tenen van 1 px hoog hebben alleen de zwarte lijn eronder; een lijn erboven vraagt extra silhouet (pootvorm ligt bij Jordi).
- De verre vleugel leest nog vrij vlak (één zone plus een rand).
