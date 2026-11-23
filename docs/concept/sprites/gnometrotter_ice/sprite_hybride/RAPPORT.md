# Gnometrotter Ice HYBRIDE – frontsprite (23 nov)

Model (bevroren): `../hybride/model_hybride.png`. Dat is r3 met dezelfde omtrek; muts, baard, haar, neus, riem, stok en zolen zijn 100 % r3. Alleen het roze en blauwe lijf heeft de ijsblokken van r1 ("ice perfect").
Opgeleverd: `gnometrotter_ice_hybride.png` (64×64 P, index 0 transparant, 16 kleuren, zelfde palet en indexen als Ice en Rock), `gnometrotter_ice_hybride_8x.png`, `vel.png` (hybride | gewone Ice r2 | model op 8×; 1× licht/donker; 1× en 2× naast Ice r2 en Rock). Script: `python3 hybride.py`, daarna `python3 ../sprite_r2/vel.py gnometrotter_ice_hybride.png ../sprite_r2/gnometrotter_ice.png "Ice hybride" "Ice r2 (zelfde pose)" vel.png ../hybride/model_hybride.png`.

## Werkwijze (zelfde pijplijn, niets getekend)
- Buiten het lijf is de sprite Ice r2, pixel voor pixel: het model is daar gelijk aan r3 (0 px verschil buiten het lijf).
- Silhouet, onderdelen, delen (dijen, voeten, band, schouderovaal, arm, vuist, handen), buitenlijn, ringen en deelgrenzen zijn die van Ice r2. De omtrek en de zwarte lijnen van het hybride model zijn die van r3 (zie `hybride/RAPPORT.md`). Silhouetverschil met r2: 0.
- **Vlakken van het lijf opnieuw uit het hybride model.** Per spritepixel de modelhelderheid van het roze of blauw (zonder naden), plus een Gen 3-bol per deel (licht linksboven), verdeeld over 3 tinten. Daarna één meerderheidsfilter binnen het deel, zodat de blokken egale vlakken blijven.
- **Blokranden = de naden van het hybride model:** pixels donkerder dan de lokale mediaan − 22, aandeel ≥ 0,25, op een lokaal maximum en ≥ 3 px doorlopend. Ze staan in 6 (roze) of 9 (blauw), nooit zwart (72 px).

## Afwijking t.o.v. Ice r2 (alleen in het lijf)
| deel | anders / deel |
|---|---|
| nek | 21 / 32 |
| schouderovaal | 18 / 67 |
| lijf | 91 / 177 |
| arm R | 8 / 30 |
| vuist | 7 / 52 |
| arm L | 9 / 24 |
| hand R | 15 / 66 |
| rechterdij | 53 / 118 |
| band | 14 / 31 |
| linkerdij | 46 / 107 |
| linkervoet | 12 / 44 |
| rechtervoet | 16 / 52 |
| **totaal** | **310** (0 buiten het lijf) |

Afwijking t.o.v. de kale reductie: zoals bij Ice r2 (zie `../sprite_r2/RAPPORT.md`), plus deze 310 px.

## Pixels die niet rechtstreeks uit het model komen
- De volumeterm (bol per deel) in de tintkeuze. Dit is een regel, geen vorm.
- Alles wat Ice r2 al meldde (gesp, oogstrook, outline highlights, de puntvorm van de baardpegels, het gat).

## Controle
Geen losse zwarte pixels en geen lichte kleur op de buitenrand. Vlekjes < 3 px: 4 hooglichtpixels (15) op de blokken, lijnstukjes en de vlekjes die ook in r2 staan.

## Zwakke punten
- **Pastel:** het model heeft pastelroze blokken. De sprite gebruikt het gedeelde (fellere) roze van Rock en Gnomad, want het palet moet gedeeld blijven.
- **Schouder en elleboog** blijven ronde schijven met een ring (de omtrek is heilig, zie `hybride/RAPPORT.md`). De blokken staan erin, maar de cilindervorm van r1 kan niet.
- **Gat bij de mutspunt:** hetzelfde punt als bij Ice r2. Er is geen aparte hybride-variant met het gat dicht; die is te maken door `hybride.py` op `../sprite_r2/gnometrotter_ice_gatdicht.png` te laten draaien.
