# Regionale Poliwrath (Ice/Poison)

Eindvorm van de regionale Poliwag-lijn (harlekijnpad, ijs met cinnaber); pre-evoluties `../poliwag_regional/` en `../poliwhirl_regional/` (beide af). Politoed blijft gewoon. Type en besluit: `../../IDEEEN.md` (Jordi, 25 nov).

## Al vastgelegd voor de lijn (Jordi)
- Eindvorm = regionale Poliwrath, Ice/Poison; duidelijk anders dan Glimmora.
- "kleur zou ik voor de hele lijn hetzelfde blijven houden" (bij Poliwhirl, 25 nov).

## Jordi, letterlijk (Poliwrath)
- 25 nov: "tijd voor de ice/poison poliwrath".
- 25 nov: "hij moet als een logisch vervolg van deze lijn zien, maar iets meer een pad, dezelfde boze ogen als poliwrath, blijft ice/poison, meer en grotere kristallen, laten we eerst aan gemini. iets meer gevechtspose, maar ik vind het tot nu toe een hele logisch lopende lijn"

## Keuzes Claude in de conceptprompt (mag Jordi schrappen)
- Bijlage: gewone Poliwrath (Gen 3, 8×, `gemini/bijlage_poliwrath.png`); pre-evoluties niet als bijlage of naam (les Emolga, GEMINI.md).
- Kleuren in woorden zoals bij Poliwhirl; plek van de kristallen vrij gelaten.
- "Logisch vervolg" niet in de prompt als pre-evolutie-bijlage (les Emolga); wel hetzelfde lijnpalet en dezelfde behouden kenmerken.

## Rondes
- Prompt v1: `gemini/PROMPT.md` (bijlage `gemini/bijlage_poliwrath.png`).
- v1 (`gemini/r1/gemini_v1.png`): Jordi "het is iets teveel de originele poliwrath tov de poliwhirl die we gemaakt hebben". Bijsturen in hetzelfde gesprek met de bouw van onze Poliwhirl in woorden (slanker, scherper, langere dunnere ledematen, hoekiger), naam/bijlage trekken Gemini naar de gewone soort (GEMINI.md). Jordi: "en de mond ziet er gek uit".
- v2 (`gemini/r2/gemini_v2.png`, bijgestuurd: slanker/hoekiger + mond als dunne rode lijn): Jordi "heeft onze poliwhirl een mond?" Antwoord: ja, een rechte dunne rode lijn onder twee neusgaatjes, onderbroken door de zwarte vlek (`poliwhirl_regional/af/`).
- **v2 gekozen als model (Jordi, 25 nov):** "ok prima, dan mag poliwrath ook een mond, hij wijkt dan wel een beetje af, ik vind hem verder goed hoor". Jordi: "alleen de glimlach is idd out of place" → mond recht, zoals de regionale Poliwhirl (dunne rode lijn). Ogen: modelogen of Gen 3-Poliwrath-ogen naar verhouding ("dezelfde boze ogen als poliwrath") ook als variant.
- Jordi (25 nov): "gespiegeld uiteraard he" → model horizontaal gespiegeld vóór de reductie; licht daarna opnieuw van linksboven.
- **r1 (maker, 25 nov):** model gespiegeld, natief raster (10,24 px) 75→62 door rijen/kolommen te schrappen (kop/spiraal beschermd), palet = regionale Poliwhirl; mond recht; 4 varianten O1/O2 × S1/S2 in `sprite_r1/` (vel.png, NOTITIES.md). Wacht op Jordi.
- **Na r1 (Jordi, 25 nov):** "ik wil graag de hele ronde vorm van poliwraths ogen zien, incl ooglid, gekleurd naar het model, en geschaald naar de passende grootte. Een mond van 1 horizontale lijn kan echt niet" / "dat heeft geen enkele pokemon". r2: hele Poliwrath-oog met lid in modelkleuren, 2 groottes; 3 mondvarianten, elk overgenomen uit een bestaande Gen 3-sprite (bron benoemd). Spiraal S1 als basis (keuze nog open).
- Jordi: "nee de mond moet je gewoon kijken hoe een lijn van 1 pixel er netjes uit kan zien, maakt me geen zak uit wat voor pokemon het is" → mond = nette 1-px lijn (niet kaarsrecht, geen glimlach), 3 vormvarianten, geen bron-Pokémon.
- **r2 (maker, 25 nov):** hele Poliwrath-oog met lid in modelkleuren, E1 = verhouding (0,879), E2 = ongeschaald; mond M1 boog, M2 recht midden met knikjes, M3 golf; spiraal S1. `sprite_r2/`. Wacht op Jordi.
- **E2M1 gekozen (Jordi, 25 nov):** "linksonder heeft alles het beste, het enige waar ik nog over twijfel is de spiraal. Stel je zou de sprite draaien, zouden we dan de hele spiraal in het midden van de buik zien?" Meting (Claude): buik x 21–42 (midden ±32), spiraalmidden ±30,7, gezichtsmidden ±28; spiraal links afgesneden door de buikrand = klopt met een lijf dat iets naar links gedraaid is.
- **S1 akkoord (Jordi: "fantastico").** Eindkeuring (DC: schaduw, belijning, kleurtinten) op E2M1 + S1 → `eindkeuring/`.
