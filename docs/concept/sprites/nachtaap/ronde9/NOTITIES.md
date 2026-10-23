# Nachtaap (Psychic-starter fase 1), ronde 9: afmaken en repareren (basis ronde 8)

Geen nieuw ontwerp. De ronde-8-lagen zijn omgezet naar `bron/delen.txt` (pixel-identiek gecontroleerd) en met de hand bijgewerkt. Kop en lijf zo veel mogelijk gelaten (Jordi: tevreden, op de ogen na); veranderd: ogen, oren, staartsteel, armen (Chimchar-verhouding) en de verre ledematen.

## Analyse: gids tegen echte Pokémon (pixelniveau) en onze ronde 8
Bekeken: Jigglypuff, Wigglytuff, Aipom, Natu/Espeon (oogkleur), Chimchar (Gen 4, voor verhoudingen en stijl); gids: *Shine* (kraalogen), *Outline shading*, *Curves*.

| Regel (gids) | Echte Pokémon | Ronde 8 | Wat ik veranderde |
|---|---|---|---|
| Oogmaat | Jigglypuff: oog 8×7 op een kop van 32 breed (±25%); Wigglytuff 7×7 op ±30 | 10×11 en 8×11 op een kop van 26 (±38%) | 7×8 (dichtbij) en 6×8 (ver), ±27% van de kopbreedte |
| Ogen niet opgeplakt: omlijning in gezichtstinten | Jigglypuff: rand van het oog in de donkere huidtinten (roodbruin), pupil in donkerblauw, alleen een paar echt zwarte pixels; Aipom: oog omringd door gezichtskleur | Volledig zwarte ring rond elk oog | Ring in donkermagenta (zijkanten), bovenlid met 2–3 zwarte pixels, onderrand en oogkas in crèmeschaduw, crèmeschaduw ook boven het lid: het oog loopt over in het gezicht |
| Glans + gekleurde reflectie | Kraalogen: witte glans linksboven, lichte kleur rechtsonder | Wel aanwezig, amber | Behouden, nu in magenta/roze (Psychic, vgl. Espeon); pupil groot gelaten (Jordi: vorm prima) |
| Gezicht compleet | Aipom/Chimchar: ronde oortjes op ooghoogte, gesloten omlijning, lichte binnenkant | Geen oren | Twee ronde oortjes met crème binnenkant; verre oor links kleiner, half achter de kop |
| Staart buigt overal | Aipom/Mew: staart als doorlopende curve, segmentlengtes lopen geleidelijk op | Spiraal met 12 px rechte buitenrand en een kaarsrechte schuine steel van 15 px | Buitenrand van de spiraal bolt uit; steel als J-curve (stappen 0-0-1-0-1-1-1-1-2-2-3) die achter de flank verdwijnt |
| Verre ledematen zichtbaar | Chimchar/Aipom: verre arm en voet steken naast het lijf uit, smaller en donkerder | Rechterarm en -been ontbraken | Verre arm langs de rechterflank in schaduwviolet met crèmehandje op de grond; verre voet rechtsonder |
| Verhouding kop/lijf/armen | Chimchar: dunne armen (3–4 px) van ±13–14 px, handen tot op de grond | Korte armen in een V onder de kin | Lange dunne armen (4 px, ±14 px), handjes op de grond; lijf voller dan Chimchar gelaten, crème buik iets smaller met violette flanken |

## Controle (checklist)
- [x] Tellen: 2 armen, 2 benen (dichtbij knie + voet, verre voet), 2 oren, 2 ogen, 1 mond, 1 staart.
- [x] Omtrek dicht: geen randpixels zonder omlijningskleur (de ene melding is de staartpunt binnen de spiraal); staart en oren sluiten aan.
- [x] Geen recht stuk > 4 px in organische vormen. Over: de bovenkant en linkerzijkant van de kop (ongewijzigd, Jordi tevreden) en de onderkant waar hij op de grond zit.
- [x] Zwart-aandeel rand **0,51**.
- [ ] Oppervlak **1041 px** (ronde 8: 994), iets boven ±800–950, door de langere armen.
- [x] 64×64, 2 frames (kop en oren 1 px omlaag, staart 1 px omhoog), 14 kleuren, index 0 transparant. Het gloeilichtje tussen de handen is vervallen (handen staan nu op de grond).

## Bestanden
- `anim_front.png`, `normal.pal`, `compare.png` (ronde 8, ronde 9, Aipom, Jigglypuff, Natu; 1× en 3×).
- `bron/delen.txt`, `bron/palet.txt`, `bron/raster_f1.txt`/`raster_f2.txt`, `bron/bouw9.py`, `bron/zet.py`, `bron/patches/`, `bron/vergelijk9.py`.
