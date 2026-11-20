# Hoatzin fase 2, r8 (19 nov), maker

Alleen de kopzone t.o.v. r7 B; buiten de kopzone 0 px verschil (gecontroleerd in `r8.py`, `r8.log`).
`kop_vel.png` = model | K1_oogA | P1_oogA | P2_oogA | P2_oogB | r7 (10×) + 1×/2× licht/donker. **`hoatzin.png` = P2 + oog A.**

## Oog (rond)
Pixel voor pixel uit **Sharpedo** (`graphics/pokemon/sharpedo/anim_front_gba.png`, x25–29 y23–27): rond oog van 5 px met ring, rode iris en
lichte kern. Omzetting: ring → ring, rood → iris (10), wit midden → pupil (1), donkerrood linksboven → glans (5), overig donkerrood → iris.
Pupil op de modelplek (12,21). **Oog A** ring zwart (1), **oog B** ring donkerblauw (8). Geen oogwit, geen kruis.

## Kuif
- Plukken = taps toelopende vormen om de modelmiddellijnen T1–T7 (plaats, richting en knik van de strengen afgelezen op het model;
  T4/T5/T6 met knik), breedte ±4 px aan de basis → 1 px aan de punt. Per pluk: lichtkant (linksboven) licht 7, midden 6,
  schaduwkant donker 2; modeltoon (bruine modelpixels per cel, `kuif_L.npy`) schuift licht/donker mee. Tegen de achtergrond: zwart
  aan de schaduwkant, bruin aan de lichtkant. Tussen de plukken het vleugelvlak in de modeltoon.
- **P1**: 7 plukken. **P2**: 5 dikkere plukken (T1, T2, T4, T6, T7). **K1** (Jordi: "mischien moet je de hele haardos omlijnen"):
  alle plukken als één haardos, doorlopend omlijnd (zwart schaduwkant, donkere selout lichtkant), binnenin licht/midden/donker,
  donker waar een pluk over een andere valt.
- Palet: bruin licht 7 = (192,122,72), midden 6 = (132,72,46), donker = 2 (gedeeld met het lijf, paarsbruin), lijn 1. Geen extra paletplek nodig.
- Zwak: P1/K1 neigen naar banden (licht/donker evenwijdig per pluk); K1 is druk.

## Studie voor r9 (8×: Pidgeot, Skarmory, Swellow, Xatu, Fearow; Archeops, Braviary, Talonflame, Honchkrow, Mandibuzz, Staraptor, Toucannon, Bombirdier, Corviknight, Decidueye, Noivern)
- **Pennen in een gespreide vleugel** (Braviary, Talonflame, Pidgeot, Fearow, Skarmory): elke pen is een eigen band van 2–4 px met
  licht aan de bovenrand (voorrand), middentint in het midden en een donkere 1-px scheiding aan de onderrand naar de volgende pen;
  de scheiding is de donkerste tint van de vleugelkleur, geen zwart. Pentoppen hebben ieder een eigen afgeronde punt in de buitenlijn
  (zwart aan de schaduwkant, selout boven). 3–4 tinten per vleugelkleur; de verre vleugel één stap donkerder. Geen losse schachtstreepjes:
  het licht ligt als rand langs de pen.
- **Kuifplukken** (Pidgeot, Staraptor, Archeops, Honchkrow, Mandibuzz): plukken als druppel/lansvormen van 3–6 px breed, omlijnd, lichte
  bovenkant, donkere onderkant, punt taps; de basis versmelt met de kop in de donkere tint.
- **Poten/klauwen** (Braviary, Talonflame, Staraptor, Skarmory, Toucannon): poot 2–3 tinten, rondom donker omlijnd, licht links;
  tenen als losse segmenten met een donkere klauwpunt; verre poot in de schaduwtint.
- **Staart** (Swellow, Pidgeot, Braviary): veren als gestapelde lobben, per veer lichte bovenrand en donkere scheiding; buitenlijn zwart onder/rechts.
- **Wat ik in r9 overneem**: buitenlijn zwart aan de schaduwkant / selout aan de lichtkant; pen = licht → midden → donkere scheiding;
  staartveer met lichte rand; nabije poot licht/midden, verre poot midden/donker; sikkelschaduw onder aan het lijf.
