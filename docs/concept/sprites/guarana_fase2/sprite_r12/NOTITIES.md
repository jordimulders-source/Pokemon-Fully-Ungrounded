# Guaraná fase 2, ronde 12 (start r11): roodverdeling naar fase 1

Jordi: "fase 2 is toch nog iets anders in kleurtinten"; akkoord met tinten naar fase 1: "ja, maar zorg ervoor dat het geen blur wordt".

Bestanden: `guarana2_r12.png`, `normal.pal` (= r11), `voor_jordi_r12_8x.png` (fase 1 | r12 | r11, 8×, wit), `afstand.png` (fase 1 | r12 | r11 op 1×, dan 2×).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r12/bouw12.py && python3 sprite_r12/vel12.py`. `los.py A B` = losse tintpixels (geen 8-buur van dezelfde tint) nieuw in B.

## Verdeling van het rood (lijnrood / schaduw / midden / licht, % van alle rode pixels)
| | lijn | schaduw | midden | licht |
|---|---|---|---|---|
| fase 1 (161 px) | 39 | 17 | 34 | 11 |
| r11 (443 px) | 44,9 | 19,9 | 26,6 | 8,6 |
| **r12** (443 px) | **39,7** | **17,6** | **34,1** | **8,6** |
Doel ±40/15/35/10 (±3 %): alles binnen de marge.

## Wat er veranderd is (56 px, alleen roodtinten; groen, ogen en silhouet gelijk, assert)
- 23 × lijnrood → schaduw: naden binnen de tros. Lijnrood blijft op de buitenrand en tegen het blad, in de schil om oogwit/pupil,
  tegen zwart, en op naden waarvan beide kanten al schaduw/lijn zijn (anders verdwijnt de grens). Een naadpixel die los zou komen
  te staan bleef lijnrood.
- 33 × schaduw → midden: schaduw alleen nog als sikkel rechtsonder (de pixel rechts of onder is een grens); waar de sikkel 2 dik was,
  wordt de binnenste midden. Een schaduwpixel die daardoor los kwam te staan kreeg zijn buur terug (sikkel van 2 px, geen stip).
- Hooglicht niet veranderd (8,6 %, binnen de marge).

## Geen blur (gecontroleerd)
- Geen nieuwe tinten, geen dithering; losse S/M/H-pixels: r11 18 → r12 14, geen nieuwe.
- Elke vruchtgrens houdt minstens één tintstap: midden raakt overal een naad (lijnrood of schaduw), nergens midden naast midden waar
  in r11 een naad lag (naden gaan alleen van lijnrood naar schaduw, nooit naar midden).
- Zelf bekeken op 1×, 2× en 8× naast fase 1 en r11: warmer en lichter, dichter bij fase 1; de vruchten blijven op 2× losse bollen.
  Geen plek gevonden die vager leest dan r11. Niet keurder-getoetst.
