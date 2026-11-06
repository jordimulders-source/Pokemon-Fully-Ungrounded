# Poedelmot: kleur r17

Vanaf r16 (`stappen/basis.txt`). Stappen: `python3 stappen/apply.py stappen/basis.txt raster.txt r17a r17b r17c r17d` (vanuit `stappen/`), daarna `palet.py`, `controle.py`, `vel.py`. 325 px gewijzigd.
Meetgereedschap (`stappen/`): `meet.py` (gem. helderheid per spritepixel), `dk.py` (donker aandeel = modellijnen), `ov.py` (sprite | model | model met spritelijnen), `lijnkaart.py` (zwart = lijn in beide, roze = alleen model, blauw = alleen sprite). `lijnkaart_r17.png`, `overlay_onderkant.png` = eindstand.

## Per punt van de keuring r15 (gemeten op het model)
1. **A/B-naad:** in r16 nog open. Nu één lijn (17,47)→(18,48)→(19,49)→(20–21,50)→(21–22,51)→(22,52–54), het V-punt van de kraag (22,50) ertussen, B-linkerrand (24,49)→(23,50–51). Poot A en B lezen los.
2. **Middenstuk/middenpootje:** het model meet lum ±110–140 (gem. (160,125,113)); r16 (8 = 173, 9 = 145) was te licht, de keurder had gelijk. Palet: 9 = (158,124,112) onderste plaat, 8 = (198,176,162) bovenste plaat (gemeten (194,167,146)). Naden op x31 (y50–52) en (33–34,51). Middenpootje (31–34,55–58) donker: 2/3 met (33,56) in 4.
3. **Vleugelnaad:** het model heeft een rechte zwarte lijn: y35 x41–51 (donker aandeel 40–50% over de hele lengte), dan (52–53,36). Geen schulpbogen. Daaronder vlak dons (D/7/A).
4. **Linkerrand achtervleugel:** zoals het model (41,38), (42,39–41), (41,42), (42,43), (43,44), (44,45). Plaatrand links (40,45), (39,46) dicht.
5. - **C/D-naad:** het gat is dicht. De naad ligt nu op x40, zoals in het model: (40,53–56), (41,57), (40–41,58). C is x35–39 en D is x41–46. De bovenlijn van C ligt op y53 (model); die lag op y52. De rechterrand van D is dicht op (46,53).
   - **B/B2-naad:** op y55, x24–31. B2 heeft de dons-tint D.
   - **Sprietbaardjes:** doorlopende steile strepen in tan 6 op zwart, periode 3. De richting is gemeten met de structuurtensor: links '/' (±75°, helling 3), rechts '\' (±63°, helling 2). Tan-aandeel ±30% (model 22–29%). Op de buitenrand en naast de nerf staat geen streep.
   - **Crème-groep:** A, 7 en D, met 5/4/3/2 als lijn. Schaduw-6 in vacht en dons is D geworden. 6 blijft alleen in de tan plaatjes (x34–45, y44–53) en de oogring. 8/9 staan alleen in het middenstuk.
   - **Kraagrand y47–48 (x16–31):** geen 3/A-wisseling meer. De onderrand is nu de doorlopende bovenlijn van B: (25,48), (26–29,47), (30,48). Daarboven ligt crème dons.
   - **Linkeroog:** (16,38), (17,39) en (19,40) zijn licht gemaakt. Het oog volgt nu het model op y33–39.
6. **1×:** de onderkant leest als losse, omlijnde bollen (A, B, B2, C, D en dons), met het donkere middenstuk ertussen. Zie vel.png rechtsboven.

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0. Palet: 13 kleuren + transparant.

## Zwakke punten (zelf gezien, niet in de opdracht)
- De golflijn onder de witte rand van de achtervleugel ((45–53,46–47)) heeft blokjes van 2 px. In het model is de periode ±2,5 px. Ik heb hem laten staan: hij is doorlopend en viel buiten de opdracht.
- Het tan plaatje (x39–44, y45–50) volgt het model grof. De bovenrand y44 heeft nog geen lijn.
