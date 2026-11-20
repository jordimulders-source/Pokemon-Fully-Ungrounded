# Eindkeuring Moonkey r3 (19 nov, Dragonfly Cave: kleur, schaduw, uitvoering)
Op 8×/14× naast Persian, Mightyena, Absol, Linoone, Aipom; indexen `r3/normal.pal`. Toepassen: `python3 wissels.py ../anim_front.png uit.png` (beide frames, controleert oude waarden; `--zonder8` laat de optionele 8 weg). Preview `voorstel_8x.png` (huidig | gerepareerd | rood gemarkeerd; 1× op licht en donker).
**Goed:** licht linksboven overal consistent (5 op schouder/rug/staart links, 3 rechts); schaduw op flank/heup is een sikkel (x41–42 boven, x43–46 midden, buigt onderaan naar x39); staart als buis 2-5-4-3-1; verre voorpoot (x30–35) en verre achterpoot in 3; luma 1/2/3/4/5/6 = 24/44/61/83/120/151: 4→5 = 37 (Aipom-niveau 32–42), 3→4 = 23 (krap, maar oud goedgekeurd palet). Geen banding of pillow shading op de romp; leest op 1× op licht en donker. Maan (x12-as) technisch in orde.

| # | Prio | Zone, pixels | Probleem | Wissel |
|---|---|---|---|---|
| 1 | hoog | staartkrul boven (51,10),(52,10),(49,11),(50,11) | open buitenrand: 3 tegen de lucht zonder lijn, lichtkant (oude sprite: 2) | 3→2 |
| 2 | midden | rug linksboven (20,29); nabije voorpoot links (22,55) | open buitenrand (3 zonder lijn) | 3→2 |
| 3 | midden | rugrand (37,29),(38,29) | selout 2-2-1-1-2-2 = zwart en lila om en om op de lichtkant | 1→2 |
| 4 | laag | naad kop/rug (21,36),(22,37) | lijn 2-2-1-1-2-2-1: niet taps | 1→2 (zwart pas vanaf (25,38)) |
| 5 | laag | staartvoet (40,33),(40,34) | los 2-px 4-strookje tussen lijn x39 en streep/lavendel | (40,33) 4→F, (40,34) 4→6 |
| 6 | laag | achterpoot onder buiklijn (42–44,55) | 5 direct onder de buik (slagschaduw), 5 naast 3 slaat 4 over; oud = 4 | 5→4 |
| 7 | laag | verre voorpoot (11,58),(12,58) | 2-px 4-vlekje in de schaduwpoot | 4→3 |
| 8 | optioneel | heup (38,44),(39,44),(38,45),(37,46),(38,46),(37,47) | heup is één vlak 4 (±10×10), volume alleen via de 3-boog | 4→5 (kleine sikkel langs dijlijn x36) |

Ter info (geen fout): voeten hebben de bruine E als buitenrand en D op (6,58) (uit de oude sprite); de 3-strook naast lijn x23–24 op de nabije voorpoot is slagschaduw van de kop (klopt); onderranden buik recht (model).
**Eindoordeel:** nu al goed; na 1–3 (8 px) technisch schoon, na 1–7 (17 px) een uitstekende Gen 3-sprite, in uitvoering gelijkwaardig aan Aipom/Mightyena. 8 is smaak.
