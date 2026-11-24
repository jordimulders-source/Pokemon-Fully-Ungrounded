# Keuring Gnometrotter Rock – sprite r3 (23 nov, verse eindkeurder)

Gekeurd: `sprite_r3/gnometrotter_rock.png` tegen het bevroren model `r8/gemini_r8.png` (gedeelde geometrie via `sprite/kijk.py`), maatstaf Gnomad `gnomad/af/gnomad.png`.
Eigen beelden: `vgl_8x.png` (r3 | model op schaal | Gnomad | r2), `vgl_1x_3x.png` (r3 | model | Gnomad op 1×, 3× vergroot), `z_kop.png` en `z_onder.png` (sprite | model op 12× met raster, rode lijn elke 5 px). Metingen met `sprite_r3/meet.py` (helderheid per spritepixel) en de silhouetdekking uit `reductie_gedeeld.bron`.

## Oordeel: **BIJNA** (alleen kleine reparaties; vorm, silhouet en vlakken zijn klaar)

**Op het oog (eerst):** op 1× leest r3 als het model: muts met omgevallen punt en gat, rugkam, neus, baard, beide haarplukken, schouderovaal, stok met vuist, hand R, riem met gesp, twee blauwe dijballen met lichte voetballen en stenen zolen. De punten uit keuring r2 zijn opgelost (voetballen, broek zonder krabbels, schouderovaal, haar R, arm L zonder dambord, mutsplooien, hooglicht lijf, haar L). Niets toegevoegd of weggelaten dat ik op 64 px kan zien; oogstrook dicht volgens afspraak.

**Eis 1 (trouw):** in orde. Gemeten: tinten van muts (5/4/3 = model ±150/±130/±95), lijf, dijen en voeten volgen de modelhelderheid; silhouetgrenzen kloppen met de ≥ 50 %-regel (ook het gaatje tussen arm R en hand R zit in het model zelf: dekking (52,34) = 0,0). Enige zichtbare afwijking: het middenstuk van de stok (punt 3).

**Eis 2 (Gen 3 / volume):** elk groot vlak heeft volume: muts licht linksboven → donker rechts zoals het model, lijf 8 met platen, 15-glans op ovaal en buik en 7 aan de rechterkant, dijballen B linksboven/A rest, baard D/C. Palet 15 kleuren, ≤ 3 tinten + lijn per groep.

**Dragonfly Cave-omlijningsronde** (gids r. 80–170 / 340–470: outline base in de donkerste eigen tint, outline shadow (zwart) alleen aan de schaduwkant, binnenlijnen niet zwart, 1 px, outline highlights binnen de lijn), getoetst zoals Gnomad het doet:
- Muts, rugkam, haar, baard: base 2 linksboven, zwart rechts/onder. Goed (gelijk aan Gnomad).
- Neus: 6 boven en rechts, zwart als boog links-midden → onder (Popplio-regel uit SPRITE_KERN). Goed; (21,16) is een outline highlight binnen de lijn.
- Lijf/arm L/vuist: 6 boven/links, zwart onder. Goed.
- Benen: base 9 links/boven, zwart rechts/onder, binnenlijnen 9 (niet zwart). Goed.
- Gesp: zwart kader = het donkere gat dat het model toont; geen lijnfout.
- **Stok: linkerrand wisselt zwart en 2 om en om** (fout, punt 1).
- **Hand R: schaduwkant in 6 i.p.v. zwart**, terwijl Gnomad zijn hand R rechtsonder zwart sluit (punt 2).

## Reparaties (belangrijkste eerst; alles "neem over uit het model", niets hertekenen)

1. **Stok, linkerrand één tint.** Linkerrand x 4–7, y 38–55 staat nu 1,1,1,2,2,1,1,2,2,2,1,1,2,2,2,2,2,2 (zwart op (4,38) (5,39) (6,40) (5,43) (6,44) (6,48) (7,49)). SPRITE_KERN: "nooit zwart en ... om en om op één rand"; het model toont hier een gewone donkere randlijn aan de lichtkant. Zet de hele linkerrand op outline base 2 (zoals de muts-linkerrand en Gnomad); zwart alleen rechts (x 9–11) en onderaan (rij 56). Silhouet ongewijzigd.
2. **Hand R, outline shadow rechtsonder.** Rechterrand x 60, y 35–39 en onderrand (57–59,40), (57–58,41) zijn 6/7. Model: hand R heeft rondom een donkere lijn; Gnomad sluit zijn hand R aan de rechter- en onderkant zwart ((49,43–45), rij 47). Neem dat over: rechts vanaf ±y 37 en de onderrand in 1, boven/links 6 laten.
3. **Stok, belichte helft in het middenstuk.** Rijen 45–50 zijn over de hele breedte 3 (x 7–9). Model: linkerhelft x 6–7 meet 115–137 (= 4), rechterhelft x 8 ±97 (= 3), zoals de stok erboven (5/3) en eronder (4/3). Neem de modeltonen over: x 7 → 4, x 8–9 → 3, zodat de stok over de hele lengte licht links/donker rechts is.
4. **Twee losse lijnpixels bovenop de rechterdij.** (42,41) en (41,42) zijn 9 midden in A; model meet daar 118 en 126 (blauw midden, geen lijn; de riemonderrand ligt op x 33–40). Neem A over uit het model.
5. **Rugkam, lichte graat iets verder door.** Model: lichte graat op x 45–46 tot y 15 (rij 13: 125/139, rij 14: 124, rij 15: 122 = 4). Sprite heeft daar 3 vanaf rij 13. Neem 4 over op (45–46,13), (45,14), (45,15).
6. **Pixeltje ruis linkerdij.** (20,42) is B tussen twee 9's; model meet 127 (= A). Neem A over.

Niet aanpassen: silhouet, oogstrook, gesp, neus, baard, haar L/R, schouderovaal, muts en plooien, lijfplaten, voetballen en zolen.
Ter info (geen eis): de maker noemde de rechterdij/-voet "één blok"; op 1× leest de voetbal wel als aparte bal, zoals in het model. Geen reparatie nodig.

Na 1–6 (± 30 px, allemaal lijn/tint, silhouet 0) is dit voor mij een **PASS**; een nieuwe volledige keuring is niet nodig, een diffcontrole (alleen deze pixels gewijzigd) volstaat.
