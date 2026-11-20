# Hoatzin fase 2: retro eerste ontwerp (19–20 nov)

Jordi (20 nov): "ik heb sowieso niet het gevoel dat we een mooie sprite aan het maken zijn, misschien klopt het hele ontwerp wel niet" → "Ik denk dat B gaat helpen [vereenvoudigen], laten we helemaal from scratch beginnen".

## Wat moeilijk was (ervaring Claude, 25 spriterondes + 8 Gemini-versies)
1. **Kuif van dunne haren.** In het model ±⅓ spritepixel breed. Werd bij elke aanpak iets fouts: bruine massa/helm, tijgerstrepen, kam van staafjes, barcode, 1-px-lijnen "zonder kleur, contrast". Een kuif moet op 64 px uit een paar stevige vormen bestaan.
2. **Vleugel vol smalle lichte streepjes.** Werd ruis, dambord, "lappendeken" of één dood donker vlak; pennen en schachten lieten zich niet tegelijk leesbaar maken.
3. **Eén kleurfamilie.** Vleugels, nek, lijf, verre vleugel en staart allemaal pruim/mauve; alleen helderheid verschilt. Daardoor "lopen de onderdelen in elkaar over" (Jordi), hoe vaak er ook binnenlijnen bij kwamen. De echte hoatzin heeft juist contrast (kastanje vleugels, lichte nek, roestrode buik).
4. **Pose met gespreide vleugels.** Vult het hele vak; kop, oog, kuif en gezicht (het interessantste) krijgen maar een paar pixels.
5. **Realistisch model.** "Draw a REAL hoatzin" gaf een herkenbare vogel, maar met echte-vogeldetail (veel veren, dunne strengen) dat niet naar Gen 3 vertaalt. Gemini verloor bij elke bewerkingsronde kwaliteit (snavel, scherpte).
6. **Werkwijze.** Keurders stuurden op pixelregels; de sprite werd technisch netter maar niet mooier (Jordi: "we zijn echt geen stap verder sinds ik de lijnen heb gezet").

## Wat wel werkte
- Blauw gezicht + rood oog met zwart puntje (Latios/Sharpedo-vorm), haaksnavel, paarse gistbuik (variant D), donkere staart: Jordi keurde deze goed.
- Pixelblad (gehele 3×-verkleining, modus per blok) gaf de juiste vorm; Jordi: "de rest klopt qua vorm".
- Jordi's lijnen op een raster naast het model (r16) waren de duidelijkste feedback.

## Ontwerp 2, sprite s1–s9 (20 nov): waarom het weer vastliep
- Het ontwerp zelf werkt (Jordi: "een stuk simplistischer"); de vorm via kale reductie was snel goed (s2–s5).
- Daarna kostte "niet blurry" 5 rondes: makers en keurders werkten in kleine pixelreparaties en regels, terwijl Jordi steeds hetzelfde zag: te weinig tinten per onderdeel (meestal 2, alleen de buik 3), te weinig schaduw/contrast, tinten die willekeurig lijken in plaats van de vorm te volgen.
- Een keurder gaf PASS (s8) waar Jordi het blurry vond: de keuring keek naar regels, niet naar "ziet het eruit als een echte Gen 3-sprite".
- Palet (15 kleuren) dwong tot samenvoegen; daardoor kreeg de snavel de nekkleur. Budget per kleurgroep vooraf uitrekenen.
- Beter voor de volgende sessie: eerst per onderdeel een bestaande sprite kiezen als voorbeeld (honchkrow-vleugel, staraptor-borst, skarmory-poten, pidgeot-kuif) en de tintverdeling daarvan overnemen op de bevroren vorm, in één ronde; dan pas keuren, en Jordi's oog als maatstaf.
