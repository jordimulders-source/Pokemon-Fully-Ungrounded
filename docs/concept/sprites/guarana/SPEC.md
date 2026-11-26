# Creepy guaraná-lijn (Grass/Ghost, 2 fases)

## Besluiten (Jordi, 25 nov)
- "creepy guarana beginnen we mee"; "ok laten we 2 fases proberen, grass/ghost".
- Lichaam: **kruipende liaan** (gekozen optie: "De klimplant zelf als lijf: ranken die als ledematen kruipen/grijpen, de vruchttrossen als hoofd(en)").
- Fases: **"Ja, zo"** op het voorstel: fase 1 dichte rode tros met een paar barstjes waar ogen door kijken, fase 2 opengebarsten vol ogen die je aankijken.
- Volgorde: **fase 1 eerst**.
- Toon: **onbehaaglijk** ("Starende ogen die je volgen, maar nog een Pokémon die je in je team wilt").

## Ronde 1 (Gemini r1, `gemini/r1.png`)
- Jordi (25 nov): "ik vind een kruipende tak/vine wel tof anders, is juist een idee wat we nog niet hebben en lekker creepy, helemaal omdat die als enige dierlijke/menslijke verder ogen heeft. Dus conceptueel goed, maar het moet nog een design worden dat beter naar een sprite vertaalt en meer guarana, verder wel eens."
- "verder wel eens" = met Claudes punten: grotere ogen die duidelijk uit de vrucht kijken; losse ronde vruchtjes met een naad. Niet: kort dik lijf (de kruipende tak blijft).

## Echte plant (naslag)
- *Paullinia cupana*, klimplant (liaan) uit de Amazone. Rode/oranjerode doosvruchten in trossen; rijp splijten ze open en tonen een zwart zaad half in een witte zaadrok: een oog.
- Legende Sateré-Mawé: een geliefd kind werd gedood; zijn ogen werden geplant en daaruit groeide de guaraná.
- Cafeïne (nooit slapen, Insomnia): oud idee uit FAKEMON_PITCH #35, niet besproken voor deze lijn.

## Open
- Kleuren buiten rood/wit/zwart (blad, rank): niet besproken, Gemini kiest.
- Naam, ability, evolutiemethode.

## Ronde 2 (Gemini r2, `gemini/r2.png`)
- Claudes twijfels: rank werd bruine houtstam met krul (slak/zeepaardje), ranken werden vier stokpootjes, vruchten met zwart raster en stekeltjes. Jordi: "verder akkoord om jouw twijfels aan te pakken" → prompt r3.
- Jordi vroeg of de ogen naar een sprite passen: test op 64 px (`gemini/r2_test64_8x.png`, langste zijde 56 px): ogen ±4–5 px, wit + pupil leesbaar. Bij een kleinere fase 1 (±40 px) worden ze ±3 px: krap.

## Ronde 3–4
- r3 (prompt r3): Jordi "hij lijkt nu wel minder te kruipen dan bij 1"; tros werd een bloem met één oog. Terug naar r2 als basis, bijsturen met 2 wijzigingen (groene rank, ranken i.p.v. pootjes).
- r4a (gesprek r1) en r4b (gesprek r2): Jordi "ik vind het nu teveel detail in de vine". 64 px-test r4b (`gemini/r4b_test64_8x.png`): de kleine krulletjes worden ruis.
- r5 (bijgestuurd in het r4b-gesprek: simpele ranken, gladde rank): 64 px-test op 56 en 44 px (`gemini/r5_test64_56en44_8x.png`): leest goed; op 44 px wordt het bovenste oog krap.

## Model en maat (bevroren, Jordi 25 nov)
- "ok 44 px, r5 is het model, maak de sprite, 56 is iets te groot denk ik". Model = `model.png` (= `gemini/r5.png`). Breedte 44 px (voorstel Claude: 44×37, ±810 px, zoals Hoppip/Ekans/Bellsprout).
- Voorstellen van Claude waar Jordi niet expliciet ja op zei (dus als variant/vraag, niet stil doorvoeren): ogen groter maken op 44 px; zwarte puntjes op de vruchten weghalen. Het zwarte raster tussen de vruchten wordt binnenlijn in eigen donkere tint (Gen 3-belijning).

## Fase 1 af (26 nov)
- Jordi over de twee oogversies: "ja rechts is veel beter" → variant B (Weepinbell-ogen, pupil 2×2 in de kijkrichting van het model). Zwarte puntjes blijven (zoals het model).
- Guaraná-gevoel: de opengebarsten rode schil om het oog en gladde bolletjes vertalen niet naar 44 px; Jordi: "akkoord", komen in fase 2 ("fase 2 doe ik in nieuw gesprek").
- Sprite: `af/guarana.png` (+ `normal.pal`, `guarana_8x.png`) = `eindkeuring/guarana_ek_ogen_groter.png`. Rondes: maker `sprite_r1`–`r4`, keurder r2/r3 BIJNA, DC-eindkeuring PASS (`eindkeuring/EINDKEURING.md`; groen contrastrijker gemaakt).

## Voor fase 2 (overdracht)
- Fase 2 = opengebarsten struik vol witte ogen met zwarte pupillen; Claude stelde voor: de rode schil splijt als lipjes om elk oog (echte guaraná), gladde glanzende bolletjes. Maat 56–64 px (fase 1 = 44×37, 809 px).
- Wat bij fase 1 werkte in Gemini: startprompt `gemini/PROMPT_r2.md` + bijsturen in hetzelfde gesprek met max. 1–2 wijzigingen ("Keep everything exactly the same. Change ONLY ..."); een nieuwe startprompt met 3 wijzigingen (r3) dreef af.
