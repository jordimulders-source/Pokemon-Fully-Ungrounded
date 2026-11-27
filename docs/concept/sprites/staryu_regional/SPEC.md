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
- **Staryu:** `gemini/r4_staryu.png` (Jordi 27 nov: "staryu r4 is uitstekend ja"; driekwart). Eerder r3 ("ja staryu r3"), vervangen omdat die te recht stond (Jordi: "ben bang dat staryu ook te recht staat"); sprite r1–r3 van r3 blijft als naslag.
- **Starmie:** voorste ster = `gemini/r3_starmie.webp` (voorstel Claude: r3 omdat r4 de voorste ster puntiger maakte; Jordi: "ga maar bouwen"). Achterste ster = vorm en hoek van de achterste ster van de Gen 3-Starmie (`graphics/pokemon/starmie/anim_front_gba.png` + `normal_gba.pal`), in de koekkleur met chips van de achterste ster uit het model.

## Open
Naam (regional forms: blijven Staryu/Starmie?), serieus/grap.

## Starmie-sprite: correctie Jordi (27 nov)
- Na r3 C1/C2 (voorste ster verkleind, gespiegelde Gen 3-achterster): "waarom neem je het model niet over?"; "je maakt hem ook steeds rechter"; "steeds minder driekwart pose".
- Dus: model r3 1-op-1 overnemen (pose, driekwart-perspectief, verhoudingen, achterpunten op hun modelplek en -richting). Alleen de vorm van de achterpunten puntiger zoals bij de echte Starmie, binnen het perspectief van het model.

## Starmie-model gekozen (27 nov)
- Jordi over r4: "Deze was bijna goed, alleen geen driekwartpose en de punten zijn te puntig, dat moest meer als de normale starmie, alleen de punten minder puntig maken". Gemini kon driekwart + achterster niet samen (v5–v8). Keuze uit (1) r4 + punten in de sprite minder puntig, pose blijft zoals r4, of (2) plakken: "doe maar r4".
- **Model Starmie = `gemini/r4_starmie.webp`.** In de sprite: de achterpunten minder puntig, zoals de normale Starmie. Pose zoals r4.

## Staryu af (27 nov)
Jordi: "ja staryu is goed, zet maar in af". `staryu/af/staryu_regional.png` (= sprite_r5: model r4, keuring + eindkeuring PASS), op het overzichtsvel (Regional forms).

## Type
- Jordi (27 nov): "staryu en starmie normaal worden water/cosmic" (gewone vorm). Voorstellen Claude voor de koekjes-vorm: Fairy → Fairy/Cosmic (aanbevolen), Fairy → Fairy/Psychic, Fire → Fire/Fairy, Normal → Normal/Fairy, Water → Water/Fairy.
- **Besloten (Jordi, 27 nov): "fairy staryu en fairy/psychic starmie doen we".** Regionale Staryu Fairy, regionale Starmie Fairy/Psychic.

## Starmie: ook de voorpunten (27 nov)
Jordi na r5: "de punten van de voorkant moeten ook minder puntig van starmie".
Jordi (27 nov), met uitsnede `referenties/jordi_starmie_punten.png` (Gen 3 Starmie, de twee punten rechts): "meet desnoods de hoek van de originele starmie sprite op deze twee".

## Starmie r6 gekozen (27 nov)
Uit licht | sterk | naar Jordi's twee Gen 3-punten: "ik vind 1 het beste" = `starmie/sprite_r6/starmie_r6_licht.png` (alle tien punten afgesneden waar ze 4 px breed zijn).

## Starmie r8 (27 nov)
Jordi over r7: "de bovenkant is wat afgekapt", "is nu een rechte lijn". r8: bovenste voorpunt 1 (A) of 2 (B) rijen terug op de plek van het modelsilhouet (r5), 3 px breed; de platte toprij van r7 wordt binnenrij. `starmie/sprite_r8/`.
Jordi: "A is uitstekend, eindkeuring daarvoor qua schaduw etc".
