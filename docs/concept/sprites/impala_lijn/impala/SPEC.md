# Impala (fase 2 van 3, impala-lijn, Normal/Steel)
Alle citaten en lijnbesluiten: `docs/concept/IDEEEN.md` → "Impala-lijn"; samenvatting `POKEMON.md` → Impala-lijn. Prompts/rondes: `gemini/PROMPTS.md`. Fase 1: `../dikdik/`.

## Vast (Jordi, letterlijk)
- "beide steel, hoorns echt van metaal, alleen de dikdik niet"; hoorns gepolijst staal (dof ijzer → gepolijst staal → spiegelglans, "akkoord").
- Overdrijven "zodat ze een beetje afwijken van de dieren ook, maar de inspiratie wel nog kenbaar is"; "het belangrijkste is dat de vorm van de hoorns blijft kloppen".
- Lichaamskleur zilver ("lichaamskleur he").
- Tekening: "echte tekening houden": scherpe tweedeling rug/flank/buik + zwarte M + plukjes.
- "de impala moet stoicijns zijn, misschien iets meer in een protector houding pose".
- "misschien de oren ietsje groter" (r1).
- Kuif: "misschien kunnen we nog iets met de kuif uit fase 1, dat die iets meer mee evolved ook"; "misschien de kuif nog iets meer over de hals laten komen"; r4b afgekeurd: "beetje jotaro uit jojo, dat het overgaat maar je niet kan zien waar".

## Model
- **`referenties/model_r5.png`** (Gemini r5). Jordi: "goed, maar vertaalt dit naar een sprite, gezien de andere artstijl?". Illustratiestijl, geen pixelraster (r5b pixelart "lukt hem niet"); sprite = eigen reductie van r5.
- Kleur mag afwijken van het model (SPRITE_KERN).

## Afwijkingen van het model (Jordi, 25 nov)
- **Strepen:** "de drie strepen hier nemen niet mooi over denk ik dus doe jouw idee al" = Claudes voorstel (r3b, regel 3): de strepen op de zijkant van de bil weg; één zwarte streep in het midden van de staart en één zwarte streep langs de achterrand van de dij.
- **Oog:** "we pakken een gen 3 bron oog, niks tekenen zelf". Welke bron: nog te kiezen door Jordi (varianten op de sprite; bronvel `oog/bronnen.png`).

## Sprite
- Rondes in `sprite/rN/`.
- Oogvarianten op r2 (25 nov): `oog/oog_varianten.png` (A model-reductie, B Rapidash, C Absol, D Stantler; `oog/varianten.py`, pixels 1-op-1 uit de `_gba`-sprite, alleen omgekleurd). Wacht op Jordi's keuze.
- Oogvarianten op r5: `oog/oog_varianten_r5.png` (`python3 oog/varianten.py r5`; A model, B Rapidash, C Absol, D Stantler).
- Jordi (25 nov), op de oogvarianten r5: "a is het vetst maar mag ietsjepietsie doortastender qua blik, en loopt de kuif/maan genoeg door op de hals?" → blikvarianten A1–A3 (`oog/blik_varianten.png`, `oog/blik.py`; alleen bestaande oogpixels omgekleurd); manen in r6.
- Jordi: "nee moet niet groter, maar iets zelfverzekerder" ("nee he toog") → B1–B3 zonder extra donker (`oog/blik_varianten2.png`).
- Jordi (26 nov), op r6: "ik zie nog wel onnodig veel lange rechte lijnen. Onder de hoorns, de oren, de rug, de manen op de rug, de poten, hij is heel houterig, de hele sprite mag wel wat smoother. Je verandert niks behalve dat je rechte lijnen wat minder recht maakt wanneer nodig, meet met het model, niet met een raster, maar waar er golven zitten en waar niet" → r7.
- Jordi (26 nov), op r8: "pak de binnenkant ook aan, links bij het witte stuk vacht was al goed, dat hoefde niet aangepast te worden" → r9: borstbolling links terug naar r7, tintgrenzen binnenin gebogen naar het model.
- Jordi (26 nov), na r10 (= r9): "nee je mag nu gaan beginnen met de eindkeuring, dus netter maken". Geen overdrijven/anti-aliasing. Oog nog open (A, B1–B3).
- **Oog (Jordi, 26 nov): "b3"** = oog A (model) met wit boven de pupil → lichte kopvacht en witte onderrand weg (`oog/blik.py` B3). Wordt na de eindkeuring toegepast.
- Jordi (26 nov), op r12: "de poten zijn effen vlakken, controleer die opnieuw" → r13.
- Poten (Jordi, 26 nov): "kijk naar andere pokemon met korte poten, hoe doen die dat?" · "niemand met zulke dunne poten?" · "kirlia heeft meerdere tinten?" · **"doe kirlia maar na idd"**: Kirlia-opbouw (gemeten, `graphics/pokemon/kirlia/anim_front_gba.png` x29–34 y46–57): 1 px vulling met tinten in de lengte (middentint bij heup/gewricht, lichtste tint op de scheen, middentint onderaan), linkerlijn donker eigen tint (soms middentint waar de poot smaller wordt), rechterlijn zwart; verre poot één tintstap donkerder. Studie in `poten_studie/`.
