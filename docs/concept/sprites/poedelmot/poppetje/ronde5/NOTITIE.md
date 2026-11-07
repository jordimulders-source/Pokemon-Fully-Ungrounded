# Poedelmot poppetje, ronde 5 (5 nov)

Jordi: "je vergeet meerdere bronfotos te gebruiken he?". Dit poppetje is getoetst aan de LEIDRAAD bovenaan de SPEC, zin voor zin (zie de keuring).
Basis is ronde 4 (`../ronde4/pop3d_poedelmot_r4.py`). Wol, lijf en poten zijn ongewijzigd.

## Wat er veranderd is
1. **Ogen** (tak-foto + Venomoth):
   - Beide ogen zijn helemaal zichtbaar, rond en zwart met een glans. Het verre oog is kleiner maar heel, geen sikkel.
   - Ze zitten lager en meer naar voren, met witte wol ertussen.
   - De warme tint is weg, net als het masker: het verre oog lag in ronde 4 tegen de silhouetrand.
   - `OOG` = (-0.84, -0.22, ±0.52), straal 8.
2. **Sprieten** (Jordi: "naar de zijkant als oren", bruin):
   - De sprieten zijn een lagere boog opzij: lengte 48, boog 11 (ronde 4: 44, met een omhoog gekrulde punt).
   - Ze hebben een dichte dubbele kam (20 tanden per kant), om en om in twee bruintinten (gestreept).
   - De vorm komt uit de close-up en het vilt; dat is een voorstel, geen eis.
3. **Vleugels** (dubbel, wit, adertjes zoals het vilt):
   - Er zijn fijne lichtbruine adertjes als waaier vanuit de wortel, op alle vier de vleugels.
   - Een eigen `shade_aders` zorgt dat de adertjes geen zwarte lijn krijgen.
   - De verre achtervleugel staat verder opzij en is groter (25×16), als eigen ovaal links naast de kop.

## Bestanden
- `pop3d_poedelmot_r5.py`.
- `poppetje_45.png` en `poppetje_45_1x.png`.
- `vel.png`: bovenaan het geheel naast de tak-foto, en op 1× naast Butterfree en Venomoth. Daaronder de vakken "bron ↔ poppetje":
  - 0: fan-art en Frosmoth (leidraad 1 en 7);
  - 1: ogen;
  - 2: sprieten;
  - 3: vleugels en het lijf los van de vleugels;
  - 4: kop met kraag (voorstel).

  Voorstellen zijn op het vel gelabeld. Het script controleert dat er niets van het vel valt.
- `keurvel_45.png` + `keurvel_45.png.keuring.md`: eigen keuring met de leidraad afgevinkt, **FAIL**.

## Eigen zwakke punten
- **Ogen:** kleiner dan op de tak-foto, en op 1× klein en dicht bij elkaar.
- **Sprieten op 1×:** dichte bruine bladen zonder kam.
- **Adertjes:** nauwelijks zichtbaar op 1×.
- **Poten:** ongewijzigd (pixelstap).
