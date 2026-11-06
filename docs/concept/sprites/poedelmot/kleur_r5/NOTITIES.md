# Poedelmot: kleur r5 (maker)

Jordi: "zo true to form als mogelijk" · "blijf doorgaan, je bent op de goede weg" · "ja let meer op vormen en belijning dan kleur".
Gebouwd vanaf r4 (r4 ongewijzigd), na de keuringen `kleur_r4/poedelmot.png.keuring_gelijkenis.md` en `…keuring_stijl.md`.

## Bestanden
- `raster.txt`, `palet.py` → `poedelmot.png` + `normal.pal` (JASC, 16 kleuren, veelvouden van 8).
- `vel.py` → `vel.png`: r5 | r4 | bron op 8× en close-ups.
- `controle.py` → `controle_uitvoer.txt`.
- `stappen/bouw5.sh`: lagen.

## Palet
Wit `A` (248,248,240). Vleugelvlak licht crème `9` (240,224,208). Vachtschaduw crème `7` (224,200,176): stap wit→schaduw Δ±40. Tan `6`/`5`/`4`. De pootpluimen houden grijsroze `8`. Verder `B` donker olijf en `C` lichte nerf. Geen lila.

## Wat er gedaan is (vorm en belijning eerst)
1. **Nabij oog**:
   - Schuin zwart amandel (x25–32, y33–40), spits linksonder (25,40), hoog rechtsboven (29–32,33).
   - Bovenlid boven de glans, zodat de glans niet in het gezicht overloopt. Glans 2×2 op (27–28,34–35).
   - Kleine donker-olijf reflectie onderin (3 px).
   - Tan ring alleen rechts en onder, zoals in de bron. Links bleef hij als rechte kolom staan en maakte hij het oog hoekig.
   - Het verre oog loopt 1 px verder door naar onder.
2. **Sprieten**:
   - Zwart vlak met een doorlopende lichte nerf.
   - Baarden als doorlopende schuine streepjes met ongelijke afstand (2–3–2–3): licht `5` bij de nerf, tussentint `3` verder weg. Daardoor geen stippenraster meer.
   - Korte baardjes boven de nerf. De belichte bovenranden zijn donkerbruin `2`.
3. **Voorvleugel**:
   - Egaal licht vlak (`9`) met drie ronde tan lobben/krullen (boog `6` rechtsonder, binnen `7`) en een tan vleugelvoet.
   - Wit alleen aan de lichtkant (boven), crème schaduw langs de schaduwrand rechts, dus geen witte band langs de rand.
   - Inkepingen als binnenlijntjes op (60,24), (59,29) en (57,33). De zoom is een geschulpte lijn met ongelijke hangende lobjes (5-4-6-3).
4. **Achtervleugel en buik**:
   - De achtervleugel is lichter, met tan alleen bovenaan en bij de voet, twee kleine lobben, witte lobben rechts, inkepingen op (55,40)/(53,44) en een geschulpte onderrand (4-3-5).
   - Het middenstuk tussen de pluimen is donkerder tan (`5`, ±L151) met twee gebogen ringen.
   - Donkere naden tussen de pluimen, gebogen langs pluim B (geen rechte kolommen).
5. **Volume**: de krassen zijn weg. De schaduw zit nu in een paar grote warme sikkels: onder de kin, kop/kraag rechtsonder, en de pluim rechtsonder (wit alleen linksboven, crème/grijsroze naar rechtsonder). De spikkels op (24,48), (28,48) en (39,30) zijn weg.
6. **Pootjes**: klauwtjes als gerichte stompjes met omlijning `2`, een lichte kern `4` en een donkere punt. De verre klauwtjes zijn hoger en donkerder `3`. Het "gat" op (21,55) ligt buiten het bevroren silhouet en kon daarom niet dicht.
7. **Linkerrand, kruin en kin**:
   - Linkerrand (x5–17, y25–52): één doorlopende lijntint `3`, met lobinkepingen naar binnen bij (10–11,31), (12–13,35) en (14–15,40).
   - Kruin: de rechte bovenlijn heeft tan tussenpixels `6` op (23,27) en (25,27), met witte plukjes eronder.
   - Kinboog 1 px hoger, met een dip op y42 bij x22–25, links doorgetrokken tot (18–19,41) onder het verre oog.

## Controle
- **Alpha-diff 0** (1782 = 1782).
- Open randen 0 (uitzonderingen: klauwtjes en de sprietpunt).
- Selout zonder afwisseling.
- Losse pixels 0, tintclusters < 3 px 0.
- Donker-aandeel **0,218**.

## Hoofdvragen (zelf getoetst naast de bron)
- **Jordi's ontwerp?** Dichter bij dan r4: lichte vleugels met ronde lobben en een witte bovenrand, een geschulpte zoom, sprieten als kam, een schuin zwart amandeloog, de kinboog onder beide ogen en een donker middenstuk tussen de pootpluimen.
- **Wat nog afwijkt van de bron**:
  - De lobben en krullen op de voorvleugel zijn kleiner en eenvoudiger dan Jordi's wolkkrullen.
  - De glans staat volgens de opdracht op (27–28,34–35); in de bron-close-up zit hij eerder rond (29–30,35–36).
  - De kruin is nog grotendeels een rechte lijn, omdat het silhouet vastligt.
  - Het donkere middenstuk oogt als één vlak (de bron heeft er losse platen in).
  - De buitenrand blijft glad door het bevroren silhouet.
- **Game Freak (naast Altaria/Venomoth)?** De omlijning is overwegend donkerbruin met een gekleurde lijntint links. De sikkels liggen rechtsonder, en de sprieten en vleugels zijn rustiger dan in r4. De sprietbaarden en schubbogen blijven door hun opzet wat regelmatig.
- Vanwege de gebruikslimiet heb ik weinig tussenrenders gemaakt. Na de naadreparatie heb ik het eindvel niet meer zelf bekeken (de controle is wel gedraaid).
