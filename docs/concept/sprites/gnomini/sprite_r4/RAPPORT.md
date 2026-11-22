# Gnomini – sprite r4 (22 nov)

Basis: `r3B.png` (= `../sprite_r3/gnomini_B.png`). Script: `r4.py`, vel: `vel.py`.
Jordi: "B is goed, maar het lijf moet nog iets smoother rond qua vorm".

## Wat er zichtbaar is van de lijfomtrek
Muts, armpjes en voetjes bedekken het grootste deel van de rand, en die blijven bevroren. Vrij liggen alleen:
- de linkerrand, rijen 47–50, tussen armpje L en voet L;
- de rechterrand, rijen 46–52, tussen armpje R en voet R;
- de onderrand tussen de voetjes.

In r3 had de rechterrand een rechte trap (2-2-2) en de linkerrand 1-1-2. Het lijf is verder al een cirkel met r ≈ 12, middelpunt (32, 42,5); het zichtbare deel volgt die cirkel op ±1 px.

- **A (licht smoother):** links 20-21-21-22 (lopen 1-2-1), rechts 43-43-43-42-42-41-40 (lopen 3-2-1-1, vloeiend in plaats van een rechte trap).
- **B (ronder):** de onderste flanken bollen uit, zodat de onderkant voller wordt (U-vorm in plaats van ei). Links 20-20-20-21 (lopen 3-2), rechts 43-43-43-43-42-41-40 (lopen 4-1-1-1). Gemeten breedte en hoogte van de bol zijn gelijk aan r3; de onderrand is ongewijzigd.

De gebogen grens, de donkerblauwe streep en de tonen lopen mee. Nieuwe pixels krijgen de toon van de dichtstbijzijnde r3-pixel, de rechterrand krijgt schaduw.

## Diff t.o.v. r3-B (`r4.py`)
| | lijf (vlak + eigen rand) | muts | neus | arm L | arm R | voet L | voet R | silhouet |
|---|---|---|---|---|---|---|---|---|
| A | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| B | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 7 |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels, 14 kleuren.

## Eigen zwak punt
Het verschil is klein, omdat de rand bijna overal achter muts, armpjes en voetjes zit. "Duidelijk ronder" lukt binnen diff 0 voor de onderdelen niet. Het lijf leest op 1× vooral als een brede kom onder de muts. Meer rondheid kan op twee manieren, allebei een ontwerpkeuze voor Jordi:
- de onderkant tussen de voetjes 1 px dieper (U-bodem);
- armpjes en voetjes een paar px naar binnen of naar onder, zodat er meer zijflank vrij komt.

Bestanden: `gnomini_A.png`, `gnomini_B.png`, `AB_8x.png` (A | B, 8×), `vel.png` (A | B | r3-B op 8× en 1×).
