# Sneeuwbolslak fase 2 (Ice) – SPEC

Lijn: sneeuwbolslak (fase 1, `sneeuwbolslak/`) → fase 2 → komeet (fase 3, Ice/Cosmic, langwerpig à la Interloper). Alle citaten en rondes: `gemini/PROMPT.md`.

## Jordi (letterlijk, kern)
- "fase 1 is echt een slak en vanaf fase 2 stappen we daar al van af"
- "Wat dit goed deed is de bol zelf, deze begint te barsten, plus in de bol begint een chaotische sneeuwstorm te ontstaan, in de derde fase barst deze bol compleet en ontstaat er zo de kern van de laatste vorm."
- "de clione zie ik zitten, maar we behouden dus nog wel de bol op de rug" / "we gebruiken de clione echt alleen voor de vorm"
- Op r7: "ik ben tevreden met dit concept, maar dit vertaalt nog niet naar een sprite denk ik"
- Op r8: "de bol is verschrikkelijk, maar daar kan je de bol die we al hadden op plakken toch?" → "a, de bol van r7"

## Model
- `sprite/r8_bol_r7.png` = r8 (lijf en staart) + bol van r7 (`sprite/plak_bol.py`; r7 en r8 hebben hetzelfde raster, 1-op-1; groenige randpixels van r7 vervangen door de r8-pixel).
- Volgende stap: natief raster, maattest, daarna maker (alleen opruimen binnen het silhouet).
- Jordi: "dan mag je daarna gaan bouwen, zoals bij de poedelmot qua methode oa". Maattest: `sprite/maattest.py`, vel `sprite/maattest_vel.png` (52, 56, 60 px breed; preview met 15 clusters, geen eindsprite).
- Jordi: "56 is goed, maar houd rekening met het feit dat de bol nu rechte lijnen heeft, dat moet echt een bol blijven".
- Silhouet: `sprite/sil.py` → `sprite/sil56.npy` (56×41, offset 4,19); bol rond gemaakt met `sprite/bol_rond.py` → **`sprite/sil56_rond.npy` = bevroren silhouet** (cirkel r 11 rond 31.5,31.0; ijspunten bovenop uit het model blijven; +2/−12 px).
- Meetgereedschap: `sprite/meet/px.py x,y` (modelkleur per spritepixel), `sprite/meet/box1x.py` (model op 1×/8×, modeluitsnede op het raster).
