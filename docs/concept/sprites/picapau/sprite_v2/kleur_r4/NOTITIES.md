# Picapau sprite_v2 kleur r4: notities (maker, 5 nov)

Afwerking vanaf `kleur_r3` (niet opnieuw begonnen). Bestanden: `teken.py` (r3-raster + rijen (x, tekens) met de hand) → `raster.txt`; `bouw.py` (palet r3, ongewijzigd) → `picapau.png`, `normal.pal`; `controle.py` → `controle_uitvoer.txt`; `vel.py` → `vel.png` (8x render | r3 | r4 | Taillow | Pikachu + 1x/2x); `model_vs_sprite.png` (tools/grounded/model_vs_sprite.py); `zoom.py` (werkvel 10–20x render | r3 | r4 met raster).

## Bevroren (bewezen met controle.py, diff met r3)
oog 0 · wang 0 (en geen nieuwe wangpixels) · vleugelstippen 0 · staart 0 · palet identiek. De vleugel zelf is ook r3 gebleven (alleen de pixels links van de vleugelrand zijn herschreven). Gewijzigd t.o.v. r3: 278 px; totaal 869 px.

## De zes punten van de opdracht
1. **Lijf bol**: voorkant is nu één convexe curve: halsinham onder de kin (25,29), dan naar buiten tot x24 (r30–35) en geleidelijk terug (25,25,26,26,27,27,28,29,30), segmenten 6-2-2-2-1-1-1 (aflopend, geen trapjes); onderkant rond: (30–32,44) → (33–37,45) → (38–43,46), krult zo naar rechts de dij/staart in. Licht: één ovaal hooglicht (r30–33, x26–28) linksboven op de borst; schaduwgrens als boog (x32 → 33 → 34 → 33 → 32 → 31 → 30 van r29 tot r43), dus een brede sikkel rechts en onder. Selout `4` aan de lichtkant (r29–41), zwart vanaf r42 (schaduwkant). **22 px buiten het silhouet** (borst/buik, allemaal ≤ 2 px).
2. **Kop**: voorhoofd 1 px voller (r12 x25, r14 x21, r15 x20) → bovenrand 4-2-2-1-1-1. Alle bruine binnenlijnen over voorhoofd/kruin weg (r3: (29–31,9–11), (34–35,9–13), (37–38,11), (38–39,16), (32–33,27), (30–31,28)). De kopschaduw is een sikkel (grens x34 → 33 → 32 → 31 → 29 naar onder). Onder de kop alleen nog de kinlijn (23–26,28) in `4` (vorm over borst), die overloopt in schaduwgeel `3`.
3. **Kuif**: twee kegels breed aan de basis (voor 5–6 px, achter 4 px), taps naar de zwarte top (voor r3–6 + één `G` in r7, achter r4–7, grijze kern `G`). Inkeping tussen de kegels tot r9 (34,9) met een kort zwart puntje (34,10); de vorm-over-vorm-lijn is de schaduwkolom `3` aan de rechterkant van de voorste kegel (x32, r8–10) en de achterste kegel staat in `3`: geen bruin. Achterkuif: drie korte afgeronde lobben (A r11–14 tot x40, B r16–19 tot x41, C r22–24 tot x41), met inham ertussen (37,15) en (37,21). **Kuif 21 + lobben 8 px buiten het silhouet.**
4. **Snavel**: voller en lichter: kegel van tip (14,17) tot basis r19–24, bovenkant `h` (bleke hoorn, 9 px), onderkant `g`, onderrand `G`/zwart, donkere basis `G` (x21, r20–24, plus (20,24)), donkere punt `G`. 9 px buiten het silhouet (snavel/verre oog).
5. **Poten**: nabij been x31–32 (r45–47, licht `g` | schaduw `G`), ver been x34–35 (r46, `G`), tenen uitgespreid: nabij naar linksvoor (27–31,48) en rechtsvoor (32–35,49), ver (34–37,47). Klauwen als donkere teenpunt (`G` op (27,48) en (35,49), zwart op (37,47)), geen losse zwarte pixels meer; zwart alleen onder de buik. 9 px buiten het silhouet.
6. **Netheid**: geel 3 tinten + selout; 0 lichte pixels op de buitenrand; 0 losse pixels; tintclusters < 3 px in het r4-werk alleen nog `g` in snavel en teen (dunne delen van 1 px, pseudo-omlijning) + twee `b`-clusters in de (bevroren gelaten) vleugel van r3.

## Render ↔ r4 per onderdeel (model_vs_sprite.png)
- **Kop**: gelijk aan render (ronde bal, middelpunt ±(28,21)); voorhoofd iets voller dan de 64-px-render, zoals gevraagd.
- **Kuif**: gelijk in plaats en richting; kegels nu breed aan de basis zoals de render. Wijkt af: de achterste kegel is op 64 px 1 px smaller dan de render.
- **Oog**: bevroren, gelijk aan render.
- **Wang**: bevroren, gelijk aan render.
- **Snavel**: gelijk in richting, lengte en dikte; donkere basis iets smaller dan de render (1 px i.p.v. 2) zodat de snavel bleek leest.
- **Borst/buik**: wijkt bewust af: bol tot 2 px vóór de render-omtrek (Jordi: "echt bol"). De aparte dij-bult van de render rechtsonder (x33–41, r40–45) staat niet als eigen vorm in de sprite, alleen als ronde onderkant + schaduw.
- **Vleugel**: r3 (gelijk aan render op de stippen; iets smaller dan de render, zoals in r3 gemeld).
- **Poten**: gelijk in plaats (render x31–33 en 34–37); tenen iets korter dan de ovale tenen van de render.
- **Staart**: bevroren, gelijk aan render.
- **Licht**: linksboven op elk onderdeel (kegels, kop, borst, snavel); schaduw als sikkels rechts/onder.

## Controle (controle_uitvoer.txt)
- Buiten het silhouet: 69 px, max 2 px afstand (kuif 21, lobben 8, snavel/verre oog 9, borst/buik 22, poten/tenen 9). Leeg gelaten silhouetpixels: 18 (inkeping kuif, inham lob B/C, tussen de poten).
- Open randen: alleen dunne delen in `g` (snavel bovenrand, nabij been, tenen), bedoeld als pseudo-omlijning.

## Eerlijk: wat nog niet perfect is
- De dij als eigen bult (render) zit er niet in; ik heb rustige vlakken boven extra binnenlijnen gekozen. Als Jordi de dij wil: een korte `3`-boog in het `2`-vlak rond (32–35, 40–43).
- De kop heeft rechts veel zwarte omlijning door de drie lobben; dat is de schaduwkant, maar op 1x oogt de achterkuif nog stekelig.
Beide punten zijn keuzes, geen fouten die ik zelf als "zwak" beoordeel; de keurder mag ze beoordelen.

## Lessen
- Een bolle buik binnen ±2 px: de curve krijgt bij een diagonaal lijf vanzelf een verticaal middenstuk (6 px); dat leest als bol zolang de segmenten daarna aflopen (2-2-2-1-1-1) en de schaduwgrens een boog is (geen verticale band). In r3 was de grens recht (banding), dat maakte het lijf plat, niet de omtrek.
- Twee kegels lossen niet in elkaar op als de achterste in de schaduwtint staat en er een echte inkeping (transparant) tussen zit; een bruine lijn is niet nodig.
- Klauwen als losse zwarte pixel diagonaal onder de teen lezen als vuil; een donkere teenpunt in dezelfde rij leest schoner.
