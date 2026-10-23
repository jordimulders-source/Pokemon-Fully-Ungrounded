# Alpaca fase 1, ronde 15: B + C, iets duidelijker, en de neusstreep

Jordi koos ronde 14 **B + C samen**, met twee wensen: de vlechtpuntjes en het aguayo-streepje "een klein beetje meer" (op 1× net leesbaar, niet overdreven), en het voormalige verre oog moet een **smalle zwarte streep op de neusbrug** worden in plaats van een half oog. Het nabije oog (met glans) en de rest van ronde 13 staan er pixel voor pixel in; alle wijzigingen zijn een overlay op `bron/r13_f1.txt`/`r13_f2.txt` in `bron/bouw15.py`. Geen nieuwe kleuren.

## Wijzigingen (coördinaten = frame 1, x/y vanaf 0; frame 2: kop y ≤ 22 zakt 1 px, hals blijft)
| Onderdeel | Ronde 14 | Ronde 15 |
|---|---|---|
| **Vlechtje verre oor** | plukje x15–16 y9–12 | 2 px langer: x15–16 y9–13, onderkant K op (15,14) tegen de kopomtrek; **knoopje** van rode wol op y12 (`S r`, dezelfde wol als de vuisten), daaronder nog een kwastje w. |
| **Vlechtje nabije oor** | plukje x34 y10–11 | loopt door als strengetje x35 y12–14 langs de kop (schaduwkant: `v`, knoopje `r` op y13), omlijning K op x36 en (35,15). |
| **Aguayo-band** | 4 px `MYTs` + 3 px schaduw | 6 px breed (x23–28 y26 `MYTYTs`) met een tweede rijtje magenta eronder (x23–27 y27 `vMMMs`) zoals de manchetten, en schaduw `vvv` op y28: leest als gebreide band in de wol. Nog steeds geen volle kraag (dat is fase 2). |
| **Neusstreep** | verre oog 2×4 zwart (x19–20 y14–17) | oude oogplek wordt wol (w); een 1-px lijn volgt de neusbrug: (19,13) (19,14) (18,15) (16–17,16), curve 2-1-2 (verticaal, neutraal, horizontaal). |

46 px gewijzigd t.o.v. ronde 13; oppervlak 945 (ronde 13: 923).

## Neusstreep: proeven
Acht proeven (S1–S8, niet bewaard). Zolang de streep op de oude oogplek bleef (x19–20), las hij als dichtgeknepen oog of knipoog, ook als 1 px dunne diagonaal. Pas 1 px verder naar de omtrek toe, beginnend boven op het voorhoofd en doorlopend tot boven op de snuit, leest hij als neusbrug.

## Checklist (§0)
1. **Lijf én blik diagonaal:** ok, ongewijzigd t.o.v. ronde 13. De neusstreep versterkt de 3/4-kop (de snuit steekt voor de verre kant).
2. **Ledematen, oren en ogen geteld en verbonden:** ok. Het verre oog is bewust vervangen door de neusbrug (wens Jordi); het verre oog zit nu achter de snuit. Beide vlechtjes hangen aan de oorbasis vast. `bouw15.py`: geen open randen in frame 1 en 2.
3. **Geen rechte lijnen in een ronde omtrek:** ok, als ronde 13. De neusstreep is een curve 2-1-2 zonder hoek; het strengetje rechts is 3 px recht, maar het is een hangende streng, geen ronde omtrek.
4. **Ogen geïntegreerd:** ok, nabije oog onaangeraakt (glans binnen het zwart, reflectie B).
5. **Silhouet op 1×:** ok, nauwelijks veranderd (alleen de twee vlechtjes steken 1 px uit). Band en knoopjes zijn op 1× zichtbaar als kleurpuntjes, zie `compare.png`.
6. **Formaat:** 945 px, binnen 870–950.
7. **Pose niet stijf:** ok, ongewijzigd.

## Bestanden
- `anim_front.png` (64×128, 2 frames, 16 kleuren, index 0 transparant), `normal.pal`
- `compare.png`: ronde 13, ronde 14 B+C (samengevoegd), ronde 15 frame 1 en 2; op wit en gevechtsgrond, 1× en 3×, plus 4×-uitsnede van kop en hals.
- `bron/`: `palet.txt`, `r13_f1.txt`/`r13_f2.txt` (ronde 13), `r15_f1.txt`/`r15_f2.txt` (resultaat), `bouw15.py`, `vergelijk15.py`. Vanuit de repo-root:
  - `python3 docs/concept/sprites/alpaca/ronde15/bron/bouw15.py`
  - `python3 docs/concept/sprites/alpaca/ronde15/bron/vergelijk15.py`

## Lessen
- **Een donker vlekje op de plek van een oog blijft een oog**, hoe dun ook (1-px diagonaal las als knipoog); om het als neusbrug te laten lezen moet de lijn van de oogplek weg, richting de omtrek, en doorlopen van voorhoofd tot snuit.
- **Een knoopje in een andere wolkleur (rood, zoals de vuisten) maakt een plukje een vlecht** met 1 px; langer maken alleen leest als langere wang.
- **Een gekleurd streepje leest als gebreide band zodra het het patroon van een bestaande band herhaalt** (hier: rijtje geel/turquoise boven een rijtje magenta, zoals de manchet).
- **Een combinatie van twee varianten (B+C) in de vergelijking zelf samenstellen** uit de verschillen met de basis (`vergelijk15.py`), zodat er geen extra variantmap nodig is.

## Oordeel Jordi (23 okt)
Neusstreep weg ("had het meer horizontaal in gedachten, maar kan prima zonder"); verre oogplek is nu gewoon wol. Sprite verder **goedgekeurd** ("prima").

## Reparatie linkervoorpoot
Jordi (23 okt): "De linkerarm is nog een beetje slordig: die zit vast aan een ander en is breder." De nabije voorpoot (x17-24, y41-43, beide frames) is nu 4 px breed (`V W v K`) zoals de verre voorpoot, schuin 1 px per rij naar de manchet, met op y43 1 px uitloop (`VWwvK`) zoals de verre poot in zijn manchet uitloopt. Tussen de poten nu 3 kolommen lucht; beide poten zitten apart aan de borst (y39). Vuist, manchet en al het andere pixel voor pixel gelijk. Vastgelegd als overlay `POOT` in `bron/bouw15.py` (`_` = transparant maken); geen open randen. Voor/na: `compare_poot.png` (1× en 4× uitsnede x12-35, y36-55).

## Reparatie na keuring
Alleen de twee "nodig"-punten uit `KEURING.md`, beide frames, als overlay `KEURING` in `bron/bouw15.py` (11 px per frame; al het andere pixel voor pixel gelijk, polijstpunten niet gedaan):
- **Open randen dicht met K**, silhouet gelijk: buik (25,39)-(26,39), kaak (19,22) (frame 2: (19,23)), kont-hoek (42,37) (nieuwe pixel), staartonderkant (43-45,30). Daarmee is ook het gaatje dicht en zit de staart vast aan de kont.
- **Verre achtervoet los:** eigen afgerond hoefje op x38-41 ((38,46) K, (39-40,47) K, (38,47) leeg) en een kolom lucht op x37 vanaf y44. De aanraking bij de hak (y43) blijft.
- **Randcontrole verscherpt:** v en u gelden nu alleen aan de lichtkant als rand; grenzen ze rechts of onder aan transparant, dan meldt `bouw15.py` een open rand. Op de oude sprite vond hij precies de 7 plekken uit de keuring; nu: geen meldingen.
- Voor/na: `compare_keuring.png` (1× en 4×, plekken omkaderd).

## Staart lager
Jordi (23 okt): staartje "lager, zoals bij een echte alpaca". Het vlaggetje (x41-46 y25-30) is weg; de rug loopt via K (40-42,29) door in een kort wollig plukje (W/w/v/u, bovenrand V, onder/rechts K) dat net onder de rugkromming aanzet (y30), tegen de kont omlaag en iets naar achteren hangt, punt op (44,35); vast aan de kont via de omlijning op x43, 12 px vulling (was ±12), beide frames. Overlay `STAART` in `bron/bouw15.py`, rest pixel voor pixel gelijk, geen open randen. Voor/na: `compare_staart.png` (1× en 4× uitsnede x34-49, y22-39).
