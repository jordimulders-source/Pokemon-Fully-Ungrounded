# Gnomini sprite r7, variant C (22 nov)

Bron: `../sprite_r6/gnomini_A.png`. Opdracht: geen egale tint rond de neus; lijnen lopen met het licht linksboven mee door meerdere tinten (belichte kant middentint, naar onder/rechts outline base), zwart alleen op het diepste punt (zoals B).
Script `r7.py`; silhouet en palet diff 0 (assert); 20 pixels gewijzigd t.o.v. A. **Zwart: af 14,8 % → C 8,8 % (83 px).**

- **Mutsrand over de neus:** linkerhelft (21,35), (22,35), (23,34), (24,34) 2 → 3; rechterhelft en de rand over het lijf blijven 2.
- **Neus:** linkerkant (20,36..38) 6 → 7, (20,39..40) en onderkant/rechterkant 6, rechtsonder (28,40), (29,40) zwart.
- **Linkerarm:** (18,40), (15,42), (15,43) 6 → 7 (bij de bestaande 7 op (17,40), (16,41)); onderkant blijft zwart (schaduwkant). **Rechterarm:** (45,41) 6 → 7.
- **Broek/voetjes:** (20,47), (21,48), (22,51), (19,52), (18,53), (23,51) a → b (belichte kant); lager en rechts a; kier (40,52) zwart.
- Overgangen 7→6→zwart en b→a→zwart lopen in één richting, nergens om en om.
Bestanden: `gnomini_C.png`, `vergelijk_8x.png` (af | r6-B | C), `strook_1x.png` (af, B, C op zwart/wit, 1× en 3×).
