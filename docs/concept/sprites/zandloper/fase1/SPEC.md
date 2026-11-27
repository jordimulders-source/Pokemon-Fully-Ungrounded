# Zandloper-lijn fase 1 (zandloper met ogen) – besluiten

Lijn: fase 1 zandloper met ogen → fase 2 zandloper net gebroken, brein met ogen van zand komt eruit → fase 3 zand-djinn (af, `../fase3/af/`). Ground/Psychic.

## Model (27 nov)
- Jordi (26 nov): "fase 1 is gewoon een zandloper met levend zand erin, nog niks eruit of vorm, dus alleen ogen".
- Jordi over r1: "te saai en te basic, we moeten er een pokemon van maken, niet een zandloper mete ogen"; "we moeten er alvast naar hinten dat er een soort djinn in opgesloten zit"; "de pose moet meer zweven, niet gewoon rechtop staan"; "kijk naar hoe bijv sinistea ook een theekopje interessanter maakt".
- Kleur: moet aansluiten bij fase 3 (Jordi over r3: "wijkt de buitenkant nu niet teveel af van de 3e fase qua kleur?").
- Handen: "de handen zijn een goed idee" (r3); "geen ovenwant vorm"; "handen zijn geen bollen"; "pak de handen uit deze [r3], want het wordt telkens minder goed"; "draai ze zodat ze kloppen".
- **Model = `model.png`** = Gemini r6 (met het halve mondje: Jordi "zet de handen op r6") + handen uit r3, 44° gedraaid en van kant gewisseld (variant C, Jordi: "c"). Handen houden de r3-kleur (Jordi: "nee" op omzetten naar de kapkleur). Plakscript `plak/plak_handen.py`.

## Sprite (27 nov)
- Reductie op 0,70 (r1–r12) gaf een te klein linkeroog; Jordi over het model op eigen raster: "dit is goed en ik wil die versie". → Model 1-op-1 op zijn natieve raster (pitch 10,24; 63×64, ±1970 px; groter dan fase 3, door Jordi gekozen), `sprite/r14_natief/`.
- Jordi: "nee handen zijn goed, alleen tinten en schaduw keuring" → eindkeuring alleen tinten/schaduw (alpha-diff 0; bovenkap egaal hout, selout kap- en glasrand, glasblauw = fase 3), `eindkeuring/`.
- **Af (Jordi, 27 nov):** "ja commit en push naar main" → eerst de grote versie in `af/`.
- Jordi daarna: "hij is nu te groot geworden kom ik achter", "hij moet een fase 1 grootte hebben", koos "0,70" → r12 + dezelfde tint/schaduwkeuring (`eindkeuring_070/`); linkeroog nog varianten (`sprite/r16_linkeroog/`), Jordi: "A is goed" (pupil 2 px hoog). → `af/zandloper_fase1.png` (44×45, ±980 px). Grote versie bewaard in `sprite/r14_natief/af_oud/`. Naam open; fase 2 (brein breekt uit) nog te doen.
