# Onweerswolk-Altaria frontsprite, ronde 2 — **op het kop×1,3-model**

**r2 staat op het kop×1,3-model** (`../model_kop/natief_kop13.png`; Jordi: kop te klein, "altaria grotere hoofd/nek lijkt goed te passen"). Het silhouet is de r1-reductie op dat model (`basis.py` → `basis_kop13.png`, zelfde regels als r1; model bovenaan 3 natieve rijen gepad omdat de kuif nu tot rij 0 reikt). Alpha-diff met r1 = 162 px, allemaal in kop en kuif (x20–49, y5–24); wolk, hals en static gelijk. Alpha-diff r2 ↔ basis = 0. Figuur x3–61, y5–62, 1904 px.
`klassen.py` kreeg parameters `KOP`/`KUIF` (standaard = oud model, r1 blijft reproduceerbaar). In het nieuwe model ligt naast de vergrote kop een bijna-witte plakhalo; die telt als achtergrond.
Jordi (letterlijk): "iets minder detail is niet erg tov het model, zolang die niet blurry wordt".

Bestanden: `altaria_r2.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `altaria_r2_8x.png` (op wit), `vel.png` (r2 | r1 | model op schaal | game-Altaria, alle 8× / close-up kop 12×: r2 | model | game-Altaria-kop / 1× op wit, crème, donker, zwart + model + game-Altaria), `basis.py`, `basis_kop13.png`, `bouw.py` (`python3 sprite_r2/bouw.py [A|B|C]`, standaard C; draait basis.py mee). Vel: `python3 gereedschap/vel2.py sprite_r2/altaria_r2.png sprite_r2/vel.png sprite_r1/altaria_r1.png model_kop/natief_kop13.png 3` (close-up kop: natief model zelf, 4 px per modelpixel).

## Opdracht (letterlijk, Jordi bij Swablu, geldt hier ook)
"nee de lijnen zijn veel te hard nu, het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben. De belijning moet juist zachter en niet zwart. Kijk desnoods naar de snavel van de echte swablu qua vorm en hoe die belijnd is"

## Studie game-Altaria (8×)
- Wolk: geen zwart; buitenlijn in een donkere wolktint (112,112,152), ook aan de schaduwkant. Bollen niet met lijnen gescheiden maar met de schaduwtint (200,200,224) tussen witte bollen, met (216,224,232) als tussenstap.
- Zwart alleen op de vogel: ogen, onderkant snavel/hals aan de schaduwkant. Kuif omlijnd met donkerblauw (72,96,144).
- Snavel: wit met grijze schaduw, omlijnd in blauw/navy (en zwart alleen in de mondhoek). Swablu idem: lichte bovenkant, donkere onderrand.
- Ogen: ver oog 1×2 zwart, nabij oog 2×2 met één witte glanspixel.

## Wat er veranderde
- **Palet (alle tinten uit het model, klassengemiddelden per helderheidsband):** wolk selout (28,50,81) L46, donker (50,83,116) L76, midden (72,116,149) L106 (de tussenstap), licht (104,156,185) L143, hooglicht (145,204,223) L188 → stappen 30/30/37/45. Violet selout (31,37,88) L41, donker (54,60,141) L67, midden (95,99,206) L110, licht (141,145,233) L153. Navy (17,31,61) L30 (donkerste modelband) voor de buitenlijn aan de schaduwkant. Zwart (6,12,28) alleen nog in de pupillen (5 px). Static (136,186,210) L173. Glans (236,240,251).
- **Wolktinten:** blokhelderheid van het model (alleen wolkpixels), licht verzacht met de buurblokken (½ eigen blok + ½ gewogen 1‑2‑1), drempels halverwege de tinten. De tintgrenzen volgen zo de ronde bollen van het model (hooglicht linksboven, schaduw rechtsonder per bol, zoals in het model) in vier vultinten in plaats van harde 2-tintsovergangen. Daarna ontkorrelen (wolk < 6 px, violet < 4 px: ook piepkleine hooglichtjes weg, liever grotere heldere vlakken) en uitsteeksels van 1 px weg.
- **Binnenlijnen:** geen zwart meer. Naden tussen de bollen = selout (donkerste wolktint), alleen waar het model een dal heeft (blok L < 62 en in één richting aan beide kanten ≥ 15 lichter); losse selout-stippen en naadstreepjes < 4 px weg (samengevoegd met de buurvultint).
- **Buitenlijn:** schaduwkant (achtergrond rechts/onder) navy, lichtkant selout van het materiaal (wolk/violet). Geen zwart op wolk of hals.
- **Static:** dezelfde plekken als r1 (modelplekken), stukjes < 5 px samengevoegd: 9 lijnen van 5–35 px, 5,5 % van de figuur,, maar in een lichtblauwe modeltint L173 in plaats van cyaanwit L214: valt binnen de wolktinten, geen witte barstjes.
- **Kuif:** kartelige vorm uit de reductie van het kop×1,3-model (kuifregel alleen waar violet/zwart overheerst; de rechterpunt ligt nu tegen de vleugel); strengen van 2 px krijgen aan de schaduwkant donkerviolette selout, takjes van 1 px midden/donker violet (niet weggevallen, niet zwart); lichtviolet alleen binnenin, aan de rand midden-violet.
- **Gezicht** (de reductie wist de ogen: zwart → selout → stip weg):
  - Ogen variant **C**: ver oog (22,20–21) 1×2 zwart (model natief x68–71, rij 48–51); nabij oog 2×2 op (27–28,20–21) met glans linksboven (27,20) (model: glans natief (86,47–48), linksboven in het oog x85–88). Het model-oog is ±1,3 px; 2×2 is iets groter, maar alleen zo leest het op 1× als oog met glans (zoals het nabije oog van de game-Altaria). A (beide 1×2 zwart, geen glans) en B (1×2 met glans boven) zijn met `bouw.py A|B` te maken; B las als witte vlek.
  - Snavel als Swablu (model natief x65–85 = X20–26): (21–26,22) hooglicht, (21,23) selout-punt, (22–26,23) licht teal, (22–26,24) navy onderrand/mondlijn (model: rij 58–61 zwarte lijnen). Wang (29–30,22–23) uit de reductie.

## Controle
- 14 kleuren incl. transparant, geïndexeerd, index 0 transparant; geen losse pixels; geen lichte kleur op de buitenrand; zwart alleen in de pupillen (5 px), navy 135 px.
- Wolk 4 vultinten + selout (hooglicht als toppen van de bollen), violet 3 + selout.
- Afwijkingen van de kale toewijzing (per stap): ontkorrelen+uitsteeksels 206, naad/static-stukjes 48, buitenlijn 193, kuif omlijnd 69, ogen 6, snavel 10. Niets getekend buiten ogen en snavel (modelplekken).

## Eerlijke twijfels
- Bollen zijn ronder en zachter dan r1, maar minder bol dan het model (bewust iets minder detail, geen korrel).
- Nabij oog 2×2 is iets groter dan het model-oog; alleen zo leest het op 1× als oog met glans.
- Kuif op 1/3: takjes van 1 px; de punt rechts raakt de vleugel (zoals in het kop×1,3-model).
