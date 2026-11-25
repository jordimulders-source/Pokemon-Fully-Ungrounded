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
