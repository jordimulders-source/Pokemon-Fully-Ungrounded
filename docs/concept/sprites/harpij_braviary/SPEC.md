# Harpij (Rufflet-splitevolutie) – SPEC

**20 nov gewijzigd:** geen Braviary-vorm meer maar een **nieuwe soort volgens het Perrserker-idee**: regionale Rufflet → harpij, gewone Rufflet → Braviary (zoals Galar-Meowth → Perrserker), gebaseerd op de harpij-arend (Amazone). Map heet nog `harpij_braviary`. Achtergrond: `docs/concept/IDEEEN.md` → Harpij-arend.

## Jordi letterlijk
- 9 nov: "We gaan voor een eigen braviary vorm"; Rufflet gaat mee: "klinkt goed".
- 9 nov: "steel/flying tof".
- 20 nov (meerkeuze): eerst Braviary, daarna Rufflet · type Steel/Flying, besloten · Steel-gevoel zit in de **klauwen** · daarna: "klauwen en snavel allebei" · pose: **zittend, kuif op** (voorstel Claude: rechtop, kuif opgezet, klauwen zichtbaar, geen ondergrond).
- 20 nov: "de kuif maken wij iets stilistischer dan irl" · "want daar zitten de veren een beetje verspreid".

## Gemini-rondes
- r1 (`gemini/r1.png`), Jordi: "eigenlijk al wel tof, alleen ik herken braviary nog niet echt erin, de pose is niet helemaal driekwart en we zien de kuif zo niet goed, plus de klauwnagels zijn alleen van staal". Op de vraag wat dat laatste betekent: hele klauw staal (niet alleen de nagels).

- Na r1, Jordi: "weet je wat ik kijk en zie dat die niet eens heel ver van braviary afwijkt, maar misschien dat we rufflet dan hetzelfde houden en dat we hier gewoon een andere vorm van maken in dezelfde lijn" · op de vraag hoe: splitevolutie · "Harpiary ofzo (betere naam bedenken)".
- r2 (`gemini/r2.png`, prompt v2), Jordi: "De klauwen zijn goed, de kuif is nog niet iconisch genoeg, ik vind hem ook iets te buff".
- r3 (`gemini/r3.png`, prompt v3), Jordi: "hij is te compact, te stocky. Ik zal bij de volgende een bronfoto erbij doen, de kuif is wederom niet goed".
- r4 (`gemini/r4.png`, prompt v4 + bronfoto), Jordi: "ok nu komen we ergens, alleen is die nu iets te realistisch en iets te weinig pokemon. De klauwen mogen volledig van steel, de strepen op de poten gaan niet goed vertalen naar een sprite dus daar moeten we iets mee, en de veren mogen iets meer een harpy look krijgen, dat die meer een pokemon wordt, misschien iets meer nog, dat het een meer overdreven feature wordt".
  Op vragen: "de veren" = de kuif · strepen: een paar dikke banden (voorstel Claude, gekozen) · aanpak: nieuwe startprompt.
- r5 (`gemini/r5.png`, prompt v5), Jordi: "ik zou graag 2 veren erbij willen op de kop, hij heeft alleen de kleuren van de klauwen veranderd maar ze lijken nog niet echt van staal. De strepen zijn beter" · "de nieuwe veer positie is ook goed".
- r6 (`gemini/r6.png`, bijsturen), Jordi: "klauwen zijn goed, maar hij voegt maar 1 veer toe en aan de verkeerde kant, ik wilde lager 2 veren erbij, laten we dat in een nieuw gesprek proberen". Op vragen: aan elke kant 1 veer erbij (lager) · bijlage r6 (met de r6-extra veer links weer weg).
- r7 (`gemini/r7.png`, nieuw gesprek met r6), Jordi: "dit gaat fout. Vraag maar alleen om extra veren". (Gemini haalde 2 veren weg en zette de nieuwe veren als oren opzij van de kop.)
- r8 (`gemini/r8.png`, nieuw gesprek met r6), Jordi: "Gemini snapt er helemaal geen bal van, ik heb nog 1 suggestie, laten we vragen of die van de veren een soort hoofdtooi kan maken, misschien dat die het dan wel doet".
- r9 (`gemini/r9.webp`, hoofdtooi), Jordi: "ben bang dat dit hem ook niet is, hij heeft de verkeerde stijl veren erop geplakt".
- Jordi daarna: "kan jij eens kijken of jij het kan, je kan alleen de veren niet copy pasten, je moet ze precies in dezelfde stijl maken maar een andere vorm" · "maak een paar varianten". Claude tekende op r6 (natief raster ±99 px, `plak/`) 1 veer per kant: varianten A–D.
- Jordi: "ik vind D het beste gelukt, al best mooi" · "Kan je misschien nog de veer die Gemini er neer heeft gezet ook nog in lijn met de rest maken? Dan is die niet symmetrisch maar dat is irl ook niet". Varianten D+E/F/G (`plak/varianten_midden.png`).
- Jordi: "houd de bodem van de veer hetzelfde, alleen de top, zodat die niet volledig recht is" → varianten H/I/J. Jordi: "vind ze allemaal nog niet mooi, maar dat fixen we in de sprite wel, ga maar met D+J verder en bouwen".
- Sprite: Jordi "ga maar met D+J verder en bouwen" · over ronde 2: "doe puur pixel fixes en teken niks opnieuw" · "het oog is een beetje onafgemaakt" · "r1 is beter dan r2 qua oog, maar mist een paar pixels aan de onderkant denk ik" · "en is teveel een vierkant" · "de veren op het hoofd mogen wat poetswerk nog, behalve de meest rechtse twee, die zijn erg goed al" · "qua vorm" (die twee bevroren).
- Over r3: "juist we gaan de goede kant op. Het strepen patroon bij de poten is verdwenen, maar ik zie daar wel nog teveel rechte lijnen, ook de poten zelf zijn teveel rechte lijnen. Je gaat me toch niet vertellen dat ze opnieuw getekend zijn he? rechte lijnen bij het hoofd, de nek, rechts van de vleugel" · "kuif moet nog steeds netter". Oorzaak: r1-maker week 801/1380 px af van de kale reductie. r4 = verse maker vanaf de kale reductie (alleen 2 rechtse kuifveren en het oog uit r3). Jordi: "oog c" (`sprite_r3/harpij_r3c`).
- Over r5: "het hoofd mist contrast" · "de kuif is minder mooi" (dan r4; r5 liet de donkere banden vallen) · "de kuif kan juist wel wat zwarte lijnen gebruiken".
- Over r6: "het strepenpatroon bij de poten is nu toch weer terug, prima" · kuif: "B is beter ja" · "de snavels zijn allebei niet goed" (r6 en r5) · "dat hoort geen rechte streep te zijn, kijk naar het model" · "kijk naar braviary en andere roofvogels" · "een paar pixels die de scherpte van de snavel tonen zijn genoeg" · snavelvarianten r7: "V2 is het beste, maar ook gelijk too much, de mond mag wat subtieler, zie pidgeot. Je moet ook de snavel niet opnieuw tekenen" · "V2 heeft het beste kleurgebruik".
- Over r8: "Ja r8 is goed, nu nog eindkeuring, schaduwen, kleuren, belijning, dragonflycave, consistentie, gen 3 sprite etc".

## Model
`model/model_natief.png` (natief raster van r6, 99×99, met Claude's veren: D + middelste veer J). `model/model_10x.png` = 10× vergroot. Bevroren, behalve:

## Toegestane afwijkingen van het model (alleen deze)
1. Middelste kuifveer: Jordi vindt de varianten H/I/J "allemaal nog niet mooi, maar dat fixen we in de sprite wel" → in de sprite met Jordi verbeteren. Voorstel Claude: de getekende veren krijgen een lichte en donkere kant zoals de Gemini-veren.
2. Kleur, schaduw en volume naar Gen 3 (SPRITE_KERN: kleur mag altijd afwijken).

## Regionale Rufflet
- 20 nov: "Rufflet wordt juist regionaal" · "Perrserker idee": de regionale Rufflet evolueert in de harpij.
- 20 nov: "Rufflet wordt puur flying".
- 20 nov: "beetje deze inspiratie voor rufflet", met een foto van een harpij-kuiken (kwam niet als bestand binnen; beschrijving Claude): staand jong in een nest van takjes, kop naar links in profiel; witte donzige kop met een rommelige, rechtopstaande witte donskuif achterop; zwarte haaksnavel, licht open, roze tong; donker oog, dicht bij de snavel; wit donzig lijf (borst en buik), vleugels half gespreid en hangend, grijs met witte randen, rechtervleugel met een zwarte vlek onderaan; dikke gele poten met grote zwarte klauwen.

## Open
- Kleur: Gemini-prompt r1 vraagt harpij-kleuren (voorstel Claude); Jordi beslist bij het model.
- Naam: gepauzeerd (Jordi, 20 nov: "pauzeer de naam, ik dacht dat het grappig was om het te laten lijken op braviary"); werknaam Harpiary.
