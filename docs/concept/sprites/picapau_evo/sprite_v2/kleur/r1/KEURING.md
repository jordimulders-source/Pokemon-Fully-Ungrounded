# Keuring Picaraio kleur r1 (19 nov): alleen kleur en schaduw

Gekeurd: `picaraio.png` + `normal.pal`. De vorm is niet gekeurd (bevroren, alpha-diff 0 met r4). Vergeleken: de sprite op 8×, en de bliksem op 8× naast Pikachu, Raichu en Jolteon (Gen 3, `graphics/pokemon/`) op 5×. Helderheid gemeten als luma (0,299R + 0,587G + 0,114B).

## Oordeel: FAIL (alleen de bliksem; 5 tintwissels)

**Goed:**
- **Bruin:** o 173 → O 133 → d 92 → selout u 62, stappen 40/41/30.
- **Crème:** C 243 → c 210 → b 169, stappen 33/41.
- **Geel:** W 239 → Y 208 → y 160, stappen 31/48.
- **Tinten per groep:** overal hooguit 3 plus omlijning.
- **Licht linksboven:** kophooglicht linksboven (14–22,7–11), de bovenkant van de vleugel `o`.
- **Buiksikkel:** loopt taps, van 1 px bij de schouder (22,23) naar 3 px rechtsonder (25–29,35–40), met `b` alleen als kern rechtsonder (25–30,42–44). Geen banding meer.
- **Onderste vleugelveren:** de binnenlijnen zijn nu `u`.
- **Poten:** de nabije poot (rechts) is lichter dan de verre, met één glanspixel `g` op (27,49).
- **Selout:** geen wisseling van selout en zwart om en om op één rand.

**Fout: de bliksem is gebanded.** In de bovenste tak liggen vier tinten als evenwijdige strepen van 1 px langs de rand: selout `y` | hooglicht `W` | `Y` | schaduw `y` (rijen 34–39, bijvoorbeeld rij 37: (3)y (4)W (5)Y (6)y). Op 8× leest hij als gestreept. Raichu en Pikachu houden het hooglicht als een vlek op de belichte punt of hoek en vullen de rest met de basistint, met schaduw aan de onder- en rechterkant.

## Tintreparaties

1. **Bliksem, het hooglicht als streep in de bovenste tak wordt basisgeel.** Zet `W` → `Y` op **(3,35), (4,36), (4,37), (5,38) en (5,39)**. Dan blijft er hooglicht over op twee plekken: de bovenpunt (2,32), (2,33), (3,33), (3,34) en de hoek van de zigzag (4,39), (2,40), (3,40), (3,41), (4,42). De bovenste tak wordt dan selout `y` | `Y` | `Y` | schaduw `y`, zoals bij Raichu. De onderste tak (Y | y, rijen 43–47) is goed zo.

Optioneel, geen reden voor FAIL: de kopsikkel `d` is van (27–28,14) tot (27–28,20) overal 2 px breed. Als Claude hem taps wil: (27,14) `d` → `O`.
