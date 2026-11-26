# Gaucho-Lotad-lijn (regional form)

Lijn: Lotad → Lombre → Ludicolo (drie fases, geen vierde).

## Besluiten Jordi (25 nov), letterlijk
- Idee (9 nov): "Gaucho-Pokémon met hoed"; lichte voorkeur voor gaucho als Lotad-vorm.
- Over de opties lelie/gebied/overlap met de mate-lijn: "dit is allemaal niet belangrijk, laten we over ontwerp praten".
- "een plant die gaucho is, geen kleding, geen accessoires".
- Gaucho in alle drie de fases: "kan eventueel, maar alleen met een goed idee".
- "nee geen vierde fase".
- "Gras en water gaat eruit".
- "lotad ground, vanaf lombre fighting" (Lombre en Ludicolo: Ground/Fighting of puur Fighting nog open).

## Ronde 1 (25 nov)
- `r1/gemini_r1.png` (startprompt v1). Jordi: "ja tof idee, dit gaat werken, en dan wordt het steeds meer een cowboy hoed per evo. Alleen het lichaam is net iets te groot denk ik"; "vergeleken met lotad"; "ofja steeds meer gaucho hoed"; "die lijken op cowboy hoeden".
- `r1/lijf_varianten.png`: lijf door Claude geschaald onder de hoed (100/85/75/65 %), naast de Gen 3-Lotad; hoed onaangeroerd.
- `r2/gemini_r2.png` (v2, Lotad-bijlage): Jordi "veel minder op alle fronten".
- `r3/gemini_r3.png` (v3): Jordi "dit klopt niet, het is nu gewoon een semi pallette swap, er zit geen gaucho meer in".
- `r4/gemini_r4.png` (bijstuur v4 in r1-gesprek): armen weg, 4 poten; Jordi "nu is die geamputeerd".
- `r5/gemini_r5.png` (bijstuur v5): Jordi "nee dit werkt ook niet, we kunnen r1 doen, maar dat ontwerp heeft teveel detail voor een sprite".
- `r6/gemini_r6.png` (v6, r1 in woorden + weinig detail): Jordi "nee weer veel minder mooi".
- Jordi daarna: "ik vind het ontwerp nu prima dat die maar op 4 poten staat".
- `r7/gemini_r7.png` (v7 = v1 + één regel eenvoud): Jordi "is dit echt een vergelijkbare prompt als r1 ja?".
- `r8/gemini_r8_{1,2,3}.png` (v7 nog 3×): Jordi "Hij doet elke keer iets heel anders, de eerste vind ik wel erg tof, maar die mist 2 poten". `r8/poten_B.png`: Claude plakte 2 kopieën van de linkerpoot erachter (tussen de bestaande poten); verder niets veranderd.
- Jordi daarop: "nee extra poten toevoegen gaat niet lukken".
- Jordi: "anders schrappen we die 2 poten, zelfs ik wist niet dat lotad 4 poten had" → **model = `r8/gemini_r8_1.png`, op 4 poten** (bevroren).
- Jordi: "we bevriezen dit model, alleen we pakken de kleuren van r1"; "de ogen komen uit de bestaande lotad, dat zijn witte cirkels met een zwarte stip erin".
- `r8/r8_1_kleuren_r1.png` (script `r8/kleur_r1.py`): r8-1 per deel (hoed, gezicht, snavel, kraag, poten) op lichtheid omgezet naar de kleuren van dat deel in r1; ogen = Lotad-oog (wit rondje, zwarte stip). Alleen kleurproef.
- Jordi: "doe dat omzetten pas bij de sprite, want nu wordt het model wss lastiger om na te maken" → **model blijft `r8/gemini_r8_1.png` onaangeroerd; r1-kleuren en Lotad-ogen pas in de spritefase.**

## Open
- Welke hoed (plat met brede rand, boina, anders).
- Of hangend blad / uitlopende stengels als "plant die gaucho is" lezen of al als kleding.
- Kleur en pose: niet genoemd.

## Rondes
Prompts in `gemini/PROMPT.md`.

## Frontsprite
- r1–r2 maker (`sprite/r1`, `sprite/r2`). Jordi over het oog: "houd er rekening mee dat het lotad oog lichtblauwe pixels heeft omdat het op een blauw lijf is gebouwd, dus die maak jij een tint van het bruin van het lichaam, zoals de originele lotad het doet".
- Jordi op r2: "linkeroog valt iets teveel weg, verder vind ik hem goed" → r3 = r2 + ver oog wit met zwarte stip (2×2: wit|zwart boven, lichte lijftint eronder).
- Jordi op r3: "nee, te klein" → `sprite/r3/oog_ABC.png`: A = r3, B = 2 px breed (zwarte stip + wit + lijftint, rechterdeel van het nabije oog), C = volledig Lotad-oog 3×3.
- Jordi: "de blik klopt nog niet, hij kijkt niet goed driekwart" → `sprite/r3/oog_DEF.png`: pupillen 1 px naar links (kijkrichting); D = ver oog 2 px, E = ver oog 3×3, F = ver oog 2 px 1 kolom verder naar de rand.
- Jordi: "ze kijken nu niet driekwart maar zijwaarts" → `sprite/r3/oog_GHI.png`: pupillen naar rechts (naar de kijker); G = nabij midden + ver 2 px stip rechts, H = beide stip rechts, I = nabij midden + ver 3×3 stip rechts.
- Jordi: "G" → basis voor de eindkeuring: `sprite/r3/lotad_gaucho_oogG.png`.

## Lombre (fase 2)
- Jordi (25 nov): "de regional lombre, lotad is al af". Startprompt v1 in `lombre/gemini/PROMPT.md` (opzet Lotad-v7; keuzes van Claude daar vermeld).
- `lombre/r1/gemini_r1.png` (v1): Jordi "vind deze alweer vrij prima".
- Jordi op r1: "1 hoeft ook geen blad meer te zijn, ik vind de kleding ook echt lichaamsonderdelen, tas of riem zie ik ook niet. rechtop is prima want hij wordt fighting. de mond past niet bij lombre alleen, die is bij hem geen snavel, de ogen zoals lombre maar dan wat bozer zoals hier is prima". Alleen de mond verandert; bijstuurprompt v2 in `lombre/gemini/PROMPT.md`.
- `lombre/r2/gemini_r2.png` (bijstuur v2, mond): Jordi "dit kan die niet".
- Jordi: model = r1 (mond niet via Gemini). Mondkleur: "de kleur die de snavel van lotad heeft". Mondvorm uit de Gen 3-Lombre, in varianten ter keuze; spritefase gestart (`lombre/sprite/r1/`).
- Sprite r1 (maker): mondvarianten A/B/C (`lombre/sprite/r1/`). Jordi: "A is het beste maar mag iets kleiner" → `kleiner.py`: A1 (1 kolom geschrapt), A2 (2 kolommen), A3 (1 kolom + 1 rij), A4 (2 kolommen + 1 rij), uit de Lombre-mond geschrapt, niets hertekend; `mond_kleiner_vel.png`.
- Jordi: "a1 is de vorm van het mond het beste, a2 sluit die beter aan maar is de hele vorm van de mond weg" → A5 = vorm A1, 1 px naar rechts (`mond_A1_A2_A5_vel.png`).
- Jordi: "A5 akkkord maar zorg dat het hoofd verder consistent is, daarnaast valt het linkeroog nu teveel weg en is het rechteroog nog net niet genoeg lombre maar dan bozer" → sprite r2 (maker).
- Jordi bij r2: "ah excuses die sprite helpt niet, hier zie je hoe lombre er uit ziet" + 3 plaatjes (`lombre/referenties/`: anime, 3D, artwork). Ogen opnieuw naar deze Lombre-ogen (r3).
- Jordi op r3: "a is het beste maar de blik is niet naar driekwart" → r4: alleen pupilplaatsen, lid van A blijft.
- Jordi: "behoud hem maar, anders klopt die niet meer"; tussen r3 A en r4 A: "links" → **r3 A** (ver oog 2 px) is de basis voor de keuring en eindkeuring.
- Keuring + DC-eindkeuring (`lombre/eindkeuring/KEURING.md`, 75 px). Jordi: "commit en push naar main" → **af**: `lombre/af/lombre_gaucho.png`. Ter info open: vest/laarzen één olijftint, Lombre roder dan Lotads terra (palet kan), Ground/Fighting of puur Fighting.

## Ludicolo (fase 3)
- Jordi (25 nov): "tijd voor gaucho ludicolo". Startprompt v1 in `ludicolo/gemini/PROMPT.md` (opzet Lombre-v1; keuzes van Claude daar vermeld).
- `ludicolo/r1/gemini_r1.png` (v1).
- Jordi op r1: "op zich wel leuk deze vorm van de hoed, zolang het maar herkenbaar een gaucho hoed is. Waar lombre wat meer boos is, is deze heel comfortabel, misschien dat we nog 1 specifiek design kenmerk moeten toevoegen om deze ludicolo te laten opvallen en ietsje anders te maken dan de base versie". Voorstellen Claude: gauchosnor van bladeren, bombacha-benen, halfdichte ogen (keuze open).
- Jordi: "rode punt rechtsonder is de staart".
- Jordi: "meh we hebben al veel snorren gegeven aan pokemon, misschien wat meer een poncho?" → bijstuur poncho (blad over de schouders).
- `ludicolo/r2/gemini_r2.png` (bijstuur poncho): Jordi "ok maar hoe zouden we de poncho meer onderdeel van zijn lichaam kunnen maken".
- Jordi over de poncho: "ik weet niet of ik met de leaf kleur het eens ben gezien de typing"; "maar het moet geen kledingstuk zijn he".
- `ludicolo/r3/gemini_r3.png` (bijstuur: bladflappen in lijfkleur): Jordi "nu doet die alsnog bladeren". (Fout Claude: prompt vroeg zelf om bladflappen en nerven.)
- Jordi plakte r1 zelf terug ("omdat ik dat de beste vond"); bijstuur "lijf als poncho-mantel" niet gebruikt. Jordi: "kijk dit is gewoon goed alleen dit lichaam moet gewoon iets meer natuurlijk als een poncho vallen".
- Volgende: bijstuur "lijf valt als een poncho" (smal bij de hals, schuin over de bovenarmen, punt voor, zachte plooien) op r1, met r1 als bijlage.
- `ludicolo/r4/gemini_r4.png` (bijstuur poncho-val op r1, r1 als bijlage): Jordi "hij valt iets teveel over het lichaam heen denk ik, plus de rest van de sprite is nu minder geworden".
- `ludicolo/r5/gemini_r5.png` (bijstuur korte poncho op r1): Jordi "wat vind je hiervan? Het blad moet wel anders".
- Jordi over r5: "is die nu te kort? of leest het wel"; "misschien bij het lichaam iets langer dan?" → bijstuur langer.
- `ludicolo/r6/gemini_r6.png` (bijstuur iets langer): Jordi "kan jij die poncho nu in de bladeren over laten lopen? en misschien de vorm iets bij poetsen zodat die meer poncho dan bladeren lijkt? Zo ja, dan kan je bouwen". Claude vroeg: A (basis r6) of B (basis r5).
- Jordi: "imo is het niet plakken maar alleen inkleuren"; "de poncho". → **model = `ludicolo/r6/gemini_r6.png`**; spritefase gestart (`ludicolo/sprite/r1/`, maker): silhouet = model, alleen de inkleuring van de poncho mag zo dat hij bovenaan als poncho leest en onderaan in de bladpunten overloopt; varianten ter keuze.
- Jordi: "het enige waar je in afwijkt van het model is het lijnenwerk van de poncho, om het iets meer af te laten wijken van de bladeren, let op, dit betekent niet opnieuw tekenen, hooguit de bladervorm met wat pixels schuiven omzetten en anders inkleuren".
- Sprite r1 (maker, `ludicolo/sprite/r1/`): 0 = kale reductie (51×62), A/B/C = alleen ponchobladlijnen omgekleurd (38–44 px, 0 verschoven); `vel.png`.
- Jordi: "stuur de eerste maar naar de eindkeuring en let op de zwarte lange verticale lijn in de poncho" → variant 0 naar keuring + DC-eindkeuring (`ludicolo/eindkeuring/`).
- Jordi: "het geel moet zoals de rest van de lijn, afwijken van model" → geel = tinten van de Lotad-snavel/Lombre-mond.
- Jordi: "en het rechteroog heeft nog niet de perfecte vorm"; "mag iets ovaler" → doorgegeven aan de eindkeuring (2 oogvarianten).
- Keuring + DC-eindkeuring (`ludicolo/eindkeuring/`, 127 px, alleen indexwissels/palet): zwarte ponchobinnenlijnen (o.a. x19 y40–50) → rode lijn, dubbele lijnen 1 px, rood uit elkaar getrokken, geel = Lotad/Lombre. Rechteroog los: `oog_A`/`oog_B` (2 px elk), keuze Jordi.
- Jordi: "de ogen moeten nog wit" → `eindkeuring/oog_{A,B}_wit.png` (irispixels → wit, `oog_wit.py`).
- Jordi: "de mond moet nog wel wat duidelijker omlijnd worden zodat duidelijk is dat die ietwat uitsteekt, heeft het model wss ook, rechts is beter trouwens" → oog B (wit); `eindkeuring/mond_V1.png` (rode lijn om de snavel, 22 px) en `mond_V2.png` (idem, onderkant zwart), `mond_lijn.py`.
- Jordi: "ja rechts is goed" (V2) → `ludicolo/af/ludicolo_gaucho.png` (voorlopig); "stuur die maar naar de eindkeuring" → eindkeuring ronde 2 (`ludicolo/eindkeuring2/`).
- Eindkeuring ronde 2 (`ludicolo/eindkeuring2/`, 15 px snavelrand: zijkanten rode lijn, onderkant doorlopend zwart, clusters weg). Ter info: donkere band van 3 px boven de ogen.
