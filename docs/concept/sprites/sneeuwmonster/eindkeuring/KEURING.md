# Sneeuwmonster fase 1: eindkeuring (26 nov)

Bron: `../sprite_r10/sneeuwmonster_r10.png`. Model: `../gemini/r1/r1c.png` (natief raster `../gereedschap/natief.png`).
Opdracht (Jordi): "Eindkeuring = schaduw + belijning + kleurtinten ... dragonflycave". Omlijningsronde volgens de gids (r. 89–91, 400–404, 425–428): outline shadows zwart; "the base outlining shade for every color" voor de rest, "so that the outline is always one pixel wide"; outline highlights "on the outlines in the very most highlighted parts ... on the inside of the outline"; regel 4: "The outlines must be reasonably dark".
Bevroren (index-diff 0, assert in `bouw.py`): silhouet, beide ogen, beide knopen, kuif (y ≤ 17). De r10-zone linksonder van Jordi (x21–28, y47–50) is ook niet aangeraakt.
Vergeleken op 8× en 1× met de maatstaf (Skinguin, Dundragoon, Zapacha, Princadee) en met Gen 3 `_gba`: Snorunt, Wynaut, Spheal, Swablu, Glalie, en voor witte lijven Absol, Dewgong, Seel, Altaria (gemeten palet + randgebruik).

## Oordeel vooraf (r10)
**Kleurtinten.** Gen 3 witte lijven (gemeten): Absol ffffff L255 / dedeee 223 / c5c5d5 198 / 9494ac 150 / outline base 526262 L93 / zwart; Dewgong/Seel e6e6f6 231 / c5cdee 206 / 9ca4bd 164 / outline base 415283 L82 / zwart. r10: w 249 / m 230 / s 197 / 9 162 / l **118** / K 32. Sneeuwtinten zitten goed, twee afwijkingen:
- de lijntint l (outline base én binnenlijnen) is met L118 te licht: Gen 3 gebruikt L82–99 voor de outline base van witte soorten, en de modellijnen zelf zijn L≈85 (natief gemeten). Daardoor leest de sprite op 8× en 1× vaal naast de maatstaf (gids regel 4).
- stap licht → midden is maar 19 (Absol 32, Glalie/Dewgong 24): vlak lijf.
- tint 9 (modelblauw, alleen 5 px in de r10-zone) heeft een iets groenere tint (hue 203) dan de rest van de ramp (≈210).
**Belijning.**
- Dubbele rand (lijntint l direct binnen de zwarte buitenlijn, rand 2 px) rechts op de kop (40,22), (40,28), (40,29) en langs de rechterflank (41,34)–(44,41).
- Zwarte pixel binnen de figuur (23,31) in de nekplooi links (binnenlijn hoort niet zwart).
- Klontje lijntint bovenop de linkerarm (19,37) (lijn 2 px dik).
- Binnenlijnen overal even donker tot hun uiteinde; het model laat ze taps uitlopen (armlijn rechts begint op model L222, voetlijn rechts L168–172).
- Geen outline highlights op de belichte kant.
- Kuif (bevroren): zwart en lijntint om en om op de rand bij (30,12) en (27,15) (beide komen uit het model: donkere inkeping). Zie twijfels.
**Schaduw.** Volgt het model (kop: sikkel rechts en onder; nekschaduw van de kop op het lijf; lijf: licht links, schaduw rechts en onder); grenzen zijn gebogen, geen pillow shading. Enige ruis: twee losse m-pixels (22,28) en (24,29) in de sikkel linksonder de kop.

## Uitgevoerd (`bouw.py`, 25 px index-diff + 3 paletkleuren)
| stap | px | wat |
|---|---|---|
| K1 palet | – | l (88,124,164) L118 → (62,96,140) L90 (outline base en binnenlijnen; Absol/Dewgong-niveau, modellijn L≈85) |
| K2 palet | – | m (214,232,246) L230 → (208,226,244) L222 (stappen nu 26 / 28 / 37 / 67) |
| K3 palet | – | 9 (130,169,194) L162 → (128,164,198) L157 (tint gelijk aan de ramp); 9 is nu de DC-tint "shadows/outline highlights" |
| B1 | 3 | kop rechts: l naast zwart → s (buitenlijn 1 px) |
| B2 | 2 | nekplooi links: zwart (23,31) → l, uiteinde (24,31) → 9 (taps, model L157) |
| B3 | 10 | rechterflank: l naast zwart → 9 (model: armlijn + dunne lichte strook, natief L80–200; de arm blijft leesbaar, rand 1 px zwart); los s-pixel (43,35) → 9; tweede lijnpixel (43,38) → s |
| B4 | 1 | armlijn rechts begint taps: (36,36) → 9 (model L222) |
| B5 | 1 | linkerarm klontje (19,37) l → m (sluit aan op de m eronder) |
| B6 | 3 | voetlijn rechts loopt taps uit: (38,48), (39,48) → 9; los l naast zwart (41,47) → s |
| B7 | 3 | outline highlights kop linksboven (23,18), (22,19), (22,20) → 9 (binnen de lijn, op de meest belichte bolling; zoals Gnomad r10) |
| S1 | 2 | sikkel onder de kop links: (22,28) m → s, (25,30) s → m (model L215 / L209): doorlopende gebogen grens, geen losse pixels |

Diff per zone: kuif 0, ogen 0, knopen 0, silhouet 0, r10-zone linksonder 0 (alle assert). Overige 25 px: kop 8 (B1 3, B7 3, S1 2), nek 2, lijf/armen 12 (B3 10, B4 1, B5 1), voeten 3.
RGB: K, w en de steentinten (ogen, knopen) ongewijzigd (assert). Door K1/K2 veranderen de l- en m-pixels in de kuif en rond de oog-/knoopvakken wel van RGB (index gelijk).

## Palet na (10 van 16, incl. transparant)
0 transparant · 1 K (24,32,56) · 2 l (62,96,140) L90 · 3 s (172,200,228) L194 · 4 m (208,226,244) L222 · 5 w (244,250,255) L248 · 6/7/8 steen (48,50,60) / (86,88,102) / (130,132,146) · 9 (128,164,198) L157.
Sneeuw = w/m/s + 9 + lijn l + zwart: dezelfde opbouw als de DC-Scyther en Absol/Dewgong (licht, basis, schaduw, "shadows/outline highlights", outline base, outline shadows). Tint 9 past dus en blijft (in de r10-zone en nu als outline highlight / taps lijneinde / flank).

## Controles na
Geen vlekjes < 3 px buiten de bevroren zones, behalve drie taps uitlopende lijneinden in 9 ((24,31), (36,36), (38,48)–(39,48)); geen zwart binnen de figuur buiten ogen/knopen; geen lichte kleur op de buitenrand; zwart 11,0 %. Enkele lijnpixel tussen de andere lijnsoort op de rand: alleen nog (30,12) en (27,15) in de bevroren kuif.

## Resterende twijfels (eerlijk)
- **Kuif (bevroren):** zwart en lijntint om en om op de rand bij (30,12) en (27,15). Beide zijn in het model donkere inkepingen, maar volgens de regel "nooit zwart en lijntint om en om" zijn ze fout. Niet aangeraakt; voorstel ter keuze: `variant_kuif_zonder_om_en_om.png` (alleen die 2 px → l).
- **Nekschaduw en onderkant lijf** zijn brede s-banden over de hele breedte (rijen 30–32 en 45–47). Ze komen uit het model en hebben gebogen bovengrenzen; niet aangepast (wegpoetsen = pixelblur). Jordi kan zeggen of hij ze te zwaar vindt.
- **9-lijn rechterflank:** volgt het model (arm voor het lijf), maar is een 1 px strook evenwijdig aan de rand; op 8× leest hij als armrand, op 1× nauwelijks.
- **Donkerder lijn (K1)** maakt ook de binnenlijnen (armen, voetlijnen, kuiflijntjes) iets steviger; op 1× leest het nu als de Gen 3-witte soorten, maar het is de grootste visuele verandering.
- Het model in de close-ups van `vel.png` staat ±1 px verschoven (uitsnede met de fase uit r10); alleen ter oriëntatie.

Bestanden: `sneeuwmonster_ek.png`, `sneeuwmonster_8x.png`, `vel.png` (voor | na | model 8×, kop en voeten 12×, 1× op wit/crème/donker/zwart + 2×), `variant_kuif_zonder_om_en_om.png`, `bouw.py`, `vel.py`.
