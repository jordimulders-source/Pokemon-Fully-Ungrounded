# Keuring welp r11 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL, nipt.** Eén MOET van 4 px (neuspunt). Daarna PASS voor de basis; geen nieuwe keurder nodig als alleen die 4 px wijzigen en Claude de kop op 12× naast het model bekijkt.

Werkwijze: eerst blind (8× naast het model, BOX/Lanczos-verkleind naar de sprite-bbox x 7–56 / y 18–62; kop op 12× naast de modeluitsnede; oog per spritecel nagemeten in het model; silhouet-overlay en toonkaart model vs sprite; 1× en 3× naast Growlithe, Vulpix, Skitty (`anim_front_gba`) en `af/steenjaguar.png`; clusterscan per paletindex). Daarna `r10/keuring.md` gelezen en r10→r11 gedifft: 12 px, precies de benoemde.

Paletindex: 1 zwart, 2 (59,34,36), 3 (98,64,60), 4 (136,96,88), 5 (170,128,114), e (204,166,148), 6 lila-donker, 7 lila-mid, 8 lila, 9 oog-licht, a wit, b beige, c/d/f tong.

## Hoofdvraag
Op 1× een duidelijke zittende welp die zijn opgeheven poot likt; formaat en waarde passen naast Growlithe/Vulpix en de volwassen jaguar. Silhouet valt vrijwel exact op het model (overlay: afwijkingen ≤ 1 px, alleen randpixels). Het facettenidee staat: licht voorhoofd en snuitrug, lichte poot en voeten, donkere borst-/buikkant, ronde dij; geen kussen, geen vlekkerige blur. Het oog is trouw aan het model (zwart lid boven, glans linksboven, pupil 1×2, iris boven donkerder, oogwit achteraan) en geeft geen domme blik. Het ver oog is een omsloten oogje (geen losse pixels).
Wat nog stoort naast het model: de snuit eindigt in een rechte verticale rand (x9, y31–34) met de neus als donker blok erin, terwijl het model een neuspunt heeft die 1 px naar voren steekt (silhouet-overlay: model op (8,32) en (8,33)). Dat maakt de kop hoekig/beerachtig in plaats van een welpensnuit. Met die 4 px zou ik hem wel trots laten zien.

## r10-MOET's
| r10 | Uitgevoerd? |
|---|---|
| 1 Neus als driehoek | Deels: bovenrand (9–12,31), vulling 3 (10–11,32), punt (11,33)→philtrum (11,34) staan. Maar (8,32) is weggehaald, zodat de neuspunt uit het model nu ontbreekt (zie MOET 1). |
| 2 Tong breder naar links | Ja: (11,39) c, (11,40) d; tip 3 px, leunt over de poot. Leest als tong. |
| 3 Rand dicht | Ja: (10,36) 2, (12,36) 1, (11,37) 2; geen open rand meer bij tand/tong. |
| MAG iris, bandeinde | Ja: (20,27) 6, (20,20) 8. |

## Eis 1: trouw aan het model
| Onderdeel | Oordeel |
|---|---|
| Silhouet | OK (overlay ≤ 1 px) |
| Oren | OK; ver oor even hoog als in het model (r10-MAG vervalt) |
| Voorhoofdsband | OK in vorm; wat korrelig (MAG) |
| Oog / ver oog | OK, nagemeten per cel |
| Snuit / neus | **AFWIJKING** (MOET 1): neuspunt (8,32–33) ontbreekt |
| Mond, tanden, tong | OK |
| Poot (likt), borst, dij, voeten, staart | OK |
| Toon/volume | OK; tussen voorpoot en dij is het model donkerder (MAG) |
| Spiralen | buiten beoordeling; ontsieren de basis niet, maar lezen als hoekige "e"-tekens (spiraalronde) |

## Eis 2: Gen 3-techniek
- Bruin 4 tinten + e, stappen ±30–35: OK. Buitenlijn 1 px, 61% zwart (102 zwart / 65 index 2), gekleurd aan de lichtkant links/boven, zwart onder: binnen Gen 3 (45–68%).
- Geen open randen, geen pillow shading, geen banding.
- Kleine clusters (< 3 px) vooral in de voorhoofdsband (zie MAG); elders functioneel (lijnen, tanden, oog).

## MOET-reparaties
1. **Neuspunt terug, als driehoek (x8–9, y32–33):** (8,32) transparant → 2; (8,33) transparant → 1; (9,32) 2 → 3; (9,33) 2 → 2 (blijft). Resultaat: bovenrand 2 op (9–12,31) + (8,32), vulling 3 op (9–11,32), schuine onderrand (8,33) 1 → (10,33) 2 → punt (11,33) 1 → philtrum (11,34). Snuit krijgt de ronde neuspunt van het model; op 1× getest (variant naast r11): leest als snuit, niet als stokje.

## MAG-punten
- Voorhoofdsband rustiger: losse 4-pixels (21,21) en (20,22) → 5 (horen bij het lichte voorhoofd); groef-trap (18–19,21),(16–17,22),(14–15,23),(14,24) is een gelijke 2-px-trap: eventueel (14,24) 3 → 8 zodat de groef binnen de band eindigt.
- Volume: schaduwzone tussen voorpoot en dij (x 26–32, y 49–56) is in het model toon 2, in de sprite 3; enkele pixels naar 2 langs de achterkant van de voorpoot geven meer diepte (alleen als het de spiraal niet raakt).
- Rugrand (x 29–44, y 31–41) is zwart aan de bovenkant (lichtkant); index 2 als selout op de bovenste paar pixels zou het zachter maken. Geen must: Gen 3 doet dit ook vaak zwart.
- Spiralen (borst, dij): hoekige "e"-vorm; in de geplande spiraalronde ronder maken naar het model.
