# Gnomad sprite r8: zwart omlaag in 4 zones (22 nov)

Bron: `../af/gnomad.png`. Script: `r8.py` (bewijst: 43 pixels gewijzigd, allemaal van zwart, allemaal binnen de 4 zones; diff 0 erbuiten; silhouet gelijk; riem en gesp 0 gewijzigd). Alleen bestaande paletkleuren: 6 = donkerste roze (172,72,102), c = crème-schaduw (218,198,158), e = bruine haar-/snorselout (174,130,90).

Jordi: "rechtsonderin in de snor zijn wat onnodige zwarte pixels, evenals onderin de rechtse haarpluk, aan de linkerkant de hand en arm, rechteram, zijn echt veel zwarte pixels nog, kijk daar strenger naar, ook dragonflycave" · "als de zwarte lijnen nodig zijn, behouden, maar ik vraag me dat echt af".

Regel (Dragonfly Cave): binnenlijnen (snor tegen huid, arm tegen lijf, hand tegen arm, pluk tegen schouder) in de donkerste tint van het vlak; buitenlijn aan de lichtkant (boven/links) = selout 6; zwart alleen aan de schaduwkant (onder/rechts) tegen de achtergrond; dubbele lijnen naar 1 px.

| Zone (kader x0,y0–x1,y1) | zwart vóór | na | gewijzigd |
|---|---|---|---|
| 1 Snor rechtsonder (18,32–33,38) | 24 | 5 | 19 |
| 2 Rechter haarpluk onderkant (34,31–44,35) | 15 | 7 | 8 |
| 3 Linkerhand + -arm (4,38–13,47) | 20 | 12 | 8 |
| 4 Rechterarm + -hand (30,34–49,47, zonder riem) | 42 | 21 | 8 |

(Kaders 1 en 4 overlappen bij de snorpunt (30–32,36–38); die 6 pixels tellen in beide.)
**Zwart totaal: 278/1525 = 18,2 % → 235/1525 = 15,4 %** (Machoke 17,3 · Vigoroth 15,2 · Sudowoodo 14,3).

## Wat er gebeurde
1. **Snor rechtsonder:** hele lijn snor/wang (23,32)–(32,37) → 6 (slagschaduw op de huid); huidspleet tussen de strengen (18–21,36–38) omrand met 6; onderrand snorpunt (30,38) en (22,38) → c, (28,34) en (30,37) → c (dubbele lijn weg).
2. **Rechter haarpluk:** lijn onder de pluk tegen de schouder (35,34) (36,34) (36,35) (38,34) (39,35) (40,35) → 6; binnenkant van de dubbele rand (42,33) → e, (42,31) → c.
3. **Linkerarm/-hand:** lijn arm tegen lijf (13,39–41) → 6, lijn hand tegen arm (10,41–43) → 6, bovenkant hand (8,39) en hoek linksonder (4,45) → 6 (lichtkant, aansluitend op de bestaande selout).
4. **Rechterarm/-hand:** dubbele lijn onder de arm (39–41,40) → 6 (de riemlijn eronder blijft), lijn hand tegen arm (42,39) → 6, bovenkant hand (43,39) (44,39) (46,40) → 6 (was zwart tussen twee selout-pixels), hoek linksonder (42,45) → 6.

## Zwart dat bleef (en waarom)
- Snor-kader: (18–22,33) = onderkant neus, niet de snor (keuring r7: in 6 loopt hij weg in de neusschaduw).
- Haarpluk: (43,30) (43,31) (44,32) (43,33) (44,33) (42,34) (41,35) (42,35) = buitenrand rechtsonder tegen de achtergrond (schaduwkant).
- Linkerhand/-arm: (5,45) (6,46) (7,47) (8,47) (9,46) (10,44) (10,45) (11,43) (12,43) = buitenrand onder/rechts tegen de achtergrond; (13,42) = hoek arm tegen het gaatje naar het lijf (achtergrond); (12,38) (13,38) = onderlijn van de snor links (niet in de opdracht).
- Rechterarm/-hand: (40,36) (42,37) (43,38) = buitenrand schouder/arm rechts; (41,41) (42,41) = onderkant arm tegen achtergrond; (48,41) (49,42–45) (43,46) (48,46) (44–47,47) = buitenrand hand rechts/onder; (37–40,41) = bovenlijn riem (bevroren).

## Controle 1×
Op 1×/3× naast de af-versie: snor leest als eigen crème vorm tegen de roze huid (6-rand), de huidspleet blijft zichtbaar; beide armen lezen tegen het lijf (arm 7 met 6-lijn tegen lijf 8), beide handen lezen als bolletjes los van de arm. Het silhouet is ongewijzigd.

Bestanden: `gnomad.png`, `gnomad_8x.png`, `vergelijk_8x.png` (af | r8 | r8 met gewijzigde pixels cyaan omrand), `r8.py`.
