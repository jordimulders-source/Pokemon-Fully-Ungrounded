# Poesrups: kleur r3 (kam groter, Jordi: "de kam mag prima groter"; oog A gekozen)

Start: `../kleur_r2/stappen/r2d.txt`. Handrasters: `stappen/r3.txt` (eerste grote kam: dunne draadhaakjes) → `r3b` (krul 1–4 dikker, wit in punt en steel) → `r3c` (krul 2 dikker, losse pixels weg; **eindstand** = `raster.txt`).

## Kam
- Zes krullen, voeten op dezelfde plek op de rug als in r2. Vorm per krul: steel omhoog, ronde kop, punt hangt naar links (voren) omlaag over een holte.
  | krul | x | y | maat (b×h) | holte |
  |---|---|---|---|---|
  | 1 | 15–23 | 24–32 | 9×9 | lucht (2×3 px, open naar links) |
  | 2 | 25–30 | 27–33 | 6×7 | schaduwpixel (27,30) + lucht onder de punt |
  | 3 | 31–36 | 31–36 | 6×6 | donker haaklijntje (spiraal) |
  | 4 | 38–42 | 34–39 | 5×6 | donker haaklijntje |
  | 5 | 42–45 | 39–43 | 4×5 | donkere pixel onder de lip |
  | 6 | 44–46 | 45–46 | 3×2 | bultje met witte kern |
- Krul 1 is groter dan de richtlijn (7–8 × 6–7): met 2 px wit in punt én steel en een open holte kwam hij op 9×9. Bovenkant y24.
- Tussen de krullen 1 px lucht (1–2, 2–3, 3–4), zodat ze op 1× los lezen.
- Buitenlijn van de kam overal 3 (4 was in r2 dun op licht); 2 alleen onder de lip/punt en in de oksels.
- Bron pixelvorm: gezocht in `graphics/pokemon/` (swirlix, mareep, whimsicott bekeken). Swirlix (`swirlix/anim_front.png`, y16–27) heeft ronde lobben met een middentoon-omlijning en wit binnenin; een haak-krul op deze maat (5–9 px) heb ik in die drie niet gevonden. De haakvorm komt dus van het model, niet van een echte sprite; altaria en wooloo niet bekeken.

## Overige punten
- **Pootjes:** pootje 4 is nu rond (4×3, zoals pootje 3; binnenwerk 5/5/5/4, donkerder want ver). Drie ronde: 2, 3, 4. Het is ±1 px groter dan in het model (daar x34–36,4, y58,7–60,5).
- **Loklijnen:** de zachte lijn op kolom 26/27 is weg; de lijn vanaf naad B stopt nu op (36,56) (was tot (38,58)); de onderste staartlijn stopt op (48,55) (was tot (51,56)); naad A begint in 5 en loopt naar 4. Over: 2 lange (naad A → (34,58), naad C → (46,57)), 1 korte (naad B), 2 korte in de staart, plus de pony-spleet op kolom 22.
- **Verre oog:** blijft 1×2 zwart op (10,55–56); (8,55), (9,55), (9,56) van 5 naar 6, zodat er een lichter randje tussen oog en buitenlijn zit. Op 1× op licht en donker zelf bekeken (vel, rij 2): als tweede stipje links van het nabije oog te zien, klein.

## Bewijs (`controle_uitvoer.txt`, `diff_r2.py`)
- diff t.o.v. r2: kam 159 px (waarvan alpha 115), pootjes 6 (alpha 4), loklijnen 15 (alpha 0), verre oog 3 (alpha 0); **buiten de zones 0**. Lijf onder de kamvoet: alpha-diff 0.
- t.o.v. het silhouet: 129 px erbij, 6 eraf (`alpha_wijzigingen.txt`, per script uit het raster geschreven; alles kam of pootjes).
- open randen 0, losse omlijningspixels 0, losse pixels 0, tintclusters < 3 px 0, selout 5 reeksen (11–26 px), 8 kleuren + transparant.
- Uitgezonderd van de clustertelling: `lijnwerk.txt` (naden, haarlijnen, lokschaduwpixels, witte kernen van krul 4–6, schaduwpixel (27,30)), `pootjes.txt`, oogglans. `lijnwerk.txt` bevat nog de coördinaten van de weggehaalde loklijnen (nu vlak 6, dus zonder effect).

## Resterende zwakke punten (eerlijk)
1. **Krul 2–5 zijn dunne haakjes** (1 px wit, verder omlijning): op 8× lezen ze als vraagtekens/vishaakjes van draad, niet als de volle, zachte plukken van het model. Op 1× en op donker lezen ze wel als krullen. Voller kan alleen als ze elkaar mogen overlappen (geen lucht ertussen) of nog groter worden.
2. **Krul 1 staat rechtop** met een open holte; in het model is het een liggende golf met de holte bijna dicht. Hij is ook duidelijk groter dan de rest (9 tegen 6 px): het verloop naar de staart is een sprong, geen geleidelijke afname.
3. **Omlijning 3 is zwaar** voor zulke dunne vormen op een lichte achtergrond; 4 was te dun. Geen tussenweg in het palet.
4. Pootje 4 is iets groter dan het model; pootjes 1 en 5 blijven bultjes.
5. Verre oog is op 1× zichtbaar maar klein.
6. De krulvorm is niet van een echte Gen 3-sprite overgenomen (geen passende gevonden in drie bekeken soorten).
