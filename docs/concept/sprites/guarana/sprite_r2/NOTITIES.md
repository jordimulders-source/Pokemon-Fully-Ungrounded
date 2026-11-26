# Guaraná fase 1, ronde 2: kleur en lijn binnen het bevroren silhouet

Bestanden: `guarana_r2.png` (hoofdversie, modelogen), `r2_ogen_groter.png` (Weepinbell-ogen), `kaal.png` (identiek aan r1-kaal), `vel.png` (r2 | r1 | model 8×, close-ups 12×, 1× op vier achtergronden), `vel_ogen_groter.png` (idem voor de variant), `varianten.png` (r2, r2-ogen, r1, r1-ogen; 8× en 1× op wit, crème, donker), `bouw.py`.
Bouwen: `cd guarana && python3 sprite_r2/bouw.py`. Varianten: `VARIANT=ogen_groter python3 sprite_r2/bouw.py sprite_r2/r2_ogen_groter.png`, `VARIANT=zonder_puntjes python3 sprite_r2/bouw.py UIT.png` (zonder puntjes wordt niet meer meegeleverd, het script werkt nog; die variant heeft een eigen, kleiner silhouet, de assert in het script geldt dan niet: kaal = eigen kaal).
**Silhouet:** alpha-diff 0 t.o.v. r1 voor beide versies (assert in `bouw.py` + controle). 809 px, 44×37.

## Benoemde reparaties (Claude r1 → r2)
1. **Tros** (niets getekend, alles gemeten op het natieve model):
   - **Vruchten** = samenhangende stukken vruchtvlees (rood L ≥ 72, zonder lijnen) in het natieve model; 7 grote stukken. Per spritepixel de vrucht met de meeste dekking.
   - **Modelrasterlijnen** = natief donkerrood L < 72 plus zwart binnen de tros dat niet aan de achtergrond of een oog grenst. Lijnpixel als (a) er geen vruchtvlees onder ligt, (b) de lijndekking ≥ 50 % is, of (c) het de grens tussen twee vruchten is met lijndekking ≥ 24 %; dan komt de lijn op één van de twee pixels, de pixel met de meeste modellijn (1 px, op de modelplek).
   - **Vulling** = gemiddelde modelhelderheid van alléén het vruchtvlees onder de pixel (lijnen niet meegeteld): ≥ 145 licht, < 100 schaduw, anders midden. De lichte plek linksboven en de schaduw rechtsonder per vrucht komen zo uit het model.
   - **Zwart** in de tros alleen nog voor pupil, oogcontour (4-buur van oogwit), buitenlijn aan de schaduwkant en de puntjes.
   - **Palet:** lijntint (2) is nu de enige donkerrode lijntint, los van de schaduw (3). Het model-donkerrood telt niet meer als vlak. Lijn (120,28,32), schaduw (176,56,48): geen samensmelten. Geen extra index nodig.
2. **Buitenlijn:** zwart alleen waar de achtergrond rechts of onder ligt, anders selout. Gecontroleerd over het hele silhouet: 0 zwarte pixels met achtergrond alleen links/boven. Donkergroene selout lichter gemaakt naar Gen 3 (66,96,52) in plaats van (48,72,48), dat op 1× als zwart las (Bellsprout/Oddish-bladrand 82,98,41).
3. **Krullen** (zones y ≥ 42 links/rechts en y ≥ 47): gemeten in Bellsprout (`anim_front_gba`): 1-px wortels zijn eigen donkere tint zonder zwart, bladranden donkergroen. Zwart blijft daarom alleen als schaduwrand (rechts/onder) van een groene vulpixel; overige zwart (1-px stukken, binnenkant, lichtkant) wordt donkergroen. Niets aan de vorm veranderd. Kleine ingesloten gaatjes (≤ 6 px) tellen niet als schaduwkant.

## Metingen
| | hoofdversie r2 | ogen groter r2 | r1 |
|---|---|---|---|
| zwart totaal | **16,3 %** | 18,0 % | 20,8 % |
| zwart tros / rank / krullen | 19 / 13 / 20 % | 24 / 13 / 20 % | 21 / 17 / 43 % |
| anders dan kaal | 256 px | 295 px | 205 px |
| per zone t.o.v. kaal: tros+ogen / rank / krullen / blad | 118 / 50 / 75 / 13 | 157 / 50 / 75 / 13 | 89 / 50 / 53 / 13 |

r2 t.o.v. r1 (hoofdversie): 86 px anders. Stappen hoofdversie: ogen 15, tros lijnen+vulling 91, binnenlijnen 15, buitenlijn 133, krullen 30, ontkorrelen 32 (overlap mogelijk). Variant: ogen 80, tros 68, de rest gelijk.
Ter vergelijking (_gba): Bellsprout 19,2 %, Tangela 16,1 %, Weepinbell 14,5 %, Ekans 14,4 %.

## Ogen-groter-variant in r2
Zelfde Weepinbell-oog (nabij oog, `graphics/pokemon/weepinbell/anim_front_gba.png` x26–32 y34–40). In r1 vielen 3 zwarte pixels van het rechteroog buiten het silhouet; nu worden stempelpixels buiten het silhouet overgeslagen, en oogwit dat daardoor op de buitenrand komt wordt zwart (2 px). De zwarte rechterrand van dat oog schuift dus 1 px naar binnen.

## Zwakke punten (eerlijk)
- **Tros:** leest beter als losse bolletjes dan r1, maar niet zo strak als het model. Niet elke vruchtgrens is doorlopend: waar de modellijn minder dan 24 % van een pixel dekt (diagonale stukken) valt hij weg. De zone links van het bovenoog is een donkere massa lijn+schaduw, zoals het model daar ook donker is.
- **Krullen op donkere achtergrond:** de 1-px donkergroene stukken vallen op donker bijna weg (op wit/crème lezen ze als groene krulletjes). Zoals Bellsprouts wortels.
- **Rechteroog in de hoofdversie** blijft het zwakste oog (smal, pupil tegen de rand). De Weepinbell-variant leest op 1× duidelijk beter.
- Eén "losse" zwarte pixel (25,25) is de oogcontour links-onder van het rechteroog, zoals het model.
