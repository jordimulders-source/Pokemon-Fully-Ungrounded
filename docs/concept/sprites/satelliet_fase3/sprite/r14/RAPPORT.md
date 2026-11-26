# Ruimtestation sprite r14 (25 nov): PF gelijk aan PB

Jordi over r13: "bovenste zie ik geen verschil tussen c en d, dus een van de twee, de onderste heb je precies hetgene wat goed zou zijn geen enkele keer gedaan, dezelfde breedte als boven, 4 pixels tussen de lijnen in".

`herstel14.py` (= herstel13 met vaste keuzes) bouwt opnieuw vanaf r11, met het recept uit `recept.py`.

**Ongewijzigd:**
- de ogen: 0 px verschil;
- PC: pixel-gelijk aan r12;
- de PE-punten zoals in r12.

**Kleuren:** 16 inclusief transparant, transparency=0.

**Uitvoer:**
- `sprite.png` en `sprite_8x.png`;
- `vel.png`: r13-C en r14 op 8×, PB naast PF op 12×, 1×/2× naast fase 2;
- `diff_r11.png` en `log.txt`.

## PB
Gelijk aan r13-C: −2 px verschoven langs de breedterichting (−2,00 / −1,11).

## PF
- **Breedte:** dezelfde breedtevector als PB.
- **Vakken:** precies 4 spritepx lang (4 × 3,515625 modelpx), 5 vakken.
- **Verschuiving:** dezelfde als PB, dus de stok zit even ver in het paneel als bij PB.
- **Tinten:** zoals bij PB: het eerste vak licht (14), de rest 13.
- **Volgorde:** achter de voorbuis en achter PE.

## Gemeten in de sprite

| | breedte | afstand tussen de rasterlijnen |
|---|---|---|
| PB | 6 px (x 32–37: rand, lichte rand, 3 vak, rand) | lijnen op rij 18 en 22 = 4 px (3 vakpixels + lijn) |
| PF | 6 px (x 32–37, onderste stuk) | lijnen op rij 45, (49, 53 achter PE), 57 = 4 px |

## Zichtbare stukken van PF
- **Boven PE:** 21 px, x 34–37, y 41–46. Dat is het eerste vak heel; x 32–33 valt achter de voorbuis.
- **Onder PE:** 37 px, x 32–37, y 54–61. Dat is de volle breedte: het onderste stuk van vak 4, de rasterlijn (rij 56/57) en vak 5 heel, met de bodemrand.
- De onderkant van de sprite ligt nu op y 61 (r11: 55).
