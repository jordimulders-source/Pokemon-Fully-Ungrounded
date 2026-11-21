# Vileplume r8 (Jordi over r7 verwerkt) — NIET af: voorste anemonen en mondjes niet opgelost

Bestanden: `vileplume_r8.png` (gelaat B), `vileplume_r8_gelaat{A..E}.png`, `gezicht_varianten.png` (lijf 8× + 1× licht/donker, naast het model), `vileplume_r8_kroonr7.png` (terugvaloptie: kroon van r7 + gelaat B + nieuwe linkerpoot, 82 px anders dan r7), `kaal.png`, `bouw.py` (`python3 r8/bouw.py` vanuit `vileplume_sprite/`), `meet.py` (tentakelrichtingen VL/VR in het model), `gezichten.py`, `uitvoer.txt`, `vel.png` (r8 | r7 | model 8×; 12×: krater, L, VL, VR, lijf+poten; 1× licht/donker + model).
64×64, 4 bpp, 16 kleuren, index 0 transparant (transparency=0). Palet = r7.

## Per punt
1. **Voorste anemonen (VL, VR): mislukt.** Richtingen gemeten op het model (`meet.py`: pieken van R3 rond het mondje; VL 9, VR 10 na samenvoegen < 18°). Geprobeerd (proefvellen niet bewaard, opties staan in bouw.py):
   - vingers als capsules (zoals de punten van L/R/T) over de hele schijf, scheiding R0 waar ze raken (`--vstraal`, oude code): ruis rond het mondje, geen leesbare vingers;
   - "Lileep-opbouw" (Gen 3 krans): lichte vinger 2 px + R0-lijn aan de schaduwkant op R2: vingers en tussenruimte smelten samen (R3/R2 te weinig verschil), liggende vingers naast het mondje worden horizontale streepjes;
   - (gekozen in de png) opbouw van de achterste 3: stralen met scheidingslijnen, nu in R0, in de gemeten richtingen, lichte kern 2,6 px, bovenkant lager zodat de bovenste modelpunten als vingers uitsteken. Leest op 8× als glyphs ("-O-", "=", "U") en niet als ster; op 1× drukker dan r7. **Mijn oordeel: slechter dan r7.**
   Oorzaak: de schijven zijn plat (VL 21×11 px, mondje op 3 rijen); de vingers links/rechts van het mondje liggen in dezelfde 3 rijen als het mondje en worden horizontale strepen. Boven kunnen VL/VR nauwelijks uitsteken: daar ligt de krater (moest blijven als r7).
2. **Mondjes:** één stempel voor alle vijf (6×3, ring R0, binnen R3, hoeken R1, lichte rand van 1 px). Wel gelijk, maar leest als een rechthoekje/"O" en versterkt het glyph-effect. Niet opgelost. (20 van de losse pixels in de toets zijn deze R1-hoeken.)
3. **Gezicht: opgelost.** Ogen op de plek van de U uit het model (x24–25 en x29–30, y33–), y32 blijft licht tussen kroonrand en ogen. Varianten: A model (U), **B ogen 2×2 zwart (standaard)**, C 2×2 + glanspixel, D 2×3 + glanspixel, E 2×2 + mondje (W0, 2 px op y36). C/D: glans linksboven maakt de blik boos/scheef; B en E lezen het rustigst. Op 1× zijn B–E duidelijk zichtbaar, ook op donker.
4. **Linkerpoot: rij voor rij uit het model** (dekking per spritepixel): bovenbeen y44–50 naar links (y45 4 px breed), knie rechts donkergrijs W0 (y46–51, zoals het model), **knik op y51** (scheen één kolom naar rechts, x24–26), scheen rechts zwart, voet y59 zwart x25–26 (model: y60 nog 0,3 dekking, weggelaten). Heup y41–43 = r4. Rechterpoot ongewijzigd (geassert).
5. **Krater:** pixeldiff 0 met r7 (geassert).

## Telling (t.o.v. r7)
anemonen 200 px (VL/VR + overlap met L/T/R + vijf mondjes; achterste 3 verder gelijk), krater 0, lijf+armen 10 (gelaat), poten 72 (linkerpoot).

## Toets
16 kleuren; lichte kleur op de buitenrand 0; lijnpixel midden in een vlak 0; zwart 18,3 %. Losse pixels 36: 20 mondhoeken (R1, bewust), 6 vingertoppen T (als r7), 3 armoksel (als r7), rest in VL/VR-randen.

## Voorstel voor de volgende ronde (Claude/Jordi beslist)
- VL/VR niet langer met een generator: de donkere tentakellijnen uit het skelet van het natieve model projecteren als 1-px-lijnen (spooktrein-/pitahaya-methode), dan klonteren door lijnen te schrappen tot ±8–10 vingers; of een krabbel van Jordi met de gewenste vingers op één schijf.
- Mondje: kleiner (5×2 of 4×2, gevuld donker met 1–2 lichte pixels) proberen; het model-ovaal is op 64 px maar ±6×2,5 px.
- Tot dan: `vileplume_r8_kroonr7.png` (r7-kroon + gezicht + poot) als tussenstand.
- Geen keurder gedraaid.
