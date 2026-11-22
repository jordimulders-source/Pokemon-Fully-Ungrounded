# Vuurduivel fase 2, sprite r1

**Sprite:** `vuurduivel2_r1.png` (64×64, 4-bit palet, 13 kleuren + transparant op index 0). Figuur x4–59, y5–62: **56 breed, 58 hoog**, voeten onderin (y62).
**Vel:** `vel.png` = r1 8× | kale reductie 8× | model (natief) op dezelfde schaal; daaronder het gezicht op 12× (model links, sprite rechts, raster met spritecoördinaten); 1× op wit, lichtgroen, donkerblauw, zwart. `vuurduivel2_r1_8x.png` = de sprite op 8× op wit.

## Werkwijze (model overgenomen, niet hertekend; gereedschap van fase 1)
1. `pitch.py` + kamscore: 12,8 / 8,53 / 4,267 zijn veelvouden; de echte cel is **4,267 px (1024/240)**, net als bij fase 1. Celrand x 3,75, y 3,75. `natief.py` → `natief.png`; figuur natief 111×116.
2. `reductie.py`: exact 2× (fase x+0, y+0; die hield het rode oog). Klasse per natieve pixel = dichtstbijzijnde modelkleur. Achtergrond = licht en verbonden met de rand **plus de drie ingesloten witte modelgaten** (binnen de grote hoornkrul 94 px, tussen arm en romp 105 px, binnen de staartkrul 32 px); gecontroleerd, alle drie blijven gat. Spritepixel = figuur bij ≥2 van 4 (vuur al bij 1). Zwart als ≥2 zwart, anders meerderheid (gelijk: donkerste, in vuur lichtste).
3. `schoon.py`: middenrood → oranjerood/rood naar de buren, losse pixels op in de buren, vlamvlekjes < 3 px binnenin op in de vlam (punten aan de rand blijven), buitenlijn 1 px zwart; vlammen krijgen een tint donkerder als rand (model heeft daar geen zwarte lijn). → `kaal.png` / `raster_auto.txt`.
4. `wijzig.py` + `wijzig_extra.py`: reparaties per pixel met reden → `raster_r1.txt`, lijst in `wijzigingen.txt`. `bouw.py` → png. `controle.py` → kleuren, vlekjes, losse zwarte pixels, lichte kleur op de buitenrand (geen).

Palet (gemeten op het model): zwart 3,1,1 · lijf 22,22,22 / 40,40,40 · bruin 50,40,34 / 80,64,52 / 124,97,77 (hoorns donker+midden, benen/hand midden+licht) · crème 218,184,134 / 240,229,186 · vuur 105,20,22 / 138,30,34 / 205,75,50 / 240,135,62 / 250,205,110 (rood ook voor oog en haar). 2 indexen vrij.

## Pixels die niet uit de kale reductie komen (45 van 1992)
Allemaal naar de natieve modelcellen:
- **Oog (7):** de losse-pixelregel at het rode oog op. Bovenlid (27,18) zwart; iris (27,19) en (27,20) rood, pupil (28,19) en (28,20) donkerrood, lichte oogrand rechts (29,19) crème en (29,20) crème-schaduw. Het model heeft geen witte pupilpixel, dus die is er niet.
- **Hand (12):** de regel "zwart bij ≥2 van 4" maakte de vingers zwart. Met "≥3 van 4" komt de bruine hand van het model terug: (5–6,29), (5–7,30), (6–9,31), (6–8,32) in licht- en middenbruin, met de donkere vingerscheidingen van het model.
- **Vonk boven de handvlam (3):** (9,17), (9,18) oranjerood, (10,18) oranje; de randregel had er zwart van gemaakt.
- **Kleine hoornhaak links van het gezicht (5):** (16,18), (16,20), (17,21), (18,21) middenbruin, (17,20) donkerbruin; de hoorn was zwart/donkergrijs geworden.
- **Opschoning (2):** (26,21) los crème-puntje → crème-schaduw; (55,44) staartvlamhart viel in de crèmeklasse → geel.
- **Selout lichtkant benen/hoeven (17):** linksboven op de benen een tint donkerder dan het vlak eronder in plaats van zwart (Gen 3-eis; het model heeft daar zwart): middenbruin op (14,43), (15,43), (12,44), (11,45), (10,47), (17,56), (16,57), (15,58); donkerbruin op (19,43), (20–22,44), (23–24,45), (10,48), (10,49), (11,50).

Verder niets getekend: gezicht (crème bles, zwart masker, mond), hoorns met ringen, haarvlammen, lijf, arm, staart, staartvlam en benen komen uit de reductie.

## Zelf geziene zwakke punten
- **Oog** is 2×2 rood + crème rechts: dat is wat het model op 2× geeft. Leest als rood oog, maar minder amandelvormig dan in het model.
- **Vlammen** (hand, staart, haar) hebben tintvlekjes < 3 px (model is daar gevlekt). Niet verder gladgestreken om het model te volgen; een keurder kan wegen of dit te rommelig is.
- **Zwarte binnenlijnen** in hoorns (ringen), lijf en benen staan als losse zwarte pixels in donkere vlakken; het zijn modellijnen (hoornringen, plooien). Op 1× onzichtbaar tot klein.
- **Lijf** is vooral 22-grijs met 40-grijs lichtvlakken van het model; arm leest tegen de romp door de zwarte lijn. Volume is beperkt tot wat het model heeft.
- Benen hebben twee tinten (licht/midden) plus selout; het model heeft daar ook weinig donkere schaduw.
