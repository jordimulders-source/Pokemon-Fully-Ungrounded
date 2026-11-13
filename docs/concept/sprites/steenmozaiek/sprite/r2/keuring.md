# Keuring steenjaguar r2 (onafhankelijke keurder, 13 nov)

Getoetst op de twee eisen uit SPRITE_KERN: (1) trouw aan het model, (2) Gen 3-sprite. Plus de aanvulling van Jordi: "beetje slim met shading omgaan en misschien sommige kleuren verwisselen als dat het model ten goede komt" en "het oog iets gedefinieerder".

Coördinaten = pixels in `steenjaguar_r2.png` (64×64; x 0–63, y 0–63). Paletindex: 1 k, 2 d (DB), 3 q (DR), 4 x, 5 g, 6 a (B0), 7 b (B1), 8 c (B2), 9 r (R0), 10 R (R1), 11 p (R2), 12 e (C0), 13 f (C1), 14 h (C2), 15 w (W).
Modelbewijs = `natief_zonder_wangoog.png` met 2×2-box verkleind naar spritemaat (hulpvel `keuring/naast_box_12x.png`; die uitlijning klopt op ±0 px, beter dan de opgegeven formule).

## Oordeel: NOG NIET (bijna GOED)

Blind op 1× leest het direct als dit model: brullende, sluipende steenkat, open muil met hoektanden, één oog, grote opgerolde staart met zwart puntstuk, alle mozaïekstukken in de juiste kleur op de juiste plek. Silhouet, pose, poten en staart liggen binnen ±1 px op het model; dit is een sprite die je Jordi kunt laten zien. Wat ontbreekt is klein: het oog is op 1× bijna weg (de glans is grijs g, 118 helderheid, en zit aan de rand), de onderste tandenrij staat één rij te laag, één lila stuk in de voorpoot is crème geworden en de borst onder de kop is te licht voor een schaduwzone. 18 pixels lossen de MOET-lijst op (`keuring/voorstel_moet.png`); met MAG erbij 25 (`keuring/voorstel_moet_mag.png`, 8×: `voorstel_moet_mag_8x.png`).

## MOET (4)

1. **Oog gedefinieerder** (Jordi's wens; nu: glans g aan de linkerrand, oog leest op 1× als vlekje). Model: (12,19) 2e2e29, (13,19) 020305, (12,20) 1d0f0c, (13,20) 020302, (14,20) 2b2b37 = zwart blok 3×2; de glans in het natieve raster (979991 op model 29,31) valt binnen het oog, niet aan de rand.
   Voorstel (naar het Gen 3-oog van Raikou, `graphics/pokemon/raikou/anim_front_gba.png` rij 16–17: zwart blok met één wit glanspixel ín de pupil, en Absol rij 24–25: wit glanspixel naast rood/zwart):
   - (12,19) g 5 → k 1
   - (13,19) k 1 → w 15
   Resultaat (x 11–15, y 18–21):
   ```
   r2            voorstel
   y18 c c c b b   c c c b b
   y19 c g k k c   c k w k c
   y20 c k k k c   c k k k c
   y21 R R c c c   R R c c c
   ```
   Vergelijking op 16×: `keuring/oog_varianten_16x.png` (links r2, midden dit voorstel, rechts met MAG-wenkbrauw).

2. **Onderste tandenrij één rij te laag.** Model: rij 33 x7–10 = bdc4ce cfd6e0 b6bbc2 979da4 (wit/lichtgrijs, de tandenrij), rij 34 x7–10 = 686676 4b4b63 44445d 42455e (donkere voeg = d). Sprite heeft wit op rij 34 en lila op rij 33.
   - (8,33) c 8 → w 15; (9,33) c 8 → w 15
   - (8,34) w 15 → d 2; (9,34) w 15 → d 2

3. **Lila stuk in de nabije voorpoot is crème/voeg geworden.** Model: (22,41) c1c1e2, (23,41) cfcfee, (24,41) 7b7488, (22,42) bcbce2, (23,42) d4d5f0, (24,43) b3b5df = licht lila (B2); de crème zit links ervan (18–21, 38–41). Sprite heeft hier d/q/h.
   - (22,41) d 2 → c 8; (23,41) q 3 → c 8; (24,41) q 3 → b 7
   - (22,42) d 2 → c 8; (23,42) h 14 → c 8; (24,42) h 14 → c 8; (24,43) h 14 → c 8

4. **Strook R2 onder de nek te licht** (model én shading). Model (23..26,40) = 936857 80594d 7b5449 b67d6a, dat is R1 (158,94,78), niet R2 (196,132,114); het ligt in de schaduw onder de kop.
   - (23,40) (24,40) (25,40) (26,40) p 11 → R 10

(Klein, hoort bij 2: (9,28) c 8 → r 9. Los lila spikkeltje (cluster van 1 px) in de muil; model (9,28) 231313 = donker mondbinnenste.)

## MAG (4)

1. **Wenkbrauw boven het oog** (extra definitie, Absol-achtig donker lijntje boven het oog; model heeft daar lila, dus dit is een bewuste afwijking op Jordi's "oog gedefinieerder"): (12,18) c 8 → a 6; (13,18) c 8 → a 6. Alleen doen als MOET 1 alleen nog te zwak is.
2. **Crème borststuk in schaduw** (licht linksboven; dit stuk zit onder de kop): (19,40) h 14 → f 13; (20,40) h 14 → f 13; (19,41) h 14 → f 13. Het bovenste deel (18–19, 38–39) blijft h, zodat het stuk een licht-naar-schaduw-verloop krijgt dat de borstronding volgt.
3. **Buitenkant staartkrul als schaduwsikkel**: (59,24) b 7 → a 6; (59,25) b 7 → a 6. Model daar 8389b9/8387b7 (B1), dus kleine afwijking, puur voor de ronding van de krul (lichtkant is de binnenzijde met c op (56–57,21)).
4. **Spikkels achter de kop** (losse 1-px tinten, Gen 3-netheid): (23,20) a, (22,21) b, (22,22) a zitten als drie losse stipjes in de x-voeg. Laten staan als het model ze echt zo heeft; anders samenvoegen tot één tint (b 7).

## Gen 3-punten
- Omlijning: overal 1 px k, geen open randen, geen zwart/gekleurd om en om. In orde.
- Tinten: per kleurgroep 3 tinten + voegtint (d, q); voor een mozaïek met voegen correct. De vele 1-px d/q-clusters zijn voegen, geen ruis.
- Licht: kop, rug en voorpoot hebben licht linksboven; borst onder de kop (MOET 4, MAG 2) was de enige echt tegenstrijdige plek.
- Contrast: in orde, behalve de oogglans (g op lichte c, verschil te klein; MOET 1).

## Hulpafbeeldingen (`keuring/`)
`naast_box_12x.png` (sprite naast 2×2-verkleind model), `kop_24x.png`, `naast_10x.png`, `oog_varianten_16x.png`, `varianten_6x.png`, `voorstel_moet.png` (+`_8x`), `voorstel_moet_mag.png` (+`_8x`), `1x_en_4x.png`.
