# Vlieglijn fase 2 (mug) – SPEC

Lijn: **vlieg → mug, 2 fases** (Jordi, 20 nov). Mug = **Poison/Electric** (Jordi, 22 okt). Fase 1 = robotvlieg, Bug/Electric (`../vlieglijn_fase1/af/vlieg.png`, SPEC daar). Evolutie: "Omdat het maar 2 fases is kan die ook prima op lvl 30 pas evolueren ofzo" (Jordi, 20 nov). Naam: open.

## Al vastgelegd (uit POKEMON.md / IDEEEN.md)
- Inspiratie (POKEMON.md): het zoemen (Electric, vleugelslag als elektrisch gezoem), de steek en de ziektes die muggen overbrengen (Poison: malaria, dengue). Ideeën: een steek die gif + verlamming kan geven; zwermen in de Amazone en het Pantanal.
- Rol (IDEEEN.md): "Mug als bug (Jordi): iets minder early route, een beetje zoals Kricketot in Sinnoh; verschijnt zodra je in lager/warmer gebied komt".
- Fase 1 (bevroren): grijze ronde kop zonder mond met een zwart LED-vizier en een lichtpaarse ^ in elk oog, korte voelsprietjes, zwart borststuk, grijs-zwart gestreept achterlijf, twee lichte vleugels plat naar achteren, zes poten als stroomkabels (ronde kabel met glans, witte ringen bij de knieën, twee koperdraadjes als klauwtjes).

## Model
`referenties/gemini_gekozen_r1.png` (= `gemini/r1.png`), bevroren (Jordi, 21 nov: "ja r1 is het model, 56×63 akkoord"). Sprite 56×63 in het 64×64-kader.

## Toegestane afwijkingen van het model
(geen)


## Jordi letterlijk
- 21 nov (sessiestart): "Hoe de mug uit de vlieg voortkomt: welke kenmerken van fase 1 terugkomen (LED-ogen, kabelpoten, robotisch/mechanisch, kleuren) en wat nieuw is (steeksnuit, grote voelsprieten, Poison)." · "Pose en grootte als eindvorm."

- 21 nov, keuzes: "belangrijk is dat als een nieuwe fase moet tonen. We gaan de mug niet super gedetailleerd maken, want dat vertaalt niet. Hij wordt electric/poison en ik wil dat robot element nog een beetje behouden.  De snuit en poten kunnen niet te dun want dat vertaalt niet. De leds behouden maar \   / als meer boze look lijkt me geinig, paars nog steeds ja." · "De steeksnuit mag idd een soort robotische naald zijn. Hij is vliegend in de pose met de snuit klaar om aan te vallen. Hij moet groter zijn, maar niet dik worden"
- Niet beantwoord (dus niet ingevuld, aan Gemini gelaten): voelsprieten, kleuren buiten paars, hoe Poison zichtbaar is, of de kabelpoten/koperklauwtjes terugkomen.

## Rondes
- r1: prompt `gemini/PROMPT_r1.md` (nieuw gesprek, geen bijlage) → `gemini/r1.png`. Jordi (21 nov): "ik vind dit design echt fenomenaal. Zo vet. Vertaalt deze goed genoeg naar een sprite denk je?"
- Maattest (kale reductie, geen sprite): natief raster 6,83 px → 150×150, figuur 109×123; `maat/maten.png` op 46×52, 51×58, 56×63.
- Jordi (21 nov): "ja r1 is het model, 56×63 akkoord" → sprite r1 (maker).
- Sprite r1 (maker, 21 nov): `sprite_r1/mug_r1.png`; 202/1361 px afwijkend van de kale reductie (silhouet 0), 5 poten in het model (niets toegevoegd). Claude: trouw goed; ogen lezen op 1× nog niet als \ /.
- Keuring r1 (verse keurder): BIJNA; MOET: linkeroog leest als | i.p.v. \ (cel 16,24), om-en-om-rand linkervleugel, gele knie zonder lijn; MAG: achterlijf volume, 2 losse pixels. Model heeft 3 zichtbare vleugels en 5 poten. `keuring_r1/KEURING.md`.
- Sprite r2 (maker, 21 nov): keurdersreparaties, 10 px t.o.v. r1; verre oog variant B (3 px, schuine band) → leest \ /; MAG 1 en 3 niet gedaan (model spreekt ze tegen).
- Jordi (21 nov) over r2: "rechterarm en linkerpoot vallen een beetje samen, dat moet met kleurgebruik en schaduw opgelost worden" (lezing Claude, ter controle: de poot van het borststuk met het gele gewricht bij (35,36) en het linker Λ-been met de gele knie bij (24,45), die elkaar midden onder het lijf kruisen).
- Jordi (21 nov) over r2: "en hij is nog wat blurry"
- Jordi (21 nov): "maar je hoeft niks aan te passen verder behalve kleur, schaduw en belijning" · "de vorm is perfect" → silhouet/vorm van r2 bevroren (alpha-diff 0). · "niks opnieuw tekenen"
- Eindkeuring r2 (verse DFC-keurder): BIJNA → MOET arm/poot 8 px, scherp 14 px, volume achterlijf 13 px; MAG grijze selout vleugels/koepel 72 px; alpha-diff 0. Toegepast (MOET+MAG) als `sprite_r3/mug_r3.png`.
- Jordi (21 nov) over r3: "ja hij is nog blurry, verschil tussen poot en arm is net wat beter, maar nog steeds lastig om het verschil te zien"
- Jordi (21 nov): "volgens mij maakt 2 vultinten max een sprite ook blurry" · "dus misschien goed om naar de hele sprite daarvoor te kijken"
- Jordi (21 nov): "en kijk naar fase 3 van pitahaya draak proces, dat ging ook een tijdje fout" → lessen pitahaya fase 3 (scheidingslijn ledematen, palet donkerder/gespreid, verre ledematen 1 stap donkerder) aan de maker van r4 gegeven.
- Sprite r4 (verse maker, 21 nov): kleurronde, A (gematigd, 103 px) en B (sterker, 110 px), alpha-diff 0; poten 3 vultinten, kruising: Λ-been voor (glans), borstarm achter (donker, lijn x33); achterlijf nog troebel volgens maker.
- Jordi (21 nov) over r4 (krabbel `sprite_r4/krabbel_jordi_r4.png`, gele driehoek om het Λ: schuine poot naar de gele knie + onderstuk, en de rechte poot): "arm en poot lijken nog steeds verbonden hier, op alle 3". Model (`sprite_r4/model_driehoek.png`): twee losse poten, de rechte poot licht (voor), de knie-poot donkerder, met zwarte lijnen ertussen bovenaan en waar het onderstuk achter de rechte poot verdwijnt.
- Jordi (21 nov), met modeluitsnede `sprite_r4/jordi_model_uitsnede.png`: "in het model zie je het wel, leg het model op een pixelraster en kijk waar het zit" · "dat je niet hoeft te gokken" → `raster/raster.py` legt het model op het spriteraster (`raster/driehoek_model_vs_r4B.png`).
- Jordi (21 nov), krabbel op het raster `raster/krabbel_jordi_raster.png` (gele lus over r4B): "zo lees ik het een beetje"
- Jordi (21 nov): "de bovenarm is ook nog niet heel duidelijk te zien van dezelfde arm"
- Jordi (21 nov): "en wederom niks opnieuw tekenen he!" · "het is puur kleurgebruik"
