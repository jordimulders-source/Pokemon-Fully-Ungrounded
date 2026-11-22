# Vuurduivel fase 2, sprite r4 (vanaf r3)

**Sprite:** `vuurduivel2_r4.png` (64×64, 4-bit, 15 kleuren + transparant op index 0 = vol palet), figuur x4–59, y5–62. `vuurduivel2_r4_8x.png`.
**Vel:** `vel.png` = r4 8× | r3 8× | model. Daaronder op 12× romp + bovenarm (x16–47, y27–44: model | r3 | r4) en de dijbeenrand (model | r3 | r4). Daarna 1× op 4 achtergronden (r4 links, r3 rechts).
**Diff (`diff.txt`):** 49 indexen anders dan r3: romp/bovenarm 42, dijbeen 6, handvlam 1, **buiten de zones 0**.

## MOET: volume romp + bovenarm (`lijf.py`, alleen kleur)
- **Wat verandert:** alleen pixels in x18–46, y29–43 die in r3 lijfgrijs waren (46 of 76). Omlijning, plooien (zwart), manen en benen blijven.
- **Meting:** per spritepixel de gemiddelde luminantie van de natieve modelpixels in een 4×4-venster rond de 2×2-cel. Alleen lijfklassen, zonder lijnpixels (lum ≤ 8). Gemeten bereik 20–40. `python3 lijf.py raster_r3.txt /dev/null --toon` drukt de meting af.
- **Verdeling:**
  - lum < 24 → donker (46,44,44): de sikkel onder de manen, onder de plooien en tegen de benen. Daar is het model het donkerst.
  - lum ≥ 24 → midden (76,72,72): de bolling van de bovenarm/schouder links, de schouder en flank rechts, en de buikband boven de benen. Daar is het model lichter.
  - Hooglicht (105,100,100), nieuw op index 15: alleen in de schouderzone links (x18–24, y32–37) waar lum ≥ 34. Het model is daar het lichtst (35–38, ongeveer gelijk aan de schouder rechts en de buikband). Dat geeft 3 px: (20,34), (19,35) en (20,35).
- **Opschoning:** vlekjes kleiner dan 3 px zijn opgegaan in de buurtint; de controle vindt er in de zone geen meer. Alles is neutraal grijs. Maximaal 3 tinten in de grijsgroep.

## MAG (uit `mag.txt`)
- **Dijbeen links:** de selout is nu één tint donkerbruin (50,40,34). (14,43), (15,43), (12,44), (11,45) en (10,47) gingen van middenbruin naar donkerbruin; de zwarte pixel (10,46) ook naar donkerbruin. (10,48), (10,49) en (11,50) waren al donkerbruin.
- **Handvlam:** (8,20) van rood naar donkerrood, zodat de tongpunt één band is.

## Zelf gezien
- Het model is lichter aan de rechterkant van het lijf (schouder en flank rechts) en in de buikband. Dat staat er nu zo, ook al valt het licht in Gen 3 linksboven. Links komt het licht van de bovenarm met het hooglicht.
- De middentint loopt rechts langs de rand (x40–44). Die strook stond al zo in het model en in r3, en de keurder liet hem toe.
- Het palet is nu vol (15 kleuren + transparant).
