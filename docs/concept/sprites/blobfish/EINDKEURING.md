# Eindkeuring blobfish fase 1: `ogen/ogen_v4_B.png` (Dragonfly Cave, 16 nov)

Getoetst: alleen uitvoering (Gen 3 / Dragonfly Cave-gidsen, SPRITE_KERN, FAKEMON_CHECKLIST E, SPRITING §0/§3–§8). Geen herontwerp; trouw aan het model is in r4 al PASS. Bekeken op 8× en op 1×/2× (licht en donker) naast Magikarp, Feebas, Barboach, Luvdisc en Corsola (`anim_front_gba.png`, bovenste 64×64). Vel: `eindkeuring_vel.png` (links de sprite met aanwijzingen, rechts een voorbeeld ná reparatie 1+2; de sprite zelf is niet gewijzigd).

## Oordeel: PASS, na 2 kleine reparaties (17 px, alleen indexen, alpha-diff 0)

## Reparaties
1. **Tint 8 (mauve) → tint 6, 15 px.** (36,30) (41,30) (34,31) (36,31) (38,31) (40,31) (41,31) (36,32) (38,32) (39,32) (13,33) (33,33) (34,33) (35,33) (36,33): index 8 → 6.
   Waarom: na de lichtronde is 8 (169,68,74) helderheid 99 even licht als lijftint 6 (198,53,56) 97; het verschil is alleen nog hue. Op de rugvin geeft dat een 6-8-6-8-6-8-rij (rij 31, x33–38): een streeppatroon zonder toonstap, op 1× vlekkerig. Model op die pixels: mediaan 93, dichter bij de 6-pixels (84) dan bij 9 (110), dus samenvoegen met 6 is de trouwste keuze. De rugvin houdt zijn stralen via de lichte tint 11 en de donkere diagonaal (39,29) (40,30) (39,31). Palet wordt 9 kleuren + transparant.
   (Alternatief als Jordi de vage strepen wil houden: niet de indexen maar de paletkleur 8 naar ±(186,75,82), helderheid ±110, zelfde hue. Dan blijft wel een tint met een stap van maar ±12 over; daarom niet de eerste keuze.)
2. **Dambord 9/6 op de kop, 2 px.** (23,36) 6 → 9 en (21,37) 6 → 9.
   Waarom: rij 36 x21–24 = 9 6 9 6 en rij 37 x20–23 = 9 6 9 6, een 2×2-dambord op de grens licht/midden van de kop (overblijfsel van de reductie, model daar 94–104, tussen beide tinten). Na de reparatie loopt de grens 9/6 als nette curve: rij 35 tot x26, rij 36 tot x24, rij 37 tot x22, rij 38 tot x19 (segmenten 2-2-3, oplopend, geen besluiteloosheid).

Verder niets aanraken.

## Wat in orde is
- **Buitenlijn:** overal 1 px en gesloten; randpixels alleen zwart (65) en lijnrood (58), nooit een lichte kleur op de rand. Selout (lijnrood) aan de lichte kant linksboven (kop, vinnen), zwart onder en rechts. Script: geen enkele geïsoleerde zwart/lijnrood-wissel langs de rand.
- **Losse zwarte pixels (index 1 zonder transparante buur):** alleen de twee ogen, de mondlijn (8,46)→(12–18,49)→(19,48) en de voorrand van de borstvin (38,43) (38,44), die aansluit op de buitenlijn (39,45). Geen zwarte pixel los midden in een vlak.
- **Licht linksboven:** glans (14–16,34–36) + (13,37) op de kop linksboven, oogglans linksboven, rim-licht op de linkerrand (8,44) (8,45). Schaduw (tint 4) rechtsonder op wang, lijf en staartsteel.
- **Tinten en contrast:** lijf 4 / 6 / 9 = 70 / 97 / 122 (stappen 27 en 25, binnen de ±20–40 die SPRITE_KERN vraagt); lichten 10 / 11 / wit = 134 / 168 / 253. Geen banding (de middentint ligt als overgang, niet parallel aan de omtrek), geen pillow shading (de lichte buikrand onderaan komt uit het model, r4).
- **Kleine clusters:** de 1–2-px-clusters van 4, 10 en 11 zijn vinstralen (diagonale lijnen), lipglans en de schaduw onder de liphoek (20–21,51) (model 73–74): functioneel, geen ruis.
- **Ogen (v4):** zwart 2×2 kraaloog met witte glanspixel linksboven, zelfde opbouw nabij (19–20,45–46) en ver (9–10,41–42). Contrast zwart 23 tegen lijf 70.
- **Formaat:** 848 px, box 50×29: binnen fase 1 (700–950). Op 1× leest hij naast de Gen 3-vissen als vis met lippen en glans; het oog is op 1× klein maar zichtbaar.

## Ter info voor Jordi (geen reparatie)
- Het verre oog raakt de linker buitenlijn (8,41–42); op 1× smelt het met die lijn tot één donker inkepinkje. Dat is de gekozen plek en vorm.
- Dragonfly Cave noemt bij kraalogen naast de witte glans een gekleurde reflectie aan de andere kant; in 2×2 is daar geen plek voor zonder het oog groter te maken.
- Naast Magikarp/Corsola blijft de vis vrij donker (tint 4 is 316 van 848 px); dat is het model (winegum), de lichtronde heeft het contrast al opgehaald.
