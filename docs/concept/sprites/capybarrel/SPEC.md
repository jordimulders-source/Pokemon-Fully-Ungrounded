# Capybarrel (fase 1 van 2, Normal)
Alle citaten en lijnbesluiten: `docs/concept/IDEEEN.md` → "Capybarrel". Prompts en rondes: `gemini/PROMPTS.md`.

## Vast (Jordi, letterlijk)
- Naam: **Capybarrel** ("de naam capybarrel in mijn hoofd").
- Type: Normal ("hij begint als Normal"). Geen Water ("GEEN WATER"), ook niet als thema.
- 2 fases; evolutie: "wanneer die evolved, evolved het hout ook en wordt het een soort houten autotje, dus krijgt de capybara een soort van kart vorm waar delen van zijn lichaam uitsteken"; puur Normal ("gewoon normal").
- Uiterlijk: "gewoon een capybara in pokemon stijl met een barrel om zijn lichaam, maar die wel nog kan lopen".

## Model
- **`referenties/model_r3.png`** (Gemini r3). Jordi: "ok op oog na vind ik hem prima". Natief raster: pitch 20,48 px (≈50×50; `oog/natief.py`, `oog/r3_natief.png`).
- Oog: Jordi: "geen cute neopets oog maar een lui capybara oog pokemon stijl"; Gemini lukte het niet (r4, `gemini/r3/capybarrel_r4_oog_mislukt.png`: "dit kan gemini niet").
- Jordi (23 nov): "ga maar bouwen en baseer het oog op een sprite studie". → Oog 1-op-1 overnemen van een bestaande Gen 3-sprite met een lui/half-dicht oog (SPRITE_KERN: gezicht = model of een echte Gen 3-sprite, geen eigen oogvorm).
- Sprite r2 (A Hypno-oog, B Drowzee-oog), Jordi (23 nov): "dat zijn geen luie ogen". Keuzevel: `oog/studie/luie_ogen.png`.
- Jordi (23 nov) stuurde een foto van een echte capibara: "check die blik" en "mag volledig zwart oog". Op de foto (niet als bestand binnengekomen): klein, rond, volledig donker/zwart glanzend oog hoog op de kop, geen oogwit zichtbaar, met een zwaar bovenlid/vachtwenkbrauw net erboven die het bovenste stukje afdekt; kalme, onverschillige blik.
