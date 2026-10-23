# Olinguito (Dark-starter fase 1), ronde 9: afmaken en repareren (basis ronde 8)

Geen nieuw ontwerp. De ronde-8-rasters zijn omgezet naar één delenbestand (`bron/delen.txt`, pixel-identiek gecontroleerd) en daarna met de hand bijgewerkt. Ogen, kleuren en de staartvorm bleven (Jordi: goed op weg); de staart kreeg alleen een lichte haak.

## Analyse: gids tegen echte Gen 3 (pixelniveau) en onze ronde 8
Bekeken: Poochyena, Zigzagoon, Sneasel, Sandshrew, Teddiursa; gids: *Shading*, *Outline shading*, *Curves*.

| Regel (gids) | Echte Pokémon | Ronde 8 | Wat ik veranderde |
|---|---|---|---|
| 3/4-aanzicht (naar links-voor) | Poochyena: verre oog klein naast de neusbrug, kop steekt links nog 2–3 px voorbij het verre oog uit, snoet kort en schuin omlaag | Snoet 5 px recht opzij vanaf de rand van de schedel, neus op ooghoogte: leest als profiel | Verre wang/voorhoofd 1–2 px naar links, zodat de neusbrug in één schuine lijn van voorhoofd naar neus loopt; snoet 2 px korter, neus rond (3×3 met glans), lager |
| Verre ledematen zichtbaar | Sneasel/Sandshrew: verre arm met klauw steekt rechts naast het lijf uit, kleiner en in schaduwtinten | Verre arm een vlekje grijs rechtsonder ("geamputeerd", lijf leek onaf) | Verre arm hangt langs de rechterflank met elleboog naar achter en een kleine dubbele klauw (klauwschaduw/-basis); zwarte rand links scheidt hem van het donkere lijf |
| Alles verbonden | Teddiursa: voeten lopen in het lijf over | Verre voet zweefde (1 lege rij tussen lijf en voet) | Verre been toegevoegd (schaduwbruin), voet sluit aan |
| Gezicht compleet | Zigzagoon/Poochyena: korte donkere mondlijn onder de neus naar achteren | Geen mond | Mondje: zwarte pixel onder de neus, 2 px mondlijn in omlijningsbruin |
| Geen rechte stukken in organische vormen | Aipom/Teddiursa: staart en schedel buigen overal | Staart 8 px rechte rand, schedeltop 7 px plat, kop rechts 5 px recht | Staart bovenaan naar rechts gebogen (haak), schedeltop met bolling, kop rechts licht bol |
| Omlijning per kleurgroep | Gen 3: 0,35–0,6 zwart | 0,64 | 0,62 (lijf is bewust overwegend schaduwtint; nog net te hoog) |

## Controle (checklist)
- [x] Tellen: 2 armen (voor met grote klauw, achter met kleine klauw), 2 benen/voeten, 2 oren, 2 ogen, 1 mond, 1 neus, 1 staart.
- [x] Omtrek dicht: geen randpixels zonder omlijningskleur; verre voet en verre arm verbonden met het lijf.
- [x] Geen recht stuk > 4 px in organische vormen. Over: de linkerkant van de grote klauw (7 px, klauw is hard materiaal; ongewijzigd).
- [~] Zwart-aandeel rand **0,62** (doel 0,35–0,6).
- [ ] Oppervlak **1099 px** (ronde 8: 1081), boven ±800–950; kleiner kan alleen door herschalen.
- [x] 64×64, 2 frames (kop, armen, klauwen en staart 1 px omhoog), 16 kleuren, index 0 transparant.

## Bestanden
- `anim_front.png`, `normal.pal`, `compare.png` (ronde 8, ronde 9, Zigzagoon, Poochyena, Teddiursa; 1× en 3×).
- `bron/delen.txt`, `bron/palet.txt`, `bron/raster_f1.txt`/`raster_f2.txt`, `bron/bouw9.py`, `bron/zet.py`, `bron/patches/`, `bron/vergelijk9.py`.
