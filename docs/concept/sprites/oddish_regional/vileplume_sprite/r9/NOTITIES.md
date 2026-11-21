# Vileplume r9: VL/VR met modellijnen (opdracht coördinator), mondjes kleiner. Oordeel: VL/VR NIET beter dan r7

Basis: `r8/vileplume_r8_kroonr7.png` (r7-kroon + gezicht + linkerpoot uit r8). `python3 r9/bouw.py [--mond=M1..M6] [--modus=model|r7|r7lijnen] [--wijd]` vanuit `vileplume_sprite/`.

## Bestanden
- `vileplume_r9.png` (modus model, mond M4, gezicht van Vileplume): hoofdopdracht.
- `alt_r7kroon_nieuwemondjes.png`: kroon van r7 ongewijzigd, alleen de vijf nieuwe mondjes (M4). **Mijn voorkeur.**
- `alt_r7stralen_R0.png`: de r7-stralen van VL/VR in R0 met een bredere buitenkant.
- `vel.png` (r9 | r7 | model 8×; 12× krater, L, VL; **12× gezicht r9 naast Vileplume uit de game**; 12× VR, lijf+poten; onderaan 4×/2×/1×: r9 | alt_r7kroon | alt_r7stralen | r7 | model), `kaal.png`, `lijnen.py` (meting), `uitvoer.txt`.

## Per punt
1. **VL/VR (modus model):** de R0/K-pixels van het natieve model binnen VL/VR (zonder rand en mondring) geprojecteerd op het spriteraster (`lijnen.py`). Per 5° het lijngewicht rond het mondje, de pieken zijn de modellijnen; de sterkste blijven (minstens 22° uit elkaar). Lijnen die minder dan ±33° van de horizontaal lopen zijn geschrapt (dus geen streepjes naast het mondje). Elke lijn is 1 px van net buiten het mondje tot de rand; het buitenste deel van steile lijnen is 2 px. Vulling R3, sikkel R2.
   **Resultaat:** door de grens van 33° blijven er maar 7 (VL) en 5 (VR) lijnen over, want de meeste modellijnen liggen in deze platte schijven vlak. Ze komen als losse brokjes uit en de schijven worden leeg. **Slechter dan r7.** Met de grens op 18° komen er meer lijnen, maar dan krijg je weer de horizontale streepjes. Bij deze schijfvorm (21×11 px) zijn ±9 lijnen zonder horizontale streepjes niet te halen.
2. **Mondjes:** stempels getest: M1/M2 5×2, M3 4×3, M4 5×3, M5 4×2, M6. De 2-rijsvarianten lezen als een boogje of kommetje, niet als ring. **M3 en M4 (ring van R0, hoeken R1, licht binnenin, met een lichte rand van 1 px) lezen als ringetje.** M4 is gekozen; hij is op alle vijf gelijk en rustiger dan het mondje van r7.
3. **Gezicht (Jordi: "neem gewoon de vileplume mond en ogen over en doe ze ver genoeg uit elkaar" / "het gezicht het ALLERBELANGRIJKSTE" / "de ogen dus maar net zichtbaar" = net onder de kroon uit, zoals in de game):** ogen en mond pixel voor pixel uit `graphics/pokemon/vileplume/anim_front.png`: linkeroog 3 px (36,24)(37,24)(37,25), rechteroog 2 px (38,32)(38,33), mond 7 px (39,26)…(40,31). Kleuren naar het dichtstbijzijnde paletnummer: rood (216,72,88) wordt R2, donkerrood (112,24,16) wordt idx 12 (kraterbruin 110,38,47), mondblauw (24,41,74) wordt W0. Geplaatst: linkeroog (32,22)(33,22)(33,23), direct onder de zwarte kroonrand y31; rechteroog (31,31)(31,32), direct onder de kroonrand y30 (onze kroonrand ligt daar 1 rij hoger, dus het rechteroog staat 3 rijen hoger dan in de game). Mond y35–37 x25–30, 3 rijen onder het linkeroog zoals in de game, op de plek van de U uit het model. **Enige wijziging: de ogen staan 9 px uit elkaar in plaats van 8** (linkeroog 1 px extra naar links), naast de aanpassing van de hoogte aan onze kroonrand. Geen glans of andere vorm toegevoegd. Varianten A–E zijn vervallen; dezelfde gezichtspixels staan ook op de twee alt-bestanden.
4. **Linkerpoot en krater** zijn gelijk aan r8; de krater wijkt 0 px af van r7.

## Telling t.o.v. r7 (vileplume_r9.png)
VL/VR-binnenkant 111 px, mondjes achter 31 px, krater 0, gelaat 20 px, linkerpoot 72 px.

## Toets
16 kleuren, index 0 transparant, lichte kleur op de buitenrand 0, zwart 16,9 %. Er zijn 2 losse lijnpixels in VL/VR (17,25) en (32,25), allebei brokjes van de modellijnen.

## Advies
Neem `alt_r7kroon_nieuwemondjes.png` als tussenstand (r7-kroon, die volgens mij beter leest dan alle varianten van r8/r9, met nette mondjes, het Vileplume-gezicht en de poot met knik). Voor VL/VR is een krabbel van Jordi op één schijf nodig met de vingers die hij wil; het genereren en overnemen per script lukte niet in 3 pogingen (r8, r9). Geen keurder gedraaid.
