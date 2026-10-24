# Alpaca ronde 17: C2 en C4 (+ variant kop)

Basis: `../ronde16/variant_hals/anim_front.png` (goedgekeurd). Openstaand uit `checklist_keuring/KEURING.md` §4. Palet ongewijzigd, transparency=0. Lijf en poten zijn in beide frames gelijk, dus de wijzigingen ook. Script: `bron/alpaca17.py`.

| Punt | Wat | Waar | Pixels |
|---|---|---|---|
| C2 verre voorpoot 1 px lager | Handschoen en manchet (x24–31, y43–50) schuiven letterlijk 1 rij omlaag. De poot wordt 1 rij langer: rij y42 (`644551`) staat nu ook op y43. De voet staat nu op y51, **3 px** hoger dan de nabije (y54); dat was 4. De omlijning van de nabije achtervoet (31,50) blijft staan. De handschoen raakt de achtervoet nu op y48–50 (was y48), met omlijning ertussen. | x24–31, y43–51 | 35 |
| C4 knie nabije voorpoot | Rij y42 schuift 1 px naar achteren (gelijk aan y41: `6241` op x19–22). Op y43 wordt (18,43) omlijning `6` (anders ontstaat een open rand). Het bovenbeen loopt steiler, het onderbeen schuin naar voren: er zit een knik op y42. | x18–22, y42–43 | 6 |

Totaal 41 px per frame. **Pixeldiff buiten de zones (x17–31, y42–51): 0.** Open randen: 0 nieuw. Oppervlak 937 → 943.
**Zelfcheck** (1× en 3× naast ronde 16): de verre vuist staat meer op de grond en de vier voeten staan minder getrapt. De knie leest op 3× als een kleine knik, op 1× subtiel. De kop en de hals zijn ongewijzigd.

## variant_kop/ (groot, ter keuze): D2
Ronde 17 met een grotere kop. **Geen herschaling.** Er worden 2 rijen en 2 kolommen letterlijk verdubbeld op plekken zonder kenmerk, zodat oog, oren, vlechtjes, snuit, neus en mond pixel voor pixel gelijk blijven. Script: `bron/alpaca17_kop.py`.
- **Kolom x21** (voorhoofd/wang tussen snuit en oog): de snuit wordt 1 px langer.
- **Kolom x29** (achterhoofd achter het oog): het achterhoofd en het nabije oor schuiven 1 px naar rechts.
- **Rijen y11** (voorhoofd) **en y19** (bovenlip): de kop wordt 2 rijen hoger.
- De onderrand van de kop (y22) en de hals blijven staan; de kop groeit naar boven en opzij. Frame 2 volgt dezelfde regel als ronde 15–17.
- Kop y2–22 = 21/53 = **40%** (doel 40–55%; was 37%). Oppervlak **1019** (D1 fase 1: 700–950; ronde 17 heeft 943). De grotere kop brengt het formaat dus boven de grens. Open randen: 0 nieuw. Alle 225 gewijzigde px liggen in de koprijen (y ≤ 22/23).
- Op 3× oogt hij jonger en kopziger, met dezelfde gezichtsuitdrukking. Het voorhoofdstreepje heeft één tussenruimte van 4 px (was 3).

## Jordi (23 okt)
**variant_kop goedgekeurd** ("alpaca variant ook goed").

- **Telgang bewust (Jordi, 24 okt):** alpaca's (kameelachtigen) lopen in telgang; de pootstand (beide nabije poten vóór) blijft zo.
