# Werkwijze overworldsprite (compact, verplicht)

Bewezen op de viscacha (19 nov): `docs/concept/sprites/viscacha/overworld/gemini_route/af/overworld.png`. Test met twee routes naast elkaar: **Gemini-route** (A) tegen **eigen route** zonder Gemini (B, uit front/rug/icoon + meetregels). Jordi: "Gemini is echt zeer goed" · "en de eigen route echt heel matig" · "dit is no contest". Dus: altijd via Gemini.

**Oordeel Jordi (19 nov), letterlijk:** "alles is in de eigen route slechter, behalve misschien de staart positie, maar de staart vorm klopt ook niet. Plus gemini is wel consistent met andere sprites. Zijaanzicht is goed, hoofd naar verhouding, rug naar verohuding, aan de voorkant is die herkenbaar, met alle belangrijke elementen, terwijl eigen route het hoofd verschrikkelijk is, en de ogen wederom gewoon niet goed zijn, met te dikke heupen. Gemini geef ik een 9 tot 9,5 en de eigen route hooguit een 4". Naslag: `docs/concept/sprites/rug_icoon_studie/overworld/` (meetstudie) en `viscacha/overworld/PROMPT_OW.md` (prompts en rondes).

## Wanneer
Alleen voor soorten die in de wereld staan (`OBJ_EVENT_GFX_SPECIES`); volgers blijven uit (Jordi). Drie aanzichten (voor, achter, opzij naar links), elk stil + lopen.

## Stappen
1. **Gemini-prompt** (nieuw gesprek), bijlage = onze **front én rug op 8× naast elkaar** (geen icoon: het gedeelde icoonpalet geeft verkeerde kleuren; geen voorbeeldsoort). Voorbeeld: `PROMPT_OW.md` ronde 2, variant A. Vast erin:
   - "HeartGold/SoulSilver walking Pokémon", drie aanzichten in eigen 32×32-vakken op één basislijn: voor recht van voren (beide ogen, symmetrisch), achter recht van achteren, opzij naar links.
   - **De bouw in woorden** (viervoeter/tweevoeter, houding, lijfvorm) plus de kenmerken. Zonder bouw maakte Gemini er een rechtopstaande Raichu van (r1).
   - AVOID-regel met de soorten waar hij naartoe glijdt (bij knaagdieren: Raichu, Pikachu, Pachirisu, Dedenne, konijn, op twee poten).
   - Chibi, ±21 px hoog, zwarte omlijning, vlak met één schaduw, uitvergroot, witte achtergrond.
2. **Jordi kiest** en zegt wat afwijkt (viscacha: alleen de ogen; snorharen weglaten mocht). Opslaan als `<soort>/overworld/gemini_rN.png`.
3. **Overnemen, niet hertekenen** (één maker-agent, SPRITE_KERN meegeven): natief raster terughalen (Gemini-pixel ±5 px; per aanzicht ±46 px hoog), **exacte 2×2-reductie** (masker bij 2 van 4 gevuld, rand = omlijning, binnen = meerderheidskleur; kies de schoonste fase), dan opschonen op een tekstraster. Kleuren uit het frontpalet (`normal.pal`); omlijning onder/opzij zwart, bovenrand een donkere vachttint (mag als extra kleur in het eigen overworldpalet). De maker meldt per zone hoeveel pixels afwijken van de kale reductie.
4. **Ogen** (en andere toegestane afwijkingen): opbouw van het front-oog, kleiner (viscacha voor: [bruin, zwart] boven [zwart, glans], gespiegeld; opzij zwaar lid van 3 px boven zwart + glans).
5. **Loopframes**: zelfde figuur op dezelfde plek en hoogte; alleen de voeten 1 px (voor/achter een voet omhoog, opzij voorpoot naar voren en achtervoet naar achteren), 10–15 px verschil.
6. **Claude vergelijkt** model (verkleind) | sprite per aanzicht. Valkuil r1: de reductie werd hoekig (ronde oren werden staafjes, kop en lijf blokken, staart stijf, wangplukken streepjes); terug naar de ronde modelvormen. Daarna een **verse keurder** (eerst blind naast echte overworldsprites, dan trouw aan het model + normen), alleen benoemde reparaties. Viscacha: 3 rondes, 1 keuring.
7. **Opleveren** in `<soort>/overworld/gemini_route/af/`: `overworld.png` (192×32, P, index 0 transparant; frames 0–1 voor, 2–3 achter, 4–5 opzij), `overworld_normal.pal`, `overworld_8x.png`, `loop.gif`.

## Normen (meetstudie, 775 sprites + handmeting 15 viervoeters)
- Hoogte voor ±0,43 × front, achter/opzij ±0,39 × front (p25–p75 tot ±0,48); ≈ icoonhoogte. Onderkant y 29, midden x 15–16.
- Kop is een vaste maat: opzij ±9×9, voor ±13×11, achter ±13×8; beslaat 55–58% van de figuur (voor/opzij). Opzij altijd een echt profiel (15/15).
- Oog 1×2 px (groter front-oog: 2×2), ogen voor ±5 px uit elkaar; oren opzij 3 px boven de kop; poten 2–3 px.
- Voor/achter ±98% symmetrisch; 9–15 kleuren; binnenlijnen in elk frame.

## Wat niet werkte (eigen route B, cijfer hooguit 4)
Jordi: kop "verschrikkelijk", ogen "wederom gewoon niet goed", heupen te dik, staartvorm klopt niet (staartpositie misschien beter). Zonder model, uit front/icoon/rug + rekenregels: rechtopstaande kat (r1), daarna hoekig en stijf (r2). Rekenregels alleen zijn geen ontwerp: een nieuw aanzicht (recht van voren/achteren) heeft een model nodig. Gemini r1 zonder bouw in woorden faalde ook.
