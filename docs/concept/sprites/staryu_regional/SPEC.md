# Regionale Staryu/Starmie: koekjes (27 nov)

## Jordi letterlijk
- "Ik denk nog aan carambola staryu/starmie"
- "serieus/grap geen idee, laten we allebei anders even proberen, maak prompts voor een carambola staryu en starmie en een chocolate chip staryu en starmie. Mochten beide vet zijn, prefereer ik carambola"
- Na r1: "Carambola Starmie vertaalt niet helemaal merk ik, omdat het twee sterren over elkaar heen is. Chocolate chip past beter, alleen de koekjes zien er een beetje bleek uit en zouden nog iets meer stijl kunnen gebruiken, zodat ze er echt lekker uit zien"; "dus daar gaan we voor"
- "en staryu kan dan bijv chocolate chip zijn en starmie allerlei versieringen (zolang het vertaalt naar een sprite"
- Na r2: "ze zijn beide nog wat saai en staryu is maar half gedecoreerd. Het mogen echt meer koekjes worden nog"
- Na r3: "ik vind deze twee wel lachen alleen ik twijfel over de vorm van het stukje koek achter de hoofdvorm van starmie"; gekozen: "zoals de echte starmie"
- Na r4 (achterkant): "hij is nu veel te puntig, maar dat valt in een sprite wel te fixen toch? Door naar de echte starmie te kijken?"; "nee geen 7, hij heeft de voorste ster alleen puntiger gemaakt"
- "ga maar bouwen"; "ja staryu r3"

## Modellen (bevroren)
- **Staryu:** `gemini/r3_staryu.png` (Jordi: "ja staryu r3").
- **Starmie:** voorste ster = `gemini/r3_starmie.webp` (voorstel Claude: r3 omdat r4 de voorste ster puntiger maakte; Jordi: "ga maar bouwen"). Achterste ster = vorm en hoek van de achterste ster van de Gen 3-Starmie (`graphics/pokemon/starmie/anim_front_gba.png` + `normal_gba.pal`), in de koekkleur met chips van de achterste ster uit het model.

## Open
Type, naam (regional forms: blijven Staryu/Starmie?), serieus/grap.

## Starmie-sprite: correctie Jordi (27 nov)
- Na r3 C1/C2 (voorste ster verkleind, gespiegelde Gen 3-achterster): "waarom neem je het model niet over?"; "je maakt hem ook steeds rechter"; "steeds minder driekwart pose".
- Dus: model r3 1-op-1 overnemen (pose, driekwart-perspectief, verhoudingen, achterpunten op hun modelplek en -richting). Alleen de vorm van de achterpunten puntiger zoals bij de echte Starmie, binnen het perspectief van het model.
