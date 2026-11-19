# Eindkeuring Dragonfly Cave: Picaraio sprite v2, kleur r3 (19 nov)

Gekeurd: `picaraio.png` + `normal.pal` (64×64, P-modus, transparency=0, 16 kleuren). Alleen uitvoering; vorm, kleur en schaduw waren al goedgekeurd.
Vergeleken op 1×, 2×, 5× en 12× (licht en donker) naast Gen 3 Pidgeot, Swellow, Staravia, Raichu en Fearow (`graphics/pokemon/`), en met het model `gemini/r9_prompt_v6.png`.

## Oordeel: GOED

| Punt | Bevinding |
|---|---|
| Leesbaarheid 1× | Leest direct als vogel met kuif, snavel, oog, rode wang, gestippelde vleugel, bliksem en staartkoord. Staat qua netheid naast Pidgeot/Fearow niet uit de toon. |
| Belijning / selout | 1 px; zwart aan de schaduwkant, gekleurde selout (donkerbruin F, cremeschaduw 7, donkergeel D) aan de lichtkant. Geen zwart/donker om-en-om op één rand, geen dubbele lijnen, geen lichte kleur op de buitenrand. |
| Jaggies / trapjes | Vleugelbovenrand loopt in een regelmatige 2:1-trap; kuifslierten en staartkoord zijn vloeiende 1 px-lijnen zonder onderbrekingen, beide krulletjes (kuif) leesbaar. Eén lange rechte strook: zie reparatie 1 (optioneel). |
| Binnenlijnen | Zwart alleen waar vorm over vorm valt (kop/kuif, vleugel/lijf, veerpunten onderaan de vleugel, poten). Geen losse zwarte pixels midden in een vlak. |
| AA / ruis / losse pixels | Geen AA aan de buitenkant. Clusterscan: alleen selout-pixels, glans van het oog (20,12) en de vleugelstippen; geen ruis. |
| Banding / pillow shading | Geen pillow shading; licht linksboven, schaduw als sikkel rechts/onder. De 2 px schaduwband langs de achterkant van de kop (x 27–28, y 14–21) loopt parallel aan een rechte rand, maar leest als randschaduw zoals bij Swellow; acceptabel. |
| Contrast | Helderheidsstappen bruin 173 → 133 → 92 → 62, crème 243 → 211 → 170, geel 240 → 208 → 160: binnen de ±30–40 van Gen 3. Grijs (snavel/poten) stapt ±60, passend voor kleine delen. |
| Tintgebruik | Schaduw verschuift naar rood (bruin 27° → 18°, crème 45° → 37°): goede hue-shift, niet grijs/vuil. |
| Lichtrichting | Consistent linksboven op kop, buik, vleugel, snavel en bliksem. |

## Optionele pixelreparatie (niet blokkerend)
1. Buik-linkerrand is 8 px recht (x=11, y 26–33); "geen rechte stukken waar het dier rond is (buikrand)". Rondere curve met 2 pixels minder silhouet:
   - (11,26) 7 → 0 (transparant)
   - (11,33) 7 → 0 (transparant)
   - (12,33) 5 → 7
   (Rand wordt dan x=12 y 24–26, x=11 y 27–32, x=12 y 33–35: runs 3-6-3 in plaats van 1-8-2.) Raakt het goedgekeurde silhouet met 2 px; alleen doen als Jordi dat goed vindt.

## Ter info voor Jordi (ontwerp, geen keuring)
- Op een donkere achtergrond valt het zwarte 1 px-staartkoord en de kuifslierten grotendeels weg (Raichu's staart is dikker en grijs). In de gevechtsachtergronden van Gen 3 is dat meestal geen probleem.
- De bliksem raakt de linkerrand van het canvas (x=0, y 29); binnen de afgesproken marge van ±1 px.
