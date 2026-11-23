# Pinsir-evolutie v2, frontsprite r2 (23 nov)

Model: `referenties/model_v2_r4.webp` (bevroren). Bouwen vanuit `docs/concept/sprites/pinsir_evo/`:
`python3 sprite_v2_r2/bouw.py A && python3 sprite_v2_r2/bouw.py B && python3 sprite_v2_r2/vellen.py`
Gebruikt `sprite_v2/natief_ruw.png` en `sprite_v2/reductie.py` (natief raster 91×78, pitch 10,24) en het r1-silhouet.

- `pinsir_evo_v2_r2_A.png`: hoofdvariant, schild zo trouw mogelijk (alle modelnaden ≥ 6 cellen; Jordi: "probeer maar eerst zoveel mogelijk het schild na te maken").
- `pinsir_evo_v2_r2_B.png`: ter vergelijking, rug = de 4 grootste modelplaten.
- A en B verschillen alleen in de rug (173 px). Beide geïndexeerd, index 0 transparant, 14 kleuren.
- `onderdelen_12x.png` (per onderdeel r1 | r2 A | model), `rug_8x.png` (A | B | model, plus Aggron/Turtonator/Tyranitar), `vel.png` (A | B | model op 6×; 1× en 2× naast r1, Tyranitar, Aggron en Pinsir op wit en donker).
- Gereedschap: `vergelijk.py` (sprite en model op dezelfde maat met raster), `cellen.py` (per spritepixel de modelcellen afdrukken), `onderdelen.py` (onderdeelvlakken, afgelezen op het model).

## Wat er anders is dan r1 (oorzaak r1: meerderheidskleur per spritepixel)
1. **Silhouet = r1, pixelgelijk** (assert in bouw.py; verschil 0 px). Geen silhouetwijzigingen.
2. **Lijnen**: de modellijnen (zwarte cellen, de r1-lijst `HOUD` met donkerbruine lijnen en een handvak) worden in het natieve raster geskeletteerd en per cel naar de sprite gezet (positie = modelpositie × 64/91, afgerond). Zo blijven ze doorlopend 1 px. Daarna houd ik alleen lijnen die op een grens tussen onderdelen liggen (vorm over vorm), en verder de kniecirkel, het gezicht, de kaken, de staartsegmenten en de rug. Krassen midden in een vlak en stukjes < 5 px vervallen.
   Kleur: binnenlijnen in de donkere bruine lijntint (L 35), in de kaken donkerrood, buiklijnen bruin licht (model: tan L 127). Zwart alleen op de buitenlijn (= r1, 280 px, gelijk aan r1) en in het gezicht waar het model zwart is. **Er is geen zwart bijgekomen.**
3. **Tinten en schaduw**: vlakgemiddelde van het model per spritepixel (exacte celoverlap, zonder de lijncellen). Daar komt per onderdeel een bolling bij uit de vorm (licht linksboven, schaduw rechtsonder, ±16 L) en een vaste verschuiving per onderdeel: nabije arm +12, schouderkoepel +14, knie +10, kopschild +10, nabije dij +6, rug −4, verre arm en verre been −6. Het resultaat gaat in 4 bruintinten (71/104/142/184), 3 roomtinten (184/216/244) en 3 roodtinten voor de kaken (58/90/135, per kaak 30/40/30 %). Stappen zijn ±33–42 L. Langs de onderkant van kopschild, knie, koepel, nabije arm, dij en staart ligt een schaduwrand van 1 tint. Vlakjes < 5 px (bruin) of < 3 px (room/rood) worden opgeslokt.
4. **Kopschild**: geen effen vlak meer. Lichte bovenafschuining linksboven (184/142), midden naar rechts (104) en een donkere onderrand. Stekels hebben een lichte linkerflank en een donkere rechterflank, zoals de modelstekels.
5. **Gezicht**: per spritepixel uit de modelcellen, maar met de helftregel: zwart als ≥ de helft van de cellen zwart is, room als ≥ de helft room is, en oog waar oogcellen liggen. r1 maakte van elke cel met een lijn een lijnpixel, waardoor de mondspleet van 1 cel een zwart blok van 4–5 px werd. Nu: twee gele ogen van 2–3 px, wenkbrauwlijn, mondspleet van 1–2 px met tanden aan beide kanten. Tandpixels met zwart rechts of onder worden roomschaduw. Met `bouw.py A r1gezicht` krijg je het r1-gezicht terug.
6. **Knie**: de kniecirkel is gemeten op de celmiddens van het 1024-model: natief rij 71 kol 59–63 (boog), kol 56–57 (links), kol 65 (rechts), rij 78 kol 59–62 (onder). In de sprite is dat een ring van 15 px in x 36–42, y 51–56, met een lichte binnenkant.
7. **Schouderkoepel**: het lichte ronde vlak natief kol 50–58 / rij 40–48 (sprite x 31–37, y 29–35) is een eigen onderdeel met licht linksboven.
8. **Handen** (nabij x 32–37 y 40–46, ver x 8–13 y 41–47): per pixel uit de cellen. Room ≥ zwart wordt klauw, anders zwart wordt lijn. Klauwpixels met een lijn rechts of onder worden roomschaduw.
9. **Rug A**: alle modelnaden ≥ 6 cellen. Elke plaat krijgt de modeltoon plus de bolling van het rugvlak. **Rug B**: de 4 grootste vlakken tussen de modelnaden (gemeten in de sprite) groeien tot ze de rug vullen. Ertussen ligt een naad van 1 px (lijntint), en elke plaat is bol met licht linksboven en schaduw rechtsonder. De naden van B liggen dus niet precies op modellijnen, maar op de grenzen tussen de gemeten platen.

## Pixels die niet 1-op-1 uit het model komen
- Alle vultinten zijn een kleurkeuze (bolling, verschuiving per onderdeel, schaduwrand). Kleur mag afwijken (Jordi, 17 nov). Vormen en lijnplekken komen uit het model.
- De kniering (15 px) staat op gemeten modelplekken, maar is als ring gezet omdat de modellijn daar uit losse cellen bestaat.
- Stekelflanken: licht links en donker rechts op de 1–2 px brede uitsteeksels.
- B: de naden tussen de platen (Voronoi-grens van de 4 grootste platen).

## Zelf gezien / zwakke punten
- r2 is duidelijk beter dan r1: de kop heeft vlakken, de knie en koepel zijn zichtbaar, de hand heeft klauwen, er zijn 3–4 tinten per onderdeel en het gezicht is leesbaar. Op 2× naast Tyranitar/Aggron is hij nog drukker: het lijf heeft meer binnenlijnen dan zij. Dat zijn de modellijnen zelf; vooral in A is de rug een net van naden.
- De rugstekels blijven kleine bultjes van 1–2 px, want het r1-silhouet heeft geen ruimte voor echte driehoeken. Grotere stekels zouden een silhouetwijziging zijn.
- De nabije onderarm (tussen koepel en hand, x 33–40 y 36–41) leest als een licht blok, niet als een duidelijke ledemaat.
- De hals rechts van de rechterkaak (x 24–32, y 21–36) is nog wat vlekkerig.
- Het model in `vergelijk.py` (geometrie van r1, IoU 0,94) ligt plaatselijk ±1 px anders dan de sprite. De lijnen zelf zijn per natieve cel gezet, niet via dat plaatje.
- Geen verse keurder gebruikt (opdracht: maker).
