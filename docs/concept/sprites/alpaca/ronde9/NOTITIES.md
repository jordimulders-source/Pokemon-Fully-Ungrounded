# Alpaca fase 1, ronde 9: afmaken en repareren (basis ronde 8)

Geen nieuw ontwerp: ronde 8 is met de hand bijgewerkt in de tekstrasters (`bron/delen.txt`, per lichaamsdeel, achter naar voor). Handschoenen ongewijzigd (Jordi: prima).

## Analyse: gids tegen echte Gen 3 (pixelniveau) en onze ronde 8
Bekeken: Eevee, Mareep, Teddiursa (en Skitty/Ponyta op 1×); gids: *Shading* (evenaar, slagschaduw), *Shine* (kraalogen), *Textures* (vacht), *Outline shading*.

| Regel (gids) | Echte Pokémon | Ronde 8 | Wat ik veranderde |
|---|---|---|---|
| Kraalogen: glans + gekleurde reflectie, klein en laag | Eevee: ogen 2–3 breed × 4–5 hoog, één witte glanspixel, ±8 px uit elkaar, in de onderste helft van het gezicht; ooglid in vachtomlijning (geen zwart) | 3×6 en 4×6 rechthoekige zwarte blokken midden in het gezicht | Ogen 2×5 (ver) en 3×5 (dichtbij), schuin ovaal, glans linksboven, blauwe reflectie rechtsonder, lidpixel in vachtomlijning aan de buitenkant; iets lager en naar links geschoven |
| 3/4-aanzicht | Eevee/Teddiursa: gezicht bijna frontaal, maar de gezichtslijn ligt links van het midden; verre kant smaller | Gezicht frontaal en symmetrisch, rechte wangen (x14, x34) | Ogen en mondje 1–2 px naar links, verre oog smaller, snuitbolling linksonder, ronde wangen (geen rechte stukken > 4 px) |
| Vacht/wol: gekartelde rand en schaduwgrens | Mareep: bulten van 4–6 px met inkepingen van 1–2 px rondom, ook onderaan; schaduwgrens rafelig | Bulten vooral boven, gladde achterkant en een rechte onderrand van 12 px | Drie bulten boven, drie aan de achterkant (inkepingen 2 px), drie onderaan rond de poten, krulnaden; schaduwgrens rafelig |
| Ledematen met gewrichten | Mareep/Eevee: achterpoten met zichtbare hak (knik naar achter) | Achterpoten rechte stokjes | Achterpoot: schuin naar achter, hak, recht omlaag, hoef naar voren; verre poot 1 px hoger en donkerder |
| Alles afgemaakt en gesloten | Oren van Eevee/Teddiursa: doorlopende omlijning, voet achter de kop | Oren rechte plakken met open voet (randpixels zonder omlijning) | Bananenvormige oren, gebogen randen, gesloten voet achter de kuif, roze binnenkant |
| Omlijning per kleurgroep | Gen 3: zwart-aandeel 0,35–0,6 | 0,53 | 0,50 |

## Controle (checklist)
- [x] Tellen: 4 poten (2 handschoenen, 2 achterpoten), 2 oren, 2 ogen, 1 mond (klein 'v'-tje), geen staart (ontwerp).
- [x] Omtrek dicht: geen randpixels zonder omlijningskleur (gecontroleerd met `bouw9.py`); alle delen sluiten aan op het lijf.
- [x] Geen recht stuk > 4 px in organische vormen. Over: onderkanten van handschoenen/hoeven (staan op de grond) en de zijkant van de voorste handschoen (ongewijzigd, Jordi tevreden).
- [x] Zwart-aandeel rand **0,50**.
- [ ] Oppervlak **1210 px** (ronde 8: 1130): boven het doel van ±800–950, door de grotere wolbulten en langere achterpoten. Kleiner maken vraagt een herschaling van de hele sprite; niet gedaan om de basis van ronde 8 te houden.
- [x] 64×64, 2 frames (frame 2: kop, kuif en oren 1 px omlaag), 16 kleuren, index 0 transparant.

## Bestanden
- `anim_front.png`, `normal.pal`, `compare.png` (ronde 8, ronde 9, Eevee, Mareep, Teddiursa; 1× en 3×).
- `bron/delen.txt` (handgetekende delen), `bron/palet.txt`, `bron/raster_f1.txt`/`raster_f2.txt` (resultaat), `bron/bouw9.py` (samenvoegen + controles: oppervlak, zwart-aandeel, open randen, rechte stukken), `bron/zet.py` (zet met de hand geschreven pixelrijen in een deel), `bron/patches/` (de handwerk-rijen van deze ronde), `bron/vergelijk9.py`.
