# Onweerswolk-Altaria frontsprite, ronde 2 (vanaf r1; silhouet bevroren, alleen kleur/lijn/schaduw)

Bestanden: `altaria_r2.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `altaria_r2_8x.png` (op wit), `vel.png` (r2 | r1 | model op schaal | game-Altaria, alle 8× / close-up kop 12×: r2 | model | game-Altaria-kop / 1× op wit, crème, donker, zwart + model + game-Altaria), `bouw.py` (`python3 sprite_r2/bouw.py [A|B|C]`, standaard C). Vel: `python3 gereedschap/vel2.py sprite_r2/altaria_r2.png sprite_r2/vel.png sprite_r1/altaria_r1.png`.

## Opdracht (letterlijk, Jordi bij Swablu, geldt hier ook)
"nee de lijnen zijn veel te hard nu, het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben. De belijning moet juist zachter en niet zwart. Kijk desnoods naar de snavel van de echte swablu qua vorm en hoe die belijnd is"

## Studie game-Altaria (8×)
- Wolk: geen zwart; buitenlijn in een donkere wolktint (112,112,152), ook aan de schaduwkant. Bollen niet met lijnen gescheiden maar met de schaduwtint (200,200,224) tussen witte bollen, met (216,224,232) als tussenstap.
- Zwart alleen op de vogel: ogen, onderkant snavel/hals aan de schaduwkant. Kuif omlijnd met donkerblauw (72,96,144).
- Snavel: wit met grijze schaduw, omlijnd in blauw/navy (en zwart alleen in de mondhoek). Swablu idem: lichte bovenkant, donkere onderrand.
- Ogen: ver oog 1×2 zwart, nabij oog 2×2 met één witte glanspixel.

## Wat er veranderde
- **Silhouet:** alpha-diff met r1 = **0 px**. 1309 van de 1820 px hebben een andere kleur (nieuw palet en nieuwe tintverdeling).
- **Palet (alle tinten uit het model, klassengemiddelden per helderheidsband):** wolk selout (28,50,81) L46, donker (50,83,116) L76, midden (72,116,149) L106 (de tussenstap), licht (104,156,185) L143, hooglicht (145,204,223) L188 → stappen 30/30/37/45. Violet selout (31,37,88) L41, donker (54,60,141) L67, midden (95,99,206) L110, licht (141,145,233) L153. Navy (17,31,61) L30 (donkerste modelband) voor de buitenlijn aan de schaduwkant. Zwart (6,12,28) alleen nog in de pupillen (5 px). Static (136,186,210) L173. Glans (236,240,251).
- **Wolktinten:** blokhelderheid van het model (alleen wolkpixels), licht verzacht met de buurblokken (½ eigen blok + ½ gewogen 1‑2‑1), drempels halverwege de tinten. De tintgrenzen volgen zo de ronde bollen van het model (hooglicht linksboven, schaduw rechtsonder per bol, zoals in het model) in vier vultinten in plaats van harde 2-tintsovergangen. Daarna ontkorrelen (< 4 px) en uitsteeksels van 1 px weg.
- **Binnenlijnen:** geen zwart meer. Naden tussen de bollen = selout (donkerste wolktint), alleen waar het model een dal heeft (blok L < 62 en in één richting aan beide kanten ≥ 15 lichter); losse selout-stippen weg.
- **Buitenlijn:** schaduwkant (achtergrond rechts/onder) navy, lichtkant selout van het materiaal (wolk/violet). Geen zwart op wolk of hals.
- **Static:** dezelfde plekken als r1 (modelplekken, 10 lijnen, 6 % van de figuur), maar in een lichtblauwe modeltint L173 in plaats van cyaanwit L214: valt binnen de wolktinten, geen witte barstjes.
- **Kuif:** kartelige vorm van r1 (= model) ongewijzigd; strengen van 2 px krijgen aan de schaduwkant donkerviolette selout, takjes van 1 px midden/donker violet (niet meer weggevallen, niet zwart).
- **Gezicht** (de reductie wist de ogen: zwart → selout → stip weg):
  - Ogen variant **C** gekozen: ver oog (23,21–22) 1×2 zwart (model X23, Y21 + bovenste derde Y22); nabij oog 2×2 op (27–28,21–22) met glans op (28,21). Het model-oog is ±1,3 px; 2×2 is iets groter, maar alleen zo leest het op 1× als oog met glans (zoals het nabije oog van de game-Altaria). A (beide 1×2 zwart, geen glans) en B (1×2 met glans boven) zijn met `bouw.py A|B` te maken; B las als witte vlek.
  - Snavel als Swablu: (24–25,22) hooglicht, (23,23) hooglicht punt, (24–26,23) licht teal, (23–26,24) navy onderrand/mondlijn (model: zwarte lijn op natieve rij 59 en 61, mondlijn rij 58). Wang (28–29,23) hooglicht.

## Controle
- 14 kleuren incl. transparant, geïndexeerd, index 0 transparant; geen losse pixels; per materiaal: wolk 4 vultinten + selout (hooglicht vooral als kleine toppen), violet 3 + selout.
- Lichte kleur op de buitenrand: alleen 7 px lichtviolet (L153, geen wit) aan de lichtkant van de kuifstrengen (31,11) (37,12) (27,13) (26,14) (33,14) (25,15) (25,16): de modelstreng heeft daar zijn hooglicht; met selout erop blijft alleen een donkere streep over.

## Eerlijke twijfels
- Bollen: duidelijk ronder en zachter dan r1, maar nog minder bol dan het model; in de wolk onderaan geven de naden korte selout-streepjes.
- Nabij oog 2×2 is een kleine maatafwijking van het model (zie boven).
- Hooglicht (L188) en static (L173) liggen dicht bij elkaar; de static leest daardoor subtiel, zoals gevraagd, maar op de lichte bollen valt hij bijna weg.
