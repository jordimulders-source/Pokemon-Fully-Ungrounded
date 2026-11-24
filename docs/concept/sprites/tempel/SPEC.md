# Levende Inca-tempel (werknaam open)

Static encounter, geen legendary. Type: Ghost/Rock. Single stage (Jordi, 23 nov: "Is een single stage").

## Jordi letterlijk (23 nov)
- "we gaan de tempel pokemon maken. In game gaat het een soort fake out worden, static pokemon, groot zoals snorlax en qua data helemaal groot. Het is een tempel die leeft, ghost/rock. De speler denkt dat het een ingang is in game en dan blijkt de hele tempel tot leven te komen, inca tempel idee"
- Eerder (IDEEEN.md): "Ruïne- of zelfs tempel-Pokémon: een levende tempel, enorm, mogelijk een Snorlax-idee: geen legendary, wel een static encounter".

## Keuzes Jordi (23 nov, meerkeuze)
- Basis: **trapeziumdeur + nissen** (algemeen Inca, strak gevoegd steen; de deur is de "ingang" waar de speler naartoe loopt).
- Gezicht: **deur = mond** (nissen/ramen erboven zijn de ogen).
- Houding: **geen ledematen** (puur het gebouw dat leeft).
- Ghost-kant, letterlijk: "het idee erachter, dat een tempel na tig jaar tot leven komt. Hij heeft wel ogen, maar dat is dan licht die vanuit gaten in de architectuur komt".

## Open
- Naam, kleur van het licht in de ogen, data (stats/ability/moves; "qua data helemaal groot"), plek in de wereld.

## Rondes
- Prompt v1: `gemini/PROMPT.md` → `r1/gemini_v1.png`. Jordi: "ok hij oogt nog wat klein, het mag groter" (= vak meer vullen, meerkeuze) / "en beetje saai" / "niet per se meer detail dat niet naar een sprite vertaalt, maar interessantere architectuur" / "maar goed begin".
- Prompt v2: `gemini/PROMPT_v2.md` (nieuw gesprek, geen bijlage). Architectuurkeuzes van Claude (ter keuze voorgelegd, niet van Jordi): grote veelhoekige blokken, dubbel-getrapte trapeziumdeur, getrapte sokkel.
- r2 (`r2/gemini_v2.png`), Jordi: "hij lijkt wel ok, maar ik wil iets meer lagen, dat het echt een tempel is ipv alleen een deur".
- Prompt v3: `gemini/PROMPT_v3.md` = v2 met alleen het lagen-blok veranderd (Claude leest "lagen" als gestapelde verdiepingen/terrassen).
- r3 (`r3/gemini_v3.webp`), Jordi: "lijkt dit op een echte tempel?" (Claude: deels; de getrapte toren met overstekende randen en een stenen plat dak is niet Inca).
- Jordi over r3: "ik vind het denk ik iets te simplistisch"; bevestigt Claudes punt "Een toren van gestapelde verdiepingen bouwden de Inca's niet ... Dit doet eerder denken aan een ziggurat of een fantasietempel": "dit ja, dat bedoel ik". Keuze (meerkeuze): **tempel op terrassen** (Machu Picchu/Pisac: tempelgebouw van één laag bovenop een paar landbouwterrassen).
- Prompt v4: `gemini/PROMPT_v4.md` (zonder strodak; dat was "eventueel" en is niet gekozen).
- r4 (`r4/gemini_v4.webp`), Jordi: "nu een beetje een maya tempel he" (Claude: door de trap in het midden, die Claude zelf had toegevoegd, en de getrapte vorm).
- Prompt v5: geen trap, lange lage gebogen terrassen breder dan de tempel. v5b: idem + stenen puntgevels (voorstel Claude, niet van Jordi).
- r5: `r5/gemini_v5.png` (zonder gevels), `r5/gemini_v5b.png` (met gevels). Beide liggend/breed (1024×559).
- Jordi stuurt eigen foto's van een Inca-ruïne, "de laatste middag van de inca trail" (`referenties/jordi_incatrail_*.webp`; waarschijnlijk Wiñay Wayna): "Kunnen we hier niet iets mee?"
- Prompt v6 (Claude, uit de foto's): ruw stapelwerk i.p.v. gepolijste veelhoeken, hoge puntgevels met stenen pinnen, mos/gras op de muren, deur met stenen latei, twee rechthoekige raampjes als ogen, lage terrasmuren.
- r6 (`r6/gemini_v6.webp`), Jordi: "maar dit is niet wat ik bedoel, het toffe is dat die tempels gelaagd op bergen worden gebouwd, het zou vet zijn om daarom een tempel te hebben die dus ook gelaagd is alsof die op een bergwand staat, met de ingang onderin en de rest van de tempel een paar terraslagen".
- Prompt v7: gelaagd tegen een bergwand, ingang onderin (mond, raampjes erboven = ogen), daarboven 2–3 asymmetrische terraslagen met ruïnes met puntgevels, geen trap. Ruw stapelwerk en mos van v6 behouden.
- Jordi over r6: "en dit is teveel detail" → v7: weinig, grote stenen, vlakke delen, alleen een dun strookje mos, geen korstmosvlekken.
- r7 (`r7/gemini_v7.webp`, prompt v7), Jordi: "geweldig design, vertaalt dit naar een sprite? dit is wat ik zocht". Snelle 64 px-test (verkleinen + 16 kleuren, geen tekenwerk): `r7/test_64px_8x.png`.

## Model (bevroren, 23 nov)
`referenties/model.webp` = Gemini r7. Jordi: "ja akkoord, de ogen mag je afwijken van het model" (op Claudes voorstel: ogen iets groter en lichter zodat de schrik werkt; raampjes in de gevels dicht/donker en klein zodat alleen het onderste paar licht geeft). Jordi: "het voordeel is dat het vrij hoekig is dus dat vertaalt goed naar een sprite denk ik".

## Grootte
Static, groot zoals Snorlax: vult het 64×64-vak zoals de 64 px-test (`r7/test_64px_8x.png`).

## Sprite
Rondes in `sprite/rN/`.
- r1–r2 maker 1; keurder r3 BIJNA (vlakken effen, gevels bultjes); r4–r6 verse maker (voegen, gevels met eigen omtrek, rustig gezicht, bergwand één vlak); keurder r5 BIJNA; eindkeuring DC r6 BIJNA (2 lijnreparaties, 19 px kleur) → r7 door Claude (`sprite/r7/`, diff 19 px t.o.v. r6). Kandidaat voor Jordi: `sprite/r7/tempel.png` + `tempel_8x.png`. Ter info (eindkeurder): gezichtslijnen (oogkaders, latei, deurstijlen) blijven de donkere lijntint i.p.v. selout, voor leesbaarheid.
- Jordi over r7: "de ogen zijn niet mooi, voor de rest is alles goed behalve de eindkeuring" / "de ogen zijn teveel vierkantjes die niet mee gaan met het perspectief". Oogvarianten met de diepte (dagkant) van het model: `sprite/r8_ogen/varianten.png` (A/B/C).
- Jordi: "het gaat om de super rechthoekige zwartgelijnde vorm" → varianten zonder zwart rechthoekig kader: `sprite/r8_ogen/varianten2.png` (D geen kader, E trapezium in donkere steentint, F trapezium met zwart alleen aan de schaduwkant).
- Jordi: "beter maar de verlichting moet duidelijker geel, als de spirit die erin zit, of misschien zelfs een andere kleur" → lichtkleuren op variant E: `sprite/r8_ogen/lichtkleur.png` (geel, goud, groen, cyaan, paars).
- Jordi koos "goud" (op variant E). Af: `af/tempel.png` (= `sprite/r8_ogen/tempel_E_goud.png`, basis r7). Op het overzichtsvel (sectie New).
- Jordi over af-versie (24 nov): "ok het mos ziet er wel vet uit, misschien kan je dat nog wat meer doen, verder is het alleen nog maar inkleuren wat beter moet, ik zie veel effen vlakken, weinig kleurtinten, schaduw is niet goed, belijning kan nog net wat beter, eigenlijk dragonflycave, maar dat is eindkeuring". Kleurronde in `sprite/k1/` e.v.
- Jordi (24 nov): "en op de tweede rij van boven, met het driehoekje, daarnaast interpreteerde ik als een stuk ruine dat gebroken is, dus die moet dan hetzelfde gelijnd worden als het driehoekje ernaast, neem dat ook mee in de keuring".
- Kleurrondes k1–k2 (verse kleurmaker, DC): mos ×2 in 3 tinten, steen 6 tinten warm→koel, volume per steen, ruïneblok gelijnd als de gevel; eindkeuring k1 BIJNA, k2 BIJNA (1 lichte steen rechtsonder tegen het licht in + 2 px bultje), door Claude opgelost in k3 (35 px) → eindkeurder: "Na reparatie 1 (en eventueel 2) is het voor mij een PASS". `af/tempel.png` = `sprite/k3/`.
- Jordi over k3 (24 nov), met omcirkelde zones (`referenties/jordi_omcirkeld_k3.png`: bergwand, zijvlakken van de terrassen, zijvlak onderste blok): "het grootste deel is goed, maar er zijn nog teveel effen vlakken, zie alles wat ik omcirkeld heb, lijkt gewoon willekeurig gedaan, de zijkanten van de driehoeken ook, naast de deur rechts heb je een willekeurige horizontale streep, plus nog meer willekeurige vlakken, daardoor leest het perspectief niet goed, moet echt beter, de rest is allemaal uitstekend".
- Jordi: "dus puur kleurtinten, schaduw, lijnen". Kleurronde k4 (verse maker).
- k4 (zijvlakken per vlak + stenen) → keurder FAIL (mozaïek, zijvlak en bergwand gelijk); k5: drie toonzones uit het model (lichte bovenranden, middengrijze zijvlakken met grote stenen, gladde donkere bergwand), gevelplaten met lichte nok → keurder PASS; k6 = k5 + voegen in f-vlakken in e (26 px, optionele keurderreparatie, door Claude). `af/tempel.png` = `sprite/k6/`.
