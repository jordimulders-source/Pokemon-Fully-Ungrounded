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
- Silhouet: `sprite/sil.py` → `sprite/sil56.npy` (56×41, offset 4,19); bol rond gemaakt met `sprite/bol_rond.py` → **`sprite/sil56_rond.npy` = bevroren silhouet** (cirkel r 10.6 rond 31.5,31.0, rechte zijkant max 3 px na Jordi: "beide zijkanten hebben echt te lange rechte lijnen" "in de bol"; ijspunten bovenop uit het model blijven).
- Meetgereedschap: `sprite/meet/px.py x,y` (modelkleur per spritepixel), `sprite/meet/box1x.py` (model op 1×/8×, modeluitsnede op het raster).
- Maker r1 (onderlaag56 + opschonen; binnenlijnen ontbraken, bol te leeg) → lijnkaart `sprite/meet/lijnkaart.py` → r2 (`sprite/maker/r2.png`, vel `sprite/voor_jordi_r2.png`, ogen A/B/C).
- Jordi op r2: "geen van de drie, probeer het oog na te bouwen, c zit daar het dichtst in de buurt. En het is vooral detailwerk wat niet goed is, lijnen zijn te recht, de staart is een pixel blur, niet goed gedefinieerd, veel zwart, de bol is ook een pixel blur, aansluiting van de bol op het lichaam is niet mooi. Dit is nog niet goed"
- Jordi op r3b (`sprite/voor_jordi_r3b.png`): "ik zie er geen gezichtje in, betere versie, maar nog niet perfect, blijf werken aan schaduw, belijning, kleur en let er wederom op dat je teveel rechte lijnen gebruikt"
- r4 (`sprite/maker/r4.png`, vel_r4): rechte stukken 34→24 (langste 5), palet `maker/pal4.py` (blauwer, richting Regice), silhouet −16 px voor rondingen → **bevroren silhouet nu `sprite/sil56_r4.npy`** (Claude akkoord; bewaak.py gebruikt dat).
- Jordi (15 nov): "blijf doorwerken tot er een eindresultaat is en stuur die dan pas naar mij"
- Jordi (tijdens r6): "kijk ook naar bolinhoud, de binnenkant is niks uit te halen momenteel"
- Jordi: "het lijkt nu gewoon op een bevroren bol, je ziet niet meer wat er binnenin gebeurt"
- r5–r7b: keurder → MOET-lijst → maker (r5 kleur cyaan/rood, r6 ring/aansluiting/kopschaduw, r7–r7b bolinhoud: glas met lichte rand, witte krullende storm, Y-barst als enige donkere lijn). Eindkeuring r7b PASS met 8 MOET-pixels (Claude, `sprite/eind.py`).
- **Af: `af/sneeuwbolslak_fase2.png` + `af/sneeuwbolslak_fase2_8x.png`** (raster `sprite/maker/raster_af.txt`), op het overzichtsvel. Naam open.
- Jordi op het eindresultaat: "binnenkant bol is nog net niet goed genoeg, wel beter, maar mag nog meer een sneeuwstorm lijken" → r8 met twee varianten (A dichte sneeuwjacht, B plusvlokken zoals fase 1).
- Jordi op r8 A/B (`sprite/voor_jordi_r8.png`): "hybride van a en b, vlokken met sneeuwstorm" → r8C.
- **Af (r8C, hybride): `af/sneeuwbolslak_fase2.png` + `_8x.png`** (raster `sprite/maker/raster_af.txt` = raster_r8C).
- Jordi op de af-versie r8C: "de mond is ook niet goed gelukt, is nu gewoon 3 pixels diagonaal op een willekeurige plek" → r9: mondlijn naar het model.
