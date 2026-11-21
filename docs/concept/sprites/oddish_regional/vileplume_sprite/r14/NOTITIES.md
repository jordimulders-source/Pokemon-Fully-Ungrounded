# Vileplume r14 (21 nov)

Jordi op r13:
- "zwarte lijn tussen middenvoor en rechtsvoor"
- "poten zijn niet beter nee"
- "ga maar terug naar de vorige, zoveeel gespiegeled naar moddel"

Basis: `r13/vileplume_r13_dunnepoten.png`. Bouwen (vanuit `vileplume_sprite/`): `python3 r14/bouw.py` en daarna `python3 r14/vel.py`. Gewijzigd zijn alleen de naad VL|VR en de poten; daarbuiten is het verschil 0 (assert).

Bestanden:
- `vileplume_r14.png`: P-modus, 16 plekken, transparency=0, palet r13.
- `bouw.py`, `poten.py`, `vel.py`.
- `vel.png`: r14 | r13 | model op 8×; naad en poten op 12× naast het model; 1×.
- `uitvoer.txt`, `toets.txt`.

## Naad VL|VR (17 px)
In het model (natief raster) ligt geen van beide voorste anemonen duidelijk vóór de ander. Het zijn twee bolle lobben met een donkere onderband, die samenkomen in een korte zwarte inkeping:
- zwart alleen op u108–109, v82–93; dat is sprite x35, rij 24–28;
- onderaan wordt de inkeping breed zwart tegen het lijf (x34–36, rij 28);
- daarboven geen zwarte naad: de tentakels lopen door, met een korte donkerrode streek op (35,23).

r13 had een rechte zwarte lijn op x36 (rij 20–26) en x37 (rij 27–28). Die is nu:
- zwart op x35 rij 24–27 en x34–36 rij 28;
- R0 op (35,23);
- op de oude lijnplekken de tint van de eigen lob uit de kale reductie: R2, en R1 in de onderband.

## Poten (33 px)
Gemaakt met `poten.py`. Per rij en per poot nemen we de pixels met minstens 40 % modeldekking:
- **Breedte:** minder dan 3 px wordt aangevuld met de buur die de meeste dekking heeft. Komt het model breder uit dan de bestaande breedte, dan valt de eindpixel met de minste dekking weg.
- **Rand:** zwart of W0, wat het model het meest heeft. W1 van het model telt als W0, want het palet heeft geen W1.
- **Binnen:** de meest voorkomende vultint.

Wat er daardoor verandert t.o.v. r13-dun:
- **Linkerpoot:** de knie gaat terug naar het model. Rij 45–48 staat op x23, en vanaf rij 49 tot de voet op x24. De scheen op rij 56–58 staat niet meer op x25 maar op x24.
- **Rechterkant van de linkerpoot:** W0 op rij 46–51, daarna zwart.
- **Linkervoet:** de kap staat nu zwart op x24–26 onder de scheen. Het model heeft daar zwart met in het midden een lichte rest; zwart, omdat de buitenrand geen lichte kleur mag hebben.
- **Heup links (rij 43):** wordt aedK.
- **Rechterpoot:** de rechterrand is W0, zoals in het model, in plaats van zwart (rij 45–59). Rij 59 wordt aca. De plek per rij is gelijk gebleven. De voet (rij 60–62) is ongewijzigd.

## Toets
16 kleuren, bbox x2–60 y1–62, lijnpixel midden in een vlak 0, lichte kleur op de buitenrand 0, losse pixels 30, zwart 14,2 %.

## Eerlijk
- **Naad:** volgt het model nu duidelijk: een korte V-inkeping onderaan in plaats van een lange rechte lijn.
- **Poten:** liggen dichter bij het model (vooral de W0-rand rechts en de rechte scheen). Er is nu nog maar één verspringing, op rij 49; dat is de knik zoals het verkleinde model hem geeft.
