# Gengas (SPEC)
Eindvorm van de convergente Gastly-lijn: Dustly → Hauntflare → Gengas. Cosmic/Poison (Jordi, 15 nov: "cosmic/poison is goed").

## Jordi letterlijk
- 13 nov: "Ik wil Gastly een buitenaardse gaswolk maken die dan logisch evolueert van een andere vorm haunter en gengar gebaseerd op verschijnselen die in de ruimte plaatsvinden. Het moet echt convergent zijn he."
- 15 nov: namen "zijn definitief"; "laten we beginnen met gengas, want dat is de meest complexe van de drie, hoe zullen we die maken?"

- 15 nov (ontwerp): "gengar is te herkennen aan zijn ogen en zijn mond, plus de oren. Maar vooral ogen en mond moeten exact hetzelfde blijven. Je kan er een bol gas van maken met wolkenbanden, je kan de armen en de poten om hem heen laten zweven als een soort manen idee, dus dat het armen en poten zijn, maar dat ze disconnected zijn. voor de rest is het een toedscruel, wiglett/wugtrio idee, dus convergent, lijkt erop, maar wel een duidelijk andere vorm. wat vind je hiervan? Samen met wat van jouw suggesties"

## Basis (besloten)
- Verschijnsel: bruine dwerg (Claude, door Jordi gekozen via de naam Gengas en de lijn in `POKEMON.md`).

## Ontwerp
- 15 nov: "oren mogen van gas, schrijf de prompt maar" (na de tabel van Claude: ogen en mond exact Gengar; bol gas met wolkenbanden; vier losse ledematen als manen (Jordi); voorstellen Claude: magenta-paars met banden, oren als gaslussen, geen rugstekels, stompe ledematen met kratertextuur, dunne methaanband (in de prompt weggelaten: GEMINI.md verbiedt gloed/effecten)).
- Prompt: `gemini/PROMPT_r1.md`. Werkwijze: Gemini-model van Jordi → `SPRITE_WERKWIJZE.md` "Gemini-model namaken".
- 15 nov, Gemini r1 (`gemini/r1_a.png`): "wat vind je hiervan? Ik twijfel over de oren en de kleur, de benen zweven nog niet genoeg"
- 15 nov: "nee de kleur moet juist minder dicht bij gengar, dat is leuker. verder eens" (eens met Claude: oren gevuld in Gengars vorm van gas; ledematen allemaal los met gat, voeten onder de bol, handen als Gengars handen). Prompt r2: `gemini/PROMPT_r2.md`, kleurregel A/B/C ter keuze.
- 15 nov, Gemini r2 (`gemini/r2_a.png`): door Jordi gestuurd zonder commentaar.
- 15 nov over r2: "ik vind het nu teveel een rots, terwijl die van gas moet zijn, plus gemini past amper iets aan". Prompt r3: `gemini/PROMPT_r3.md` (nieuw gesprek, alleen Gengar als bijlage).
- 15 nov over r3 (`gemini/r3_a.png`): "Beter, alleen de pose is niet goed driekwart. Geef hem echt de brown dwarf kleuren". Prompt r4: `gemini/PROMPT_r4.md`.
- 15 nov: "de pose mag echt zwevend zijn dus dat het duidelijk een hemellichaam is ipv staand, met de armen en benen op een beetje onnatuurlijke posities om aan te tonen dat die om hem heen draaien". Prompt r5: `gemini/PROMPT_r5.md`.
- 15 nov over r5 (`gemini/r5_a.png`): "lichaam ben ik tevreden over, alleen kijkt die denk ik iets teveel zijwaarts, wat vind je van de handen en voeten? die kunnen we altijd zelf nog anders positioneren"
- 15 nov: "doordat ze juist niet exact in de positie zitten waar handen en voeten horen is het duidelijk dat ze zweven lijkt me. Ga eens kijken wat je kan doen en toon mij een paar modelversies voordat we gaan bouwen" · "zorg wel dat het een bol blijft he". Modelindelingen: `model/indelingen_v1.png`.
- 15 nov: "ik ben fan van 3" → indeling 3 (schuine baan) gekozen. Model op spritemaat: `model/gekozen_v3_natief.png` (74×74 natief → 64, lijf 86%), `model/kleurgids_64.png`, `model/silhouet_64.png`.

## Opdracht sprite (ronde 1)
Jordi letterlijk (alles hierboven) + afgesproken met Jordi:
- Ogen en mond exact Gengar (Jordi); Claude-voorstel dat Jordi met "alright" aannam: ogen en grijns pixel voor pixel uit de Gen 3-Gengar, iets meer naar het midden van de bol (twee posities tonen).
- Lijf: een bol (Jordi: "zorg wel dat het een bol blijft he"); banden, wervel, lichtvlek en oren uit het model (Jordi: "lichaam ben ik tevreden over").
- Ledematen: indeling 3 (Jordi). Claude-voorstellen uit de r5-bespreking (Jordi: "alright"): voor = groter en lichter, achter = kleiner, donkerder, half verstopt; iets donkerder en warmer grijs dan het model; handen met Gengars drie stompe vingers, voeten in Gengars voetvorm (Jordi r1: "verder eens"); 2–3 grotere kraters per maan.
- 15 nov: "toon voordat je gaat bouwen nog jouw opties voor ogen en mond posities" → `model/gezicht_opties.png` (A/B/C, Gengar-pixels op de kleurgids; schets).
- 15 nov over de gezichtsopties: "Het is lastig om te zien, want het is heel slordig knip en plakwerk".
- 15 nov: "C sowieso niet iig" (gezichtspositie C valt af; keuze tussen A en B).
- 15 nov: "ik neig toch naar A, ga maar bouwen daarmee" → gezicht op plek A (Gengar-pixels verschoven dx −6, dy +5 t.o.v. de Gengar-sprite). Bouw ronde 1: `sprite_r1/`.
- 15 nov over ronde 2/3: "die manen heb je opnieuw getekent, waardeloos idee, want jij kan geen handen en voeten tekenen. Dit zijn nu gewoon willekeurige vormen. Daarnaast heb je het linker oor niet goed nagedaan en onder het rechte oor heb je gewoon maar een vlak ingevuld wat er helemaal niet is, ook de krul in de planeet zelf is niet mooi, net als de schaduwen etc. Ogen en mond lijken teveel erop geplakt, die moeten beter aansluiten qua, kleur, schaduw, lijnen en ze mogen iets groter"
- Nieuwe basis (Claude): het model zelf, 74 → 64 door rijen/kolommen te schrappen (`model/schrap.py`, `model/model_64_geschrapt.png`, vergelijking `model/geschrapt_vs_r3.png`); r1–r3 afgekeurd.
- 15 nov: "moet nog veel beter, werk tot je bij een goede eindversie komt en stuur dan pas door naar mij" · "en kap aub met dingen zelf tekenen from scratch". Werk: `sprite_v2/` (model opschonen, niets hertekenen).
