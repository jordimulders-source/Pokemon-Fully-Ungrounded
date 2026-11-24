# Proef: tintzones opnieuw indelen (24 nov)
Jordi (24 nov): "pak eens 4 designs die in jouw ogen het meest hiermee verbeterd kunnen worden en probeer dat eens, met voor/na erbij". "Hiermee" = de stap die Jordi vrijgaf: "Die hoeft voor mij niet verboden te zijn" (tintzones binnen het silhouet opnieuw indelen).

## Lees eerst
- `docs/lessen/SPRITE_KERN.md` (bovenste blok "Tintzones opnieuw indelen mag")
- `docs/concept/sprites/gen3_studie/STUDIE.md` (secties "Blur en te schoon" en "vlekken zonder richting")
- Kijk zelf op 8× naar de Gen 3-maatstaf (echte Gen 3: `graphics/pokemon/<soort>/anim_front_gba.png`, alleen die bestanden; NIET de gewone anim_front.png of fan-made soorten).

## Wat wel / niet
- WEL: binnen het silhouet de tintzones opnieuw indelen. Grillige vlekjes zonder richting (2–6 px, tinten door elkaar) worden zones die de vorm volgen: per vlak één grondtint, licht linksboven op de bolling, schaduw als één zone (sikkel) aan de schaduwkant met een harde grens, donker als korte lijntjes van 1 px die een plooi/vorm/vachtrichting tekenen. Ringen van tinten langs de rand (kussen/airbrush) weg.
- WEL: buitenlijn aan de lichtkant (linksboven) in de donkerste eigen tint van het vlak (selout) i.p.v. zwart; zwart blijft aan de schaduwkant. Kleuren van het palet mogen aangepast worden.
- NIET: silhouet (alfa) veranderen — pixeldiff 0 op de transparantiemasker, met script bewijzen. NIET het gezicht (ogen, mond, neus, tanden en de lijn eromheen) veranderen: bepaal de gezichtszone, bevries die, bewijs diff 0. Geen nieuwe onderdelen, niets weglaten. Niet hertekenen van vormen.
- NIET: per script kwantiseren, middelen, blurren of gladstrijken ("rustiger maken" = pixelblur, verboden). Wijzig per pixel, als tekstraster of met gerichte pixel-lijsten.
- Max 15 kleuren + transparant (index 0), PNG mode P 64×64, zelfde formaat als het origineel.

## Oplevering (in jouw map `docs/concept/sprites/gen3_studie/proef/<naam>/`)
- `na.png` (de sprite), `voor_na.png`: voor | na | Gen 3-maatstaf op 6×, plus dezelfde drie op 1× eronder.
- `RAPPORT.md`: wat je per zone veranderde, aantal gewijzigde pixels per zone, bewijs diff 0 voor silhouet en gezicht, en eerlijk wat je zelf nog zwak vindt.
- Niet committen, niets buiten je map wijzigen. Origineel in `af/` niet aanraken.
