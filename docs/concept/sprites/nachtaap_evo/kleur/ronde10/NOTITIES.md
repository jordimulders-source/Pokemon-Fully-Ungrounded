# Nachtaap fase 2: kleursprite ronde 10 (ogen naar Espurr)

Basis is ronde 9. Alleen de ogen zijn veranderd. De rug, de kené en de maan (D2) zijn niet aangeraakt.

Jordi: "daarnaast mogen de ogen nog wat mysterieuzer, wat minder cute, misschien nog wat meer espurr's vorm".

## Bewijs (`bron/diff_uitvoer.txt`)
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Palet:** gelijk aan ronde 9; er is geen index gewisseld.
- **Diff buiten de oogzone (x 5–22, y 42–49):** 0. Er zijn 52 px gewijzigd, allemaal binnen x 6–20, y 43–48.
- De maanpixels naast de ogen (5,43–47), (6,43), (20–21,43–46) zijn onveranderd.

## Opbouw van het oog
Beide ogen zijn 6 × 6 px, op dezelfde plek als in ronde 9, en hebben dezelfde opbouw:

| Onderdeel | Pixels |
|---|---|
| Bovenlid | een vlakke rechte rij in de donkere violettint `d` (y 43), die in de bovenhoeken 1 px meeloopt (y 44). Zo staart het oog strak en leeg. Geen zwart. |
| Ring | concentrisch, zoals Espurr: lichtrood `j` aan de zijkanten en onderaan, karmijn `i` als iris, onderhoeken `r` voor de ronding |
| Kern | `k`, 2 × 2 px, in het midden |
| Lichtpunt | 1 px wit, linksboven op de kern. De grote witte glans is weg. |
| Verre (linker) oog | de buitenkant (x 6) is `r` in plaats van `j`: perspectief, en het oog loopt zo niet weg tegen de witte maanpunt |

- Er is geen zwart kader en geen donkere ring meer.

## Eerlijk naast ronde 9 en Espurr (vel: kop op 8×, 1× en 3×)
- **Minder cute:** ja. De grote witte glans en het zwarte kader (het poppenoog) zijn weg. Het oog is nu een rood ringoog met een donkere kern die je recht aankijkt.
- **Mysterieuzer:** ja. Op 3× en 1× leest het als een strakke, gloeiende nachtaapblik. Hij is niet boos (er is geen schuine lijn boven het oog) en niet slaperig (het lid hangt niet over de kern).
- **Espurr-vorm:** de opbouw is overgenomen: lichte ring, iris, kern, klein lichtpunt, geen kader. Het oog blijft wel rood en groter dan dat van Espurr, zoals gevraagd ("meer rood dan fase 1").
- **Voor Jordi (smaak):** door de lichtrode ring "gloeien" de ogen op een donkere vacht. Op 1× kan dat net iets enger lezen dan bedoeld. Zachter kan door de zijkanten `i` te maken en `j` alleen onderaan te houden: 4 px per oog.

## Lessen
- **Een fel lichte ring rondom op een donkere kop leest als laserogen of vierkantjes.** Zet hem alleen aan de zijkanten en onderaan, laat het bovenlid in de hoeken meelopen en rond de onderhoeken af met de donkere iristint.
- **Naast een wit vlak (de maanpunt) moet de buitenrand van het oog donker zijn,** anders loopt het oog in het wit over.
